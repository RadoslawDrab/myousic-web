import { useStorage } from '@vueuse/core'

export interface SessionData<Item = SearchAPI_Result> {
    items?: Item[]
    url?: string
    search?: string
    entity?: SearchAPI_Entity
    result?: API_SearchUrlResult
    settings?: Settings
}

const useData = <Item = SearchAPI_Result>(defaultData?: SessionData<Item>) => {
	return useStorage<SessionData<Item>>(
        import.meta.env.VITE_APP_NAME.toUpperCase() + '_DATA',
        {
            items: [],
            entity: 'song',
            settings: {
                lyricsProviders: ['AzLyrics', 'Genius'],
                artworkSize: 500,
                includedGenres: [],
                excludedGenres: [],
                lyricsModifier: {},
            },
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
}

export default useData