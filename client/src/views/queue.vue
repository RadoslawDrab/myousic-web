<script setup lang="ts">
  import useApi from '@/composables/use-api'
  import useFetch from '@/composables/use-fetch'
  import useStatus from '@/composables/use-status'
  import { getTime } from '@/utils'
  import { useRouteQuery } from '@vueuse/router'

  const { getQueueStatus, downloadTrack } = useApi()
  const status = useStatus()
  const queryStatus = useRouteQuery<'all' | 'completed' | 'pending' | 'failed'>('status', 'all')
  const { delete: _deleteJob } = useFetch({ path: ['queue']})

  const items = ref<QueueItem[]>([])
  const currentItem = ref<QueueItem | null>(null)
  const search = ref<string>('')
  const isLoading = ref<boolean>(false)

  const allHeaders = ref<DataTableHeader[]>([
    { key: 'data.artworkUrl', title: 'Artwork' },
    { key: 'data.track.artistName', title: 'Artist Name' },
    { key: 'data.track.trackName', title: 'Track Name' },
    { key: 'data.track.collectionName', title: 'Album', defaultShow: false },
    { key: 'data.track.clipping', title: 'Clipping', defaultShow: false },
    { key: 'status', title: 'Status', removable: false },
    { key: 'data.error', title: 'Error', defaultShow: false },
    { key: 'finished', title: 'Finished' },
    { key: 'createdAt', title: 'Created At' },
    { key: 'availableTo', title: 'Available To' },
    { key: 'updatedAt', title: 'Updated At', defaultShow: false },
    { key: 'actions', title: 'Actions', removable: false },
  ])
  const headers = ref(allHeaders.value)

  const filteredItems = computed(() => {
    const searchRegex = new RegExp(search.value, 'i')
    return items.value.filter(item => {
      return (
          search.value ?
              (
                  item.data?.track ? (
                    searchRegex.test(item.data.track.artistName) ||
                    searchRegex.test(item.data.track.trackName) ||
                    searchRegex.test(item.data.track.collectionName)
                  ) : false
              )
              : true
      ) && (
          queryStatus.value !== 'all' ?
              item.status.toLowerCase() === queryStatus.value.toLowerCase()
              : true
      )
    })
  })

  async function deleteJob(id: string) {
    isLoading.value = true
    try {
      await _deleteJob(null, { query: { id }})
      await refresh()
      status.add({ type: 'success', title: 'Job deleted', closable: true })
    } catch (e) {
      status.add({ type: 'error', title: e.toString() })
    } finally {
      isLoading.value = false
    }
  }
  async function refresh() {
    isLoading.value = true
    try {
      items.value = (await getQueueStatus()).reverse()
    } catch (e) {
      status.add({ type: 'error', title: e.toString() })
    } finally {
      isLoading.value = false
    }
  }

  onMounted(refresh)

  useIntervalFn(refresh, 10000)

  definePage({
    meta: {
      title: 'Queue',
      icon: 'mdi-playlist-music',
      includeInNav: true
    }
  })
</script>

<template>
  <v-data-table :headers="headers" :items="filteredItems" :loading="isLoading">
    <template #top>
      <v-toolbar class="border-b px-2" color="transparent">
        <v-text-field v-model="search" class="me-2" placeholder="String or RegEx" clearable>
          <template #prepend-inner>
            <v-icon icon="mdi-magnify"></v-icon>
          </template>
        </v-text-field>
        <v-select v-model="queryStatus" class="me-2" max-width="150" :items="['all', 'completed', 'pending', 'failed']"></v-select>
        <Flex align="center">
          <HeadersFilter ref="headerFilter" v-model="headers" v-model:all-headers="allHeaders"  />
          <v-btn icon="mdi-refresh" rounded="sm" @click="refresh"></v-btn>
        </Flex>
      </v-toolbar>
    </template>
    <template #item.actions="{ item }">
      <v-btn-group density="comfortable">
        <v-btn icon="mdi-download" variant="flat" :href="item.data.downloadUrl" :disabled="!item.data.downloadUrl && item.finished" v-tooltip="'Download'"></v-btn>
        <v-btn icon="mdi-restart" @click="downloadTrack(item.data.url, item.data.track).then(() =>refresh())" v-tooltip="'Restart'"></v-btn>
        <v-btn icon="mdi-link" variant="flat" :href="item.data.url" :disabled="!item.data.url" target="_blank" v-tooltip="'View URL'"></v-btn>
        <v-btn icon="mdi-code-json" @click="currentItem = item" v-tooltip="'View JSON'"></v-btn>
        <v-btn icon="mdi-close" @click="deleteJob(item.id)" v-tooltip="'Delete job'"></v-btn>
      </v-btn-group>
    </template>
    <template #item.data.artworkUrl="{ value }">
      <ArtworkImage :url="value" :small-render-size="400" :large-render-size="1000" />
    </template>
    <template #item.data.track.clipping="{ value }">
      <span v-if="value" class="text-grey">
        {{ getTime(value[0], true) }} - {{ getTime(value[1], true) }}
      </span>
    </template>
    <template #item.finished="{ value }">
      <v-icon :icon="value ? 'mdi-check' : 'mdi-close'"></v-icon>
    </template>
    <template #item.status="{ value }">
      <v-chip :color="value === 'completed' ? 'success' : value === 'failed' ? 'error': 'warning'" @click="queryStatus = value">{{ value }}</v-chip>
    </template>
    <template #item.createdAt="{ value }">
      <span v-if="value" class="text-grey">{{ new Date(value).toLocaleString() }}</span>
    </template>
    <template #item.updatedAt="{ value }">
      <span v-if="value" class="text-grey">{{ new Date(value).toLocaleString() }}</span>
    </template>
    <template #item.availableTo="{ value }">
      <span v-if="value" class="text-grey">{{ new Date(value).toLocaleString() }}</span>
    </template>
    <template #item.data.error="{ value }">
      <code v-if="value" class="text-red-darken-2">{{ value }}</code>
    </template>
  </v-data-table>
  <v-dialog v-model="currentItem" max-width="800">
    <Json v-model="currentItem">
      <template #appendActions>
        <v-btn prepend-icon="mdi-close" @click="currentItem = null">Close</v-btn>
      </template>
    </Json>
  </v-dialog>
</template>