import useFetch from '@/composables/use-fetch'
import { TRACK_KEYS } from '@/utils/api'
import { download } from '@/utils'
import { pascalCase } from '@/utils/string'
import Mustache from 'mustache'

const useApi = () => {
    const { isLoading, status, get, post } = useFetch()

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
    }
    async function downloadTrack(url: string, track: ExtendedTrack)
    async function downloadTrack(url: string, track: SearchAPI_TrackResult, options?: ExtraOptions)
    async function downloadTrack(url: string, track: SearchAPI_TrackResult | ExtendedTrack, options?: ExtraOptions) {
        const _track = TRACK_KEYS.reduce((acc, key) => {
            acc[key] = track[key]
            return acc
        }, { ...(options || {})} as Record<string, any>)
        const { fileName, downloadUrl } = await post<{ fileName: string, downloadUrl: string }>({
            url,
            track: { ..._track, comment: renderComment(url, track, options) }
        })

        download(fileName, downloadUrl)
    }
    function renderComment(url: string, track: SearchAPI_TrackResult | ExtendedTrack, options?: ExtraOptions, renderError: boolean = false): string {
        const _track = { ...track, ...(options || {})}

        if (!_track.comment) return ''

        const variables = {
            url,
            ..._track,
            genres: () => {
                return (_track.genres || []).map(v => pascalCase(v))
            }
        }
        try {
            return Mustache.render(_track.comment || '', variables)
        } catch (e) {
            if (renderError) return e
            else console.error(e)
        }
        return ''
    }

    async function getTrackData(track: SearchAPI_TrackResult | ExtendedTrack, settings?: Settings) {
        return await get<{
            genres: string[]
            genresUrl: string
            lyrics: string
            lyricsUrl: string
        }>(null, {
            path: [track.artistName, track.trackName],
            query: settings ? {
                lyrics: settings.lyricsProviders,
                lyricsModifier: Object.entries(settings.lyricsModifier).map(([key, value]) => `${key}:${value}`),
                // lyricsModifier: Object.entries(settings.lyricsModifier).reduce((acc, [key, value], index) => acc += `${index > 0 ? ',' : ''}${key}:${value}`, ''),
                excludedGenres: settings.excludedGenres,
                includedGenres: settings.includedGenres
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