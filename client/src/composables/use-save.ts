function useSave<T extends object>(targetRef: Ref<T>, key: keyof T): { draft: Ref<T[keyof T]>, isChanged: Ref<boolean>, save: () => void, reset: () => void }
function useSave<T>(targetRef: Ref<T>): { draft: Ref<T>, isChanged: Ref<boolean>, save: () => void, reset: () => void }
function useSave<T>(targetRef: Ref<T>, key?: keyof T) {
    const getValue = () => {
        const val = targetRef.value
        const result = (key && val && typeof val === 'object') ? val[key] : val
        // Deep clone to break reference link
        return result && typeof result === 'object' ? JSON.parse(JSON.stringify(result)) : result
    }

    const draft = ref(getValue())

    const isChanged = computed(() => {
        const current = getValue()
        return JSON.stringify(draft.value) !== JSON.stringify(current)
    })

	function save() {
        const rawValue = toRaw(draft.value)
        if (key && typeof targetRef.value === 'object' && targetRef.value !== null) {
            targetRef.value[key] = rawValue
        } else {
            targetRef.value = rawValue
        }
    }
    function reset() {
        draft.value = getValue()
    }

    watch(() => getValue(), (newVal) => {
        if (isChanged.value) return
        draft.value = newVal
    }, { deep: true })

    return {
        draft,
        isChanged,
        save,
        reset
    }
}

export default useSave