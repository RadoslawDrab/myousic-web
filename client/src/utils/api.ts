export const TRACK_KEYS: (keyof SearchAPI_TrackResult | keyof ExtendedTrack)[] = ['trackName', 'artistName', 'collectionName', 'artworkUrl100', 'primaryGenreName', 'trackNumber', 'trackCount', 'discNumber', 'discCount', 'trackTimeMillis', 'releaseDate', 'comment', 'lyrics', 'genres', 'clipping']

export function getArtworkUrl(url: string, size: number = 1000) {
    const clamped = Math.round(Math.max(Math.min(size, 3000), 100))
    return url.replace(/\d+x\d+b/, `${clamped}x${clamped}b`)
}

export function getApiUrl(_baseUrl?: string | null, ...paths: string[]): string {
    const baseUrl = (_baseUrl || import.meta.env.CLIENT_API_URL || '/api').replace('/+$', '')
    const newPath = paths.filter(p => p).join('/')
    return `${ baseUrl }${ newPath ? '/' + newPath : '' }`
}