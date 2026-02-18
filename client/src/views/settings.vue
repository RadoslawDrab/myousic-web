<script setup lang="ts">
import useData from '@/composables/use-data'

import Json from '@/components/utils/Json.vue'
import ListGroup from '@/components/utils/ListGroup.vue'
import useSave from '@/composables/use-save'

const { local } = useData()

const { draft: settings, save, reset, isChanged } = useSave(local)

definePage({
  meta: {
    breadcrumbs: 'Settings'
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
  <Json v-model="settings" v-model:previous="local" class="bg-transparent" card-title="" content-class="pa-0" :max-content-height="10" show-diff />
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
          <v-number-input v-model="settings.artworkSize" variant="solo-filled" label="Artwork Size" :min="250" :max="2000" :step="50" hide-details></v-number-input>
          <v-textarea v-model="settings.defaultComment" variant="solo-filled" label="Default Comment" placeholder="E.g. [URL: {{ url }}]" :rows="2" auto-grow hide-details persistent-placeholder></v-textarea>
        </Flex>
      </template>
    </ListGroup>
  </v-list>
</template>