<script setup lang="ts">
  import useSocials from '@/composables/use-socials'
  import { joinClass } from '@/utils/string'

  const route = useRoute()
  const router = useRouter()

  const breadcrumbs = computed<string[]>(() => {
    return route.matched.filter(v => v.meta.title || v.name).map(v => (v.meta.title || v.name) as string)
  })

  const socials = useSocials()

  const links = computed<{ icon: string, path: string, title: string, class?: string[], active?: boolean }[]>(() =>
      router.getRoutes()
            .filter(route => route.meta.includeInNav)
            .sort((r1, r2) => (r1.meta.order ?? 0) - (r2.meta.order ?? 0))
            .map(r => {
              const path = r.meta.path || r.path || '/'
              return {
                icon: r.meta.icon || '',
                title: r.meta.title || 'Link',
                path,
                class: Array.isArray(r.meta.class) ? r.meta.class : [r.meta.class],
                active: r.meta.activeRegEx ? new RegExp(r.meta.activeRegEx).test(route.path) : undefined
              }
            })
  )

</script>

<template>
  <Flex class="mb-3 border-b flex-wrap" :gap="2" align="center" justify="space-between">
    <Flex class="flex-wrap align-start align-sm-center" :gap="2">
      <v-btn
          v-for="link in links"
          :class="joinClass('text-none', ...link.class)"
          :to="link.path"
          :prepend-icon="link.icon"
          variant="plain"
          active-color="primary"
          :active="link.active"
          flat
      >
        {{ link.title }}
      </v-btn>
    </Flex>
    <Flex align="center">
      <v-breadcrumbs :class="socials.length > 0 ? 'border-e' : ''" :items="breadcrumbs"></v-breadcrumbs>
      <v-btn
          v-for="social in socials"
          :icon="social.icon"
          :href="social.url"
          variant="text"
          density="compact"
          target="_blank"
          v-tooltip="social.name"
      ></v-btn>
    </Flex>
  </Flex>
</template>