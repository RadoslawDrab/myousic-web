export function mapRecursive<T1 extends object, T2 extends object = T1>(items: RecursiveObject<T1>[], callback: (item: T1) => T2): RecursiveObject<T2>[] {
    return items.map(item => {

        const returnValue = callback(item)
        if (item.children && item.children.length > 0) {
            return {
                ...returnValue,
                children: mapRecursive(item.children, callback)
            }
        }

        return returnValue
    });
}

export function filterRecursive<T extends object>(items: RecursiveObject<T>[], callback: (item: T) => boolean): RecursiveObject<T>[] {
    return items.filter(item => {
        let isValid = callback(item)
        if (isValid && item.children && item.children.length > 0) {
            return filterRecursive(item.children, callback)
        }

        return isValid
    });
}

export function flattenRecursive<T extends object>(items: RecursiveObject<T>[], key: keyof T): string[] {
    let ids: string[] = [];
    items.forEach(item => {
        ids.push(item[key] as string); // Using key or id
        if (item.children && item.children.length > 0) {
            ids = [...ids, ...flattenRecursive(item.children, key)];
        }
    });
    return ids;
}

export function flattenRecursiveObject<T extends object>(
    items: RecursiveObject<T & { parentId?: string }>[],
    key: keyof T,
    callback?: (item: T & { parentId?: string }) => boolean,
    parentId?: string
): RecursiveObject<T & { parentId?: string }>[] {
    let _items: RecursiveObject<T & { parentId?: string }>[] = [];
    items.forEach(item => {
        if (callback ? callback(item) : true) {
            _items.push({ ...item, parentId })
        }

        if (item.children && item.children.length > 0) {
            _items = [
                ..._items,
                ...flattenRecursiveObject(
                    item.children,
                    key,
                    callback,
                    item[key] as string
                )
            ]
        }
    });
    return _items;
}