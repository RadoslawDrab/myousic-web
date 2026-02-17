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

    export type LyricsProvider = 'AzLyrics' | 'Genius'
    export type Settings = {
        lyricsProviders: LyricsProvider[]
        artworkSize: number
        lyricsModifier: Record<string, string>
        includedGenres: string[]
        excludedGenres: string[]
        defaultComment: string
    }
}