<script setup lang="ts">
  import useData from '@/composables/use-data'
  import { useDebounce } from '@/composables/use-debounce'
  import { formatTitle } from '@/utils/string'
  import { useTitle } from '@vueuse/core'

  const props = withDefaults(defineProps<{
    countdownSeconds?: number
  }>(), {
    countdownSeconds: 1
  })

  const title = useTitle()
  const sessionData = useData()
  const search = useDebounce(sessionData, 1500, { targetKey: 'search' })

  watch(() => sessionData.value.search, (search) => {
    title.value = formatTitle(search)
  }, { immediate: true })

</script>

<template>
  <div class="d-flex align-center ga-2">
    <v-text-field
        v-model="search"
        placeholder="Track, Artist or Album"
        clearable
        rounded="sm"
        hide-details
        flat
    >
    </v-text-field>
    <v-select
        v-model="sessionData.entity"
        :items="[
          { title: 'Track', value: 'song' },
          { title: 'Artist', value: 'musicArtist' },
          { title: 'Album', value: 'album' }
        ]"
        hide-details
    >
    </v-select>
    <slot></slot>
  </div>
</template>