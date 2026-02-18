from typing import Callable, Iterator, Self, TypeVar
from types import FunctionType, SimpleNamespace

M = TypeVar('M', bound=Callable[[], any])
class Singleton:
	_instance: Self | None = None
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super(Singleton, cls).__new__(cls)
		return cls._instance
	def __init__(self):
		if not self.initiated:
			raise RuntimeError('Instance not initiated')
	@property
	def initiated(self):
		return self._instance is not None
	@classmethod
	def exists(cls, method: M) -> M:
		def wrapper(*args, **kwargs):
			context = args[0]

			if isinstance(context, type) and issubclass(context, Singleton):
				instance = context._instance
			else:
				instance = context

			if instance is None or not instance.initiated:
				raise RuntimeError(
					f"Cannot call method '{method.__name__}'. "
					"Singleton instance is not yet initiated."
				)

			return method(*args, **kwargs)
		wrapper.__name__ = method.__name__
		wrapper.__doc__ = method.__doc__
		return wrapper # type: ignore

class Namespace(SimpleNamespace):
	def __getattr__(self, item):
		try:
			return super().__getattribute__(item)
		except AttributeError:
			return None
	def __getitem__(self, item):
		try:
			return super().__getattribute__(item)
		except AttributeError:
			return None
	def __iter__(self) -> Iterator[tuple[str, any]]:
		return iter([(k, v) for k, v in self.dict().items()])
	def __contains__(self, item):
		return str(item) in self.dict().keys()
	def dict(self, *include_keys: str):
		return {
			key: value
			for key, value in self.__dict__.items() if
			not key.startswith('_') and
			not isinstance(key, FunctionType) or
			key in include_keys
		}

class Enum:
	def __iter__(self):
		return self.dict().items()
	def __contains__(self, item):
		return item in self.dict().keys()

	@classmethod
	def dict(cls, *exclude_keys: str) -> dict[str, any]:
		return { key: value for key, value in cls.__dict__.items() if
		         not key.startswith('_') and not isinstance(value, FunctionType) and key not in exclude_keys }

class EnumMeta(type):
	class Member:
		def __init__(self, name: str, value: any, parent: str | None = None):
			self._name = name
			self._value = value
			self._parent = parent

		# Allow comparison by value
		def __eq__(self, other):
			return self._value == (other._value if isinstance(other, EnumMeta.Member) else other)

		# The representation is what you see when printing the object
		def __repr__(self):
			return f'<{self._parent + '.' if self._parent else ''}{self._name}: {self._value}>'

		# Properties to access name and value
		@property
		def name(self):
			return self._name

		@property
		def value(self):
			return self._value
	def __new__(mcs, name, bases, attrs):
		_members = { }
		_member_names = []

		# 1. Create a class to hold the individual permission details


		# 2. Iterate through all attributes defined in the Permission class
		new_attrs = { }
		for attr_name, attr_value in attrs.items():
			# Skip magic/private methods and previously defined attributes
			if attr_name.startswith('_') or attr_name in ('EnumMember', '_members', '_member_names'):
				new_attrs[attr_name] = attr_value
				continue

			# 3. Create a Member instance for the constant
			member_obj = EnumMeta.Member(attr_name, attr_value, name)

			# 4. Store the Member object in the class attributes
			new_attrs[attr_name] = member_obj

			# 5. Store the member for iteration and internal tracking
			_members[attr_name] = member_obj
			_member_names.append(attr_name)

		# 6. Add the internal members list/dict to the new class
		new_attrs['_member_map_'] = _members
		new_attrs['_member_names_'] = tuple(_member_names)

		# 7. Create the actual class
		return super().__new__(mcs, name, bases, new_attrs)
	def __getitem__(self, item):
		return getattr(self, item)