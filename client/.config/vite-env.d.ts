import 'vue-router'

interface ImportMetaEnv {
    readonly BASE_URL: string
    readonly DEV: boolean
    readonly MODE: 'development' | 'production'
    readonly PROD: boolean
    readonly SSR: boolean
    readonly VITE_API_URL: string
    readonly VITE_APP_NAME: string
    readonly VITE_VERSION: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}

declare module 'vue-router' {
    interface RouteMeta {
        title: string
        icon?: string
        includeInNav?: boolean
        order?: number
        class?: string | string[]
        path?: string
        activeRegEx?: string | RegExp
    }
}

export {}