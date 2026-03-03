<script setup lang="ts">

const router = useRouter()

router.beforeEach((to, from, next) => {
  if (!/\/docs$/.exec(to.path)) return next()
  return next({ path: '/docs/introduction' })
})

definePage({
  meta: {
    title: 'Docs',
    icon: 'mdi-file-document',
    includeInNav: true,
    order: 100,
  }
})
</script>

<template>

</template>

<style scoped>

</style>