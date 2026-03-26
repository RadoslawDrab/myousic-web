import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { VitePWA } from 'vite-plugin-pwa'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import VueRouter from 'unplugin-vue-router/vite'

export default defineConfig(({ mode }) => {
    const DEV = mode === 'development'
    return {
        envDir: DEV ? '../' : './',
        preview: {
            port: 4000,
            proxy: {
                '/api': {
                    target: 'http://localhost:5000',
                    changeOrigin: true,
                }
            }
        },
        server: {
            port: 3000
        },
        build: {
            outDir: './dist',
            copyPublicDir: true
        },
        plugins: [
            Components({
                dts: '.config/components.d.ts'
            }),
            AutoImport({
                imports: [
                    'vue',
                    'vue-router',
                    '@vueuse/core'
                ],
                dts: '.config/import.d.ts'
            }),
            VueRouter({
                routesFolder: [
                    'src/views',
                ],
                extensions: ['.vue', '.md'],
                dts: './.config/typed-router.d.ts'
            }),
            VitePWA({
                registerType: 'autoUpdate',
                injectRegister: 'script',
                workbox: {
                  navigateFallbackDenylist: [/^\/api\//]
                },
                manifest: {
                    lang: 'en',
                    name: 'Myousic',
                    short_name: 'Myousic',
                    description: 'Web app for downloading and fetching music from YouTube',
                    start_url: '/',
                    display: 'standalone',
                    categories: ["productivity", "utilities"],
                    theme_color: '#121212',
                    icons: [
                        {
                            src: '/icons/pwa-192x192.png',
                            sizes: '192x192',
                            type: 'image/png'
                        },
                        {
                            src: '/icons/pwa-512x512.png',
                            sizes: '512x512',
                            type: 'image/png',
                        },
                        {
                            src: '/icons/pwa-192x192.png',
                            sizes: '192x192',
                            type: 'image/png',
                            purpose: 'any'
                        },
                        {
                            src: '/icons/pwa-512x512.png',
                            sizes: '512x512',
                            type: 'image/png',
                            purpose: 'any'
                        }
                    ]
                }
            }),
            vue({
                include: [/\.vue$/]
            }),
            vueDevTools(),
        ],
        resolve: {
            alias: {
                '@': fileURLToPath(new URL('./src', import.meta.url)),
                '@public': fileURLToPath(new URL('./public', import.meta.url))
            }
        }
    }
})
