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

    export type LyricsProvider = 'AzLyrics' | 'Genius'
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
        fileContent?: string
    }>

    export type Social = {
        name: string
        url: string
        icon: string
    }
}