interface ImportMetaEnv {
    readonly BASE_URL: string
    readonly DEV: boolean
    readonly MODE: 'development' | 'production'
    readonly PROD: boolean
    readonly SSR: boolean
    readonly VITE_API_URL: string
    readonly VITE_APP_NAME: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}