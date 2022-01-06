const target = document.getElementById('equipment-list')

class InvalidURLError extends Error {
    constructor(message, options) {
        super(message, options);
    }
}

class axiosClient {
    ax: axios;

    constructor() {
        this.ax = axios.create({
            baseURL: 'http://localhost:8000/',
            timeout: 1000,
            headers: {'X-Axios-Header': 1, 'X-CSRFToken': csrfToken}
        });
    }

    async appendChildEnd(url) {
        let element = await getPartial(url)
        target.appendChild(element)
    }

    async getPartial(url): HTMLElement {
        if (!this.URLIsValid(url)) {
            throw InvalidURLError(`${url} is not a valid url.`)
        }
        let response = await ax.get(url)
        let div = document.createElement('div')
        div.innerHTML = response.data.trim()
        return div.firstChild
    }

    URLIsValid(url): boolean {
    }
}
