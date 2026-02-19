
export {}

declare global {
    export type SearchAPI_Attribute = 'mixTerm' | 'genreIndex' | 'artistTerm' | 'composerTerm' | 'albumTerm' | 'ratingIndex' | 'songTerm'
    export type SearchAPI_Entity = 'musicArtist' | 'musicTrack' | 'album' | 'musicVideo' | 'mix' | 'song'
    export type SearchAPI_Options = {
        term: string
        country?: string
        entity?: SearchAPI_Entity
        limit?: number
        attribute?: SearchAPI_Attribute
        explicit?: boolean
    }

    export type SearchAPI_Explicitness = 'explicit' | 'cleaned' | 'notExplicit'

    export type SearchAPI_TrackResult = {
        wrapperType: 'track'
        // Artist
        artistId: string
        artistName: string
        artistViewUrl: string
        // Album
        collectionId: string
        collectionName: string
        collectionCensoredName: string
        collectionExplicitness: SearchAPI_Explicitness
        collectionViewUrl: string
        // Track
        trackId: string
        trackName: string
        trackExplicitness: SearchAPI_Explicitness
        trackCensoredName: string
        trackCount: number
        trackNumber: number
        discCount: number
        discNumber: number
        trackTimeMillis: number
        trackViewUrl: string
        artworkUrl30?: string
        artworkUrl60?: string
        artworkUrl100?: string
        primaryGenreName: string
        previewUrl?: string
        releaseDate: string
    }
    export type SearchAPI_ArtistResult = {
        wrapperType: 'artist'
        artistId: number
        artistName: string
        artistType: string
        primaryGenreName: string
        primaryGenreId: number
        artistLinkUrl: string
    }
    export type SearchAPI_AlbumResult = {
        wrapperType: 'collection'
        collectionType: string
        artistId: number
        collectionId: number
        artistName: string
        collectionName: string
        collectionCensoredName: string
        collectionExplicitness: SearchAPI_Explicitness
        collectionViewUrl: string
        artworkUrl30?: string
        artworkUrl60?: string
        artworkUrl100: string
        primaryGenreName: string
        artistViewUrl: string
        trackCount: number
    }

    export type SearchAPI_Result = SearchAPI_TrackResult | SearchAPI_ArtistResult | SearchAPI_AlbumResult
    export type SearchAPI_ResultKeys = SearchAPI_TrackResult & SearchAPI_ArtistResult & SearchAPI_AlbumResult

    export type CustomTrack = Pick<
        SearchAPI_TrackResult,
        'trackName' |
        'artistName' |
        'collectionName' |
        'artworkUrl100' |
        'primaryGenreName' |
        'trackNumber' |
        'trackCount' |
        'discNumber' |
        'discCount' |
        'trackTimeMillis' |
        'releaseDate'
    >

    export type ExtendedTrack = CustomTrack & {
        comment?: string
        genres?: string[]
        genresUrl?: string
        lyrics?: string
        lyricsUrl?: string
    }

    export type API_Response = {
        code: number
        message: string
    }
    export type API_SearchUrlResult = {
        id: string
        artist?: string
        fullTitle: string
        artworkUrl: string
        title?: string
        releaseDate: number
        url: string
    }
}