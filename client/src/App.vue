<script setup lang="ts">
const route = useRoute()

const lastPath = ref<string>('/')
const isDocsRoute = computed(() => route.path.startsWith('/docs'))

const name = computed(() => import.meta.env.VITE_APP_NAME)

const breadcrumbs = computed<string[]>(() => {
  return route.matched.filter(v => v.meta.breadcrumbs || v.name).map(v => (v.meta.breadcrumbs || v.name) as string)
})

watch(() => route.path, (path) => {
  if (isDocsRoute.value) return

  lastPath.value = path
}, { immediate: true })
</script>

<template>
  <v-app theme="dark">
    <v-theme-provider>
      <v-layout>
        <v-main class="mx-auto pa-2 pa-sm-4 w-100" :style="{ 'max-width': '1100px' }">
          <Flex class="mb-3 border-b" :gap="2" align="center" justify="space-between">
            <Flex align="center" :gap="2">
              <v-btn
                  class="text-none"
                  prepend-icon="mdi-home"
                  to="/"
                  variant="plain"
                  rounded="sm"
                  flat
                  active-color="primary"
              >
                {{ name }}
              </v-btn>
              <v-divider vertical />
              <v-btn class="text-none" to="/settings" prepend-icon="mdi-cog" variant="plain" flat active-color="primary">Settings</v-btn>
              <v-btn class="text-none" to="/docs" prepend-icon="mdi-file-document" variant="plain" flat active-color="primary">Docs</v-btn>
            </Flex>
            <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
          </Flex>
          <RouterView />
          <StatusHandler />
        </v-main>
      </v-layout>
    </v-theme-provider>
  </v-app>
</template>
