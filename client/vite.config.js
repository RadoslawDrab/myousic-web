import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import VueRouter from 'unplugin-vue-router/vite'
import Markdown from 'unplugin-vue-markdown/vite'

export default defineConfig(({ mode }) => {
  const DEV = mode === 'development'
  return {
      server: {
          port: 3000
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
        Markdown({
            headEnabled: true,
            exposeFrontmatter: true,
            extendFrontmatter(frontmatter) {
                return { ...frontmatter }
            }
        }),
        vue({
            include: [/\.vue$/, /\.md$/]
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
