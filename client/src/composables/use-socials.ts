import useCache from '@/composables/use-cache'
import { checkVersion } from '@/utils'

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

    onMounted(async () => checkVersion() && await cache.refresh())

    return socials
}

export default useSocials