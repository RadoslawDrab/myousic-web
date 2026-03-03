<script setup lang="ts">
import { formatTitle } from '@/utils/string'

const route = useRoute()
const title = useTitle()

watch(() => route.meta.title, (_title) => {
  if (!_title) return
  title.value = formatTitle(_title)
})

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