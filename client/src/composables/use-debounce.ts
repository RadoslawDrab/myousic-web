export function useDebounce<T extends Record<string, any>>(targetRef: Ref<string | T>, delay: number = 1500, options?: { immediate?: boolean, targetKey?: keyof T  }) {
    const getValue = (value: string | T) => typeof value === 'string' ? value : (options.targetKey ? value[options.targetKey] : '')

    const localValue = ref<string>(getValue(targetRef.value))
    let timeout: ReturnType<typeof setTimeout>

    watch(localValue, (val) => {
        clearTimeout(timeout)
        timeout = setTimeout(() => {
            if (typeof targetRef.value === 'string') {
                targetRef.value = val
                return
            }
            if (!options.targetKey) return
            // @ts-expect-error Correct key
            targetRef.value[options.targetKey] = val
        }, delay)
    }, { immediate: options.immediate })

    watch(targetRef, (newVal) => {
        const _newVal = getValue(newVal)
        if (_newVal === localValue.value) return
        localValue.value = _newVal;
    }, { immediate: options.immediate });

    return localValue
}