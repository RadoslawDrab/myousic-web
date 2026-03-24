import useCache from '@/composables/use-cache'

const useSocials = () => {
    const cache = useCache(computed(() => '/data/social.json'))
    const socials = ref<Social[]>([])
    watch(cache.data, (data) => {
        try {
            socials.value = JSON.parse(data)
        } catch (e) {
            console.error(e)
        }
    })

    return socials
}

export default useSocials