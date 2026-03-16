import { useStorage } from '@vueuse/core'

const useSession = <T extends object>(defaultValue: T, suffix: string = 'DATA') => {
    return useStorage<T>(
        (import.meta.env.VITE_APP_NAME || 'APP').toUpperCase() + '_' + suffix.toUpperCase().replace(/^_+/g, ''),
        defaultValue,
        sessionStorage,
        {
            mergeDefaults: true,
            serializer: {
                read: (value) => JSON.parse(value),
                write: (value) => JSON.stringify(value)
            }
        }
    )
}

export default useSession