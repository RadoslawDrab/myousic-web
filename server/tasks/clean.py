from pathlib import Path

from utils.logger import Logger


def clean(output_path: Path, DEV: bool, **kwargs):
	for item in output_path.rglob('*'):
		if not item.is_file(): continue
		item.unlink()
		Logger.log(f'Removed {item}', log_type='INFO', print_only=DEV)
