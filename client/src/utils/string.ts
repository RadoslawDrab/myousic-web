export function formatTitle(title: string) {
    return title ? `${title} | ${import.meta.env.CLIENT_APP_NAME || 'APP'}` : import.meta.env.CLIENT_APP_NAME || 'APP'
}

export function pascalCase(text: string | string[]) {
    return (Array.isArray(text) ? text : text.split(' '))
               .map(word => word.trim())
               .filter(word => word)
               .map(word => (word[0] || '').toUpperCase() + word.slice(1).toLowerCase())
               .join('')
}

export function joinClass(...classes: string[]) {
    return classes.filter(v => v).join(' ')
}