import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'
import { createHead } from '@unhead/vue/client'
import * as vComponents from 'vuetify/components'
import * as vDirectives from 'vuetify/directives'

import { router } from './router'
import directives from '@/directives/index'

import 'vuetify/styles'
import './assets/main.scss'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'


const vuetify = createVuetify({
    icons: {
      defaultSet: 'mdi'
    },
    defaults: {
        VTextarea: {
            variant: 'solo-filled'
        },
        VCombobox: {
            variant: 'solo-filled'
        },
        VFileInput: {
            variant: 'solo-filled'
        },
        VTextField: {
            variant: 'solo-filled'
        },
        VSelect: {
            variant: 'solo-filled'
        },
        VNumberInput: {
            variant: 'solo-filled'
        }
    },
    components: vComponents,
    directives: vDirectives,
})

const app = createApp(App)

Object.entries(directives).forEach(([name, key]) => app.directive(name, key))

app.use(router)
app.use(createPinia())
app.use(vuetify)
app.use(createHead())

app.mount('#app')
