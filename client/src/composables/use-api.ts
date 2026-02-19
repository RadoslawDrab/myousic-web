import useData from '@/composables/use-data'
import useFetch from '@/composables/use-fetch'
import { TRACK_KEYS } from '@/utils/api'
import { download } from '@/utils'
import { pascalCase } from '@/utils/string'
import Mustache from 'mustache'

const useApi = () => {
    const { isLoading, status, get, post } = useFetch()
    const { local } = useData()

    async function searchApi(options: SearchAPI_Options): Promise<{ resultCount: number, results: (SearchAPI_TrackResult & SearchAPI_ArtistResult & SearchAPI_AlbumResult)[] }> {
        const query = {}

        query['media'] = 'music'
        query['country'] = options.country || 'US'

        Object.entries(options).forEach(([key, value]) => {
            if (query[key]) return
            query[key] = value
        })
        return await get(null, { query, baseUrl: 'https://itunes.apple.com/search' })
    }

    type ExtraOptions = {
        lyrics?: string
        genres?: string[]
        comment?: string
        artworkFile?: File
    }
    async function downloadTrack(url: string, track: SearchAPI_TrackResult | Partial<ExtendedTrack>, options?: ExtraOptions) {
        const _track = TRACK_KEYS.reduce((acc, key) => {
            acc[key] = track[key]
            return acc
        }, { ...(options || {})} as Record<string, any>)

        const formData = new FormData()

        formData.append('body', JSON.stringify({
                url,
                track: { ..._track, comment: renderComment(url, track, options) }
            }
        ))
        if (options.artworkFile) formData.append('artworkFile', options.artworkFile)

        const { fileName, downloadUrl } = await post<{ fileName: string, downloadUrl: string }>(formData, {
            baseUrl: import.meta.env.VITE_API_URL,
            path: [],
            query: {
                artworkSize: local.value.artworkSize
            }
        })

        download(fileName, downloadUrl)
    }
    function renderComment(url: string, track: SearchAPI_TrackResult | Partial<ExtendedTrack>, options?: ExtraOptions, renderError: boolean = false): string {
        const _track = { ...track, ...(options || {})}

        if (!_track.comment) {
            _track.comment = local.value.defaultComment
        }

        const variables = {
            url,
            ..._track,
            genres: () => {
                return (_track.genres || []).map(v => pascalCase(v))
            }
        }

        try {
            return Mustache.render(_track.comment || '', variables, {}, { escape: (text) => text })
        } catch (e) {
            if (renderError) return e
            else console.error(e)
        }
        return ''
    }

    async function getTrackData(track: SearchAPI_TrackResult | ExtendedTrack) {
        return await get<{
            genres: string[]
            genresUrl: string
            lyrics: string
            lyricsUrl: string
        }>(null, {
            path: [track.artistName, track.trackName],
            query: local.value ? {
                lyrics: local.value.lyricsProviders,
                lyricsModifier: Object.entries(local.value.lyricsModifier).map(([key, value]) => `${key}:${value}`),
                excludedGenres: local.value.excludedGenres,
                includedGenres: local.value.includedGenres
            } : {}
        })
    }

    return {
        isLoading,
        status,
        searchApi,
        downloadTrack,
        getTrackData,
        renderComment
    }
}

export default useApi