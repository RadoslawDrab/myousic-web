<script setup lang="ts">
import Json from '@/components/utils/Json.vue'
import useData from '@/composables/use-data'
import ListGroup from '@/components/utils/ListGroup.vue'

const open = ref<boolean>(false)

const sessionData = useData()

const settings = computed({
  get: () => sessionData.value.settings,
  set: (value) => sessionData.value.settings = value
})


</script>

<template>
  <v-fab icon="mdi-cog" app location="bottom right" @click="open = !open">
    <v-icon icon="mdi-cog"></v-icon>
  </v-fab>
  <v-navigation-drawer v-model="open" class="pa-3" location="right" width="600" max-height="100vh">
    <template #prepend>
      <span class="text-h6">Settings</span>
      <v-divider />
    </template>
    <v-list class="d-flex flex-column ga-2">
      <ListGroup title="Lyrics" group-class="border" group-content-class="pa-4 border-t d-flex flex-column ga-4">
        <template #group>
          <Flex column :gap="2">
            <span>Lyrics Provider Order</span>
            <ListSorting v-model="settings.lyricsProviders" />
          </Flex>
          <Flex column :gap="2">
            <span>Lyrics Modifier</span>
            <ObjectModifier v-model="settings.lyricsModifier" class="border" key-placeholder="RegEx or string" value-placeholder="Replacement" />
          </Flex>
<!--          <Flex column :gap="2">-->
<!--            <span>Lyrics URL Modifier</span>-->
<!--            <ListGroup title="Title" group-class="border" group-content-class="border-t">-->
<!--              <template #group>-->
<!--                <ObjectModifier v-model="settings.lyricsUrlModifiers.title" key-placeholder="RegEx or string" value-placeholder="Replacement" />-->
<!--              </template>-->
<!--            </ListGroup>-->
<!--            <ListGroup title="Artist" group-class="border" group-content-class="border-t">-->
<!--              <template #group>-->
<!--                <ObjectModifier v-model="settings.lyricsUrlModifiers.artist" key-placeholder="RegEx or string" value-placeholder="Replacement" />-->
<!--              </template>-->
<!--            </ListGroup>-->
<!--          </Flex>-->
        </template>
      </ListGroup>
      <ListGroup title="Genres" group-class="border" group-content-class="pa-4 border-t d-flex flex-column ga-4">
        <template #group>
<!--          <Flex column :gap="2">-->
<!--            <span>Genres Order</span>-->
<!--            <ListSorting v-model="settings.genresProviders" />-->
<!--          </Flex>-->
<!--          <Flex column :gap="2">-->
<!--            <span>Genres URL Modifier</span>-->
<!--            <ListGroup title="Title" group-class="border" group-content-class="border-t">-->
<!--              <template #group>-->
<!--                <ObjectModifier v-model="settings.genresUrlModifiers.title" key-placeholder="RegEx or string" value-placeholder="Replacement" />-->
<!--              </template>-->
<!--            </ListGroup>-->
<!--            <ListGroup title="Artist" group-class="border" group-content-class="border-t">-->
<!--              <template #group>-->
<!--                <ObjectModifier v-model="settings.genresUrlModifiers.artist" key-placeholder="RegEx or string" value-placeholder="Replacement" />-->
<!--              </template>-->
<!--            </ListGroup>-->
<!--          </Flex>-->
          <Flex column :gap="2">
            <span>Included Genres</span>
            <ObjectModifier v-model="settings.includedGenres" class="border" key-placeholder="RegEx or string" value-placeholder="Replacement" />
          </Flex>
          <Flex column :gap="2">
            <span>Excluded Genres</span>
            <ObjectModifier v-model="settings.excludedGenres" class="border" key-placeholder="RegEx or string" value-placeholder="Replacement" />
          </Flex>
        </template>
      </ListGroup>
      <ListGroup title="Download" group-class="border" group-content-class="pa-4 border-t">
        <template #group>
          <v-number-input v-model="settings.artworkSize" variant="plain" label="Artwork Size" :min="250" :max="2000" :step="50" hide-details></v-number-input>
        </template>
      </ListGroup>
    </v-list>
    <Json v-model="settings" />
  </v-navigation-drawer>
</template>