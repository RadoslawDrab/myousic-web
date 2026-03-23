export {}

declare global {
    export type DataTableHeader = RecursiveObject<{
        title: MessageKeys | string
        key: string
        originalKey?: string
        id?: string
        sortable?: boolean
        filterable?: boolean
        removable?: boolean
        defaultShow?: boolean
        hide?: boolean
        disabled?: boolean
        formatter?: FormatterFunction | CellType
    }>

    export interface SessionData {
        items?: SearchAPI_Result[]
        url?: string
        search?: string
        entity?: SearchAPI_Entity
        result?: API_SearchUrlResult
    }

    export type LyricsProvider = 'AzLyrics' | 'Genius' | 'LyricsOvh' | 'Lyrist'
    export type LocalData = {
        lyricsProviders: LyricsProvider[]
        artworkSize: number
        audio: {
            extension: string
            sampleRate: number
        }

        lyricsModifier: Record<string, string>
        includedGenres: string[]
        excludedGenres: string[]
        defaultComment: string
    }

    export type DocsData = RecursiveObject<{
        id?: string
        icon?: string
        title: string
        file: string
        tags?: string[]
        description?: string
        path?: string
    }>

    export type Social = {
        name: string
        url: string
        icon: string
    }

    export type QueueItem = {
        status: 'completed' | 'pending' | 'failed',
        id: string,
        finished: boolean,
        createdAt: number,
        updatedAt: number,
        data: {
            downloadUrl?: string,
            url: string,
            track: Partial<ExtendedTrack>
        }
    }
}