import { useStorage } from '@vueuse/core'
import { nullColor } from 'vuetify/components/VColorPicker/util'

const useData = () => {
	const session = useStorage<SessionData>(
        (import.meta.env.VITE_APP_NAME || 'APP').toUpperCase() + '_DATA',
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
        (import.meta.env.VITE_APP_NAME || 'APP').toUpperCase() + '_SETTINGS',
        {
            lyricsProviders: ['AzLyrics', 'Genius', 'LyricsOvh', 'Lyrist'],
            artworkSize: 500,
            includedGenres: [],
            excludedGenres: [],
            lyricsModifier: {},
            defaultComment: '[URL: {{ url }}]',
            audio: {
                extension: 'm4a',
                sampleRate: 48000
            }
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