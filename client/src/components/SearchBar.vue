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

  const emit = defineEmits<{
    'search': [value: string]
  }>()

  const title = useTitle()
  const { session } = useData()
  const search = useDebounce(session, 1500, { targetKey: 'search' })


  watch(() => session.value.search, (search) => {
    title.value = formatTitle(search)
  }, { immediate: true })

</script>

<template>
  <v-form class="d-flex align-center flex-wrap ga-1 ga-sm-2">
    <v-text-field
        v-model="search"
        placeholder="Track, Artist or Album"
        clearable
        rounded="sm"

        flat
        :min-width="300"
    >
      <template #append-inner>
        <v-btn icon="mdi-magnify" variant="text" rounded="sm" @click="emit('search', search)"></v-btn>
      </template>
    </v-text-field>
    <v-select
        v-model="session.entity"
        :items="[
          { title: 'All', value: '' },
          { title: 'Track', value: 'song' },
          { title: 'Artist', value: 'musicArtist' },
          { title: 'Album', value: 'album' },
        ]"

        :min-width="100"
    >
    </v-select>
    <slot></slot>
  </v-form>
</template>