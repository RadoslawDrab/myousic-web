<script setup lang="ts">
import { formatTitle } from '@/utils/string'

const route = useRoute()
const title = useTitle()

const lastPath = ref<string>('/')
const isDocsRoute = computed(() => route.path.startsWith('/docs'))
const name = computed(() => import.meta.env.VITE_APP_NAME)

const breadcrumbs = computed<string[]>(() => {
  return route.matched.filter(v => v.meta.title || v.name).map(v => (v.meta.title || v.name) as string)
})

watch(() => route.path, (path) => {
  if (isDocsRoute.value) return

  lastPath.value = path
}, { immediate: true })

watch(() => route.meta, (meta) => {
  if (!meta.title) return
  title.value = formatTitle(meta.title)
}, { deep: true })

</script>

<template>
  <v-app theme="dark">
    <v-theme-provider>
      <v-layout>
        <v-main class="mx-auto pa-2 px-sm-4 w-100" :style="{ 'max-width': '1100px' }">
          <Header />
          <RouterView />
          <StatusHandler />
        </v-main>
      </v-layout>
    </v-theme-provider>
  </v-app>
</template>