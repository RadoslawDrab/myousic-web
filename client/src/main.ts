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

const vuetifyInputOptions = {
    variant: 'solo-filled',
    hideDetails: true
}

const vuetify = createVuetify({
    icons: {
      defaultSet: 'mdi'
    },
    defaults: {
        VBtn: {
          variant: 'tonal'
        },
        VTextarea: vuetifyInputOptions,
        VCombobox: vuetifyInputOptions,
        VFileInput: vuetifyInputOptions,
        VTextField: vuetifyInputOptions,
        VSelect: vuetifyInputOptions,
        VNumberInput: vuetifyInputOptions
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
