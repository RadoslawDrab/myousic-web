<script setup lang="ts">
  const route = useRoute()
  const router = useRouter()

  const name = computed(() => import.meta.env.VITE_APP_NAME)
  const breadcrumbs = computed<string[]>(() => {
    return route.matched.filter(v => v.meta.title || v.name).map(v => (v.meta.title || v.name) as string)
  })
  const links = computed<{ icon: string, path: string, title: string }[]>(() =>
      router.getRoutes()
            .filter(route => route.meta.includeInNav)
            .sort((r1, r2) => (r1.meta.order ?? 0) - (r2.meta.order ?? 0))
            .map(route => {
              return {
                icon: route.meta.icon || '',
                title: route.meta.title || 'Link',
                path: route.path || '/',
              }
            })
  )
</script>

<template>
  <Flex class="mb-3 border-b flex-wrap" :gap="2" align="center" justify="space-between">
    <Flex class="flex-wrap align-start align-sm-center" :gap="2">
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
      <v-btn v-for="link in links" class="text-none" :to="link.path" :prepend-icon="link.icon" variant="plain" active-color="primary" flat>{{ link.title }}</v-btn>
<!--      <v-btn class="text-none" to="/settings" prepend-icon="mdi-cog" variant="plain" flat active-color="primary">Settings</v-btn>-->
<!--      <v-btn class="text-none" to="/docs" prepend-icon="mdi-file-document" variant="plain" flat active-color="primary">Docs</v-btn>-->
<!--      <v-btn class="text-none" to="/download" prepend-icon="mdi-download" variant="plain" flat active-color="primary">Download</v-btn>-->
    </Flex>
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
  </Flex>
</template>