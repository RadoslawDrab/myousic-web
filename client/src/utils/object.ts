export function isObject(item: any): boolean {
    return item && typeof item === 'object' && !Array.isArray(item)
}

export function deepMerge<T extends object>(target: T, ...sources: object[]): T {
    if (!sources.length) return target
    const source = sources.shift()

    if (isObject(target) && isObject(source)) {
        for (const key in source) {
            if (isObject(source[key])) {
                if (!target[key]) Object.assign(target, { [key]: {} });
                deepMerge(target[key], source[key]);
            } else {
                Object.assign(target, { [key]: source[key] });
            }
        }
    }
    return deepMerge(target, ...sources);
}

export function sanitizeObject<T extends object>(obj: object, keysOrObject: T | (keyof T)[]): Partial<T> {
    const keys = Array.isArray(keysOrObject) ? keysOrObject : Object.keys(keysOrObject)

    return keys
        // @ts-ignore
        .filter(key => obj[key] !== undefined)
        .reduce((acc, key) => {
            return {
                ...acc,
                // @ts-ignore
                [key]: obj[key]
            }
        }, {})
}