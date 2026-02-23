<script setup lang="ts" generic="T extends RecursiveObject<{}>">

const props = withDefaults(defineProps<{
  items: T[]
  indent?: number
  parent?: T
}>(), {
  indent: 0
})
</script>

<template>
  <template v-for="(item, index) in props.items">
    <slot :item="item" :indent="props.indent" :parent="props.parent" :index="index"></slot>
    <RecursiveListItem
        v-if="item.children && item.children.length > 0"
        :parent="item"
        :items="item.children"
        :indent="props.indent + 1"
        v-slot="{ item: childrenItem, indent, parent, index }">
      <slot :item="childrenItem" :indent="indent" :parent="parent" :index="index"></slot>
    </RecursiveListItem>
  </template>
</template>