<script setup lang="ts">
import useData from '@/composables/use-data'

import Json from '@/components/utils/Json.vue'
import ListGroup from '@/components/utils/ListGroup.vue'
import useSave from '@/composables/use-save'

const { local } = useData()

const { draft: settings, save, reset, isChanged } = useSave(local)


const sampleRates = computed(() => {
  switch (settings.value.audio.extension) {
    case 'mp3':
      return [33000, 44100, 48000]
    case 'm4a':
      return [44100, 48000, 96000]
    case 'opus':
      return [44100, 48000]
    default:
      return [44100, 48000, 96000, 128000, 192000]
  }
})

watch(() => settings.value.audio.extension, () => {
  settings.value.audio.sampleRate = Math.min(settings.value.audio.sampleRate, Math.max(...sampleRates.value))
}, { immediate: true })

definePage({
  meta: {
    title: 'Settings',
    icon: 'mdi-cog',
    includeInNav: true,
    order: 100
  }
})
</script>

<template>
  <Flex class="mb-2" align="center" justify="space-between" :gap="2">
    <span class="text-h5 text-sm-h4">Settings</span>
    <Flex :gap="2">
      <v-btn :disabled="!isChanged" prepend-icon="mdi-content-save" variant="tonal" color="success" flat @click="save">Save</v-btn>
      <v-btn :disabled="!isChanged" prepend-icon="mdi-restore" variant="tonal" color="error" flat @click="reset">Reset</v-btn>
    </Flex>
  </Flex>
  <Json
      v-model="settings"
      v-model:previous="local"
      class="bg-transparent"
      card-title=""
      content-class="pa-0"
      :max-content-height="10"
      show-diff
      export
      import

      @import="save()"
  />
  <v-list class="d-flex flex-column ga-2 bg-transparent">
    <ListGroup title="Lyrics" group-class="border" group-content-class="pa-4 border-t d-flex flex-column ga-4">
      <template #group>
        <Flex column :gap="2">
          <span>Lyrics Provider Order</span>
          <ListSorting v-model="settings.lyricsProviders" />
        </Flex>
        <Flex column :gap="2">
          <span>Lyrics Modifier</span>
          <ObjectModifier v-model="settings.lyricsModifier" class="border" key-placeholder="RegEx or string" value-placeholder="Replacement" save />
        </Flex>
      </template>
    </ListGroup>
    <ListGroup title="Genres" group-class="border" group-content-class="pa-4 border-t d-flex flex-column ga-4">
      <template #group>
        <Flex column :gap="2">
          <span>Included Genres</span>
          <ObjectModifier v-model="settings.includedGenres" class="border" key-placeholder="RegEx or string" value-placeholder="Replacement" save />
        </Flex>
        <Flex column :gap="2">
          <span>Excluded Genres</span>
          <ObjectModifier v-model="settings.excludedGenres" class="border" key-placeholder="RegEx or string" value-placeholder="Replacement" save />
        </Flex>
      </template>
    </ListGroup>
    <ListGroup title="Download" group-class="border" group-content-class="pa-4 border-t">
      <template #group>
        <Flex column :gap="2">
          <v-number-input v-model="settings.artworkSize" label="Artwork Size" :min="250" :max="2000" :step="50"></v-number-input>
          <v-select v-model="settings.audio.extension" label="Extension" :items="['m4a', 'mp3', 'wav', 'opus', 'flac']"></v-select>
          <v-select v-model="settings.audio.sampleRate" label="Sample Rate" :items="sampleRates.map(v => ({ title: ((v / 1000).toFixed(1).replace(/\.0$/, '')) + ' kHz', value: v }))"></v-select>
          <v-textarea v-model="settings.defaultComment" label="Default Comment" placeholder="E.g. [URL: {{ url }}]" :rows="2" auto-grow persistent-placeholder></v-textarea>
        </Flex>
      </template>
    </ListGroup>
  </v-list>
</template>