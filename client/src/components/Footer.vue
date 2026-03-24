<script setup lang="ts">
  import useSocials from '@/composables/use-socials'

  const VERSION = computed(() => import.meta.env.VITE_VERSION)
  const socials = useSocials()
</script>

<template>
  <Flex class="w-100" justify="space-between" align="center">
    <Flex align="center">
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
    <span class="d-block text-right text-caption text-grey-darken-1">
      Version: {{ VERSION }}
    </span>
  </Flex>
</template>