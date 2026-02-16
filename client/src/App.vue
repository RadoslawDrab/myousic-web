<script setup lang="ts">
import useData from '@/composables/use-data'

const route = useRoute()

const isDocsRoute = computed(() => route.path.startsWith('/docs'))
const lastPath = ref<string>('/')

watch(() => route.path, (path) => {
  if (isDocsRoute.value) return

  lastPath.value = path
}, { immediate: true })
</script>

<template>
  <v-app theme="dark">
    <v-theme-provider>
      <v-layout>
        <v-main class="mx-auto pa-4 w-100" :style="{ 'max-width': '1000px' }">
          <UrlDataSearch v-if="!isDocsRoute" class="mb-3" />
          <RouterView />
          <SettingsDial />
          <v-fab :to="!isDocsRoute ? '/docs' : lastPath" app location="bottom left" icon="mdi-file-document" v-tooltip="'Docs'"></v-fab>
          <StatusHandler />
        </v-main>
      </v-layout>
    </v-theme-provider>
  </v-app>
</template>
