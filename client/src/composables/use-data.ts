import { useStorage } from '@vueuse/core'

export interface SessionData {
    items?: SearchAPI_Result[]
    url?: string
    search?: string
    entity?: SearchAPI_Entity
    result?: API_SearchUrlResult
    savedTrack?: Partial<ExtendedTrack>
}
export interface LocalData extends Settings {
}

const useData = () => {
	const session = useStorage<SessionData>(
        import.meta.env.VITE_APP_NAME.toUpperCase() + '_DATA',
        {
            items: [],
            entity: 'song',
        },
        sessionStorage,
        {
            mergeDefaults: true,
            serializer: {
                read: (value) => JSON.parse(value),
                write: (value) => JSON.stringify(value)
            }
        }
    )

    const local = useStorage<LocalData>(
        import.meta.env.VITE_APP_NAME.toUpperCase() + '_SETTINGS',
        {
            lyricsProviders: ['AzLyrics', 'Genius'],
            artworkSize: 500,
            includedGenres: [],
            excludedGenres: [],
            lyricsModifier: {},
            defaultComment: '[URL: {{ url }}]'
        },
        localStorage,
        {
            mergeDefaults: true,
            serializer: {
                read: (value) => JSON.parse(value),
                write: (value) => JSON.stringify(value)
            }
        })

    return { session, local }
}

export default useData