
export function download(blobOrUrl: string | Blob) {
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = typeof blobOrUrl === 'string' ? blobOrUrl : URL.createObjectURL(blobOrUrl);

    document.body.appendChild(iframe);

    setTimeout(() => {
        document.body.removeChild(iframe);
        if (typeof blobOrUrl !== 'string') URL.revokeObjectURL(iframe.src);
    }, 1000);
}

export function getTime(time: number, milliseconds: boolean = false) {
    const date = new Date(time)

    return date.getMinutes().toString().padStart(2, '0') + ':' + date.getSeconds().toString().padStart(2, '0') + (milliseconds ? ':' + date.getMilliseconds().toString().padStart(3, '0') : '')
}

/**
 * @returns Returns true if version is different than saved one
 */
export function checkVersion(): boolean {
    const name = `${import.meta.env.CLIENT_APP_NAME || 'APP'}_VERSION`
    const savedVersion = localStorage.getItem(name)
    const version = import.meta.env.CLIENT_VERSION
    if (savedVersion !== version) {
        localStorage.setItem(name, version)
        return true
    }
    return false
}