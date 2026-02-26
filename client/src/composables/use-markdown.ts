import { marked } from 'marked'
import mermaid from 'mermaid'

mermaid.initialize({
    startOnLoad: true,
    securityLevel: 'loose',
    theme: 'dark'
})

const useMarkdown = (initialValue: string = '') => {
	const text = ref<string>(initialValue)
    const html = ref<string>('')
    const isRendering = ref<boolean>(false)

    function getRenderer() {
        const renderer = new marked.Renderer({
            gfm: true,
            breaks: true
        })

        renderer.code = ({ text, lang }) => {
            if (lang === 'mermaid') {
                return `<pre class="mermaid">${text}</pre>`
            }

            return `<pre><code class="language-${lang}">${text}</code></pre>`
        }

        return renderer
    }

    async function render() {
        if (!text.value) {
            html.value = ''
            return
        }

        isRendering.value = true
        try {
            // 1. Convert Markdown to HTML string
            html.value = await marked.parse(text.value, {
                renderer: getRenderer()
            })

            // 2. Wait for Vue to update the DOM
            await nextTick()

            // 3. Trigger Mermaid to process the newly injected <pre class="mermaid">
            await mermaid.run({
                nodes: document.querySelectorAll('.mermaid')
            })
        } catch (e) {
            console.error('Markdown/Mermaid Render Error:', e)
        } finally {
            isRendering.value = false
        }
    }

    // Re-render whenever text changes
    watch(text, () => render(), { immediate: true })

    return {
        text,
        html,
        isRendering,
        render
    }
}

export default useMarkdown