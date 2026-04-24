<script setup lang="ts" generic="T">
  const itemsPerPage = defineModel<number>('itemsPerPage', { default: 10 })
  const page = defineModel<number>('page', { default: 0 })
  const props = withDefaults(defineProps<{
    items: T[],
    availableItemsPerPage?: (number | 'all')[]
  }>(), {
    availableItemsPerPage: () => [10, 25, 50, 100, 'all']
  })

  const pageCount = computed(() => Math.ceil(props.items.length / itemsPerPage.value))

  watch(() => props.items.length, () => {
    page.value = 1
  })
</script>

<template>
  <Flex align="center" gap="5">
    <Flex align="center">
      <span>Items per page:</span>
      <v-select v-model:model-value="itemsPerPage" :items="[10, 25, 50, 100, { value: props.items.length, title: 'All' }]" density="compact"></v-select>
    </Flex>
    <span class="d-flex align-center">{{ page }}-{{ Math.min(page + itemsPerPage - 1, items.length) }} of {{ items.length }}</span>
    <v-pagination v-model="page" :length="pageCount" show-first-last-page></v-pagination>
  </Flex>
</template>