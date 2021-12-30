const ax = axios.create({
    baseURL: 'http://localhost:8000/',
    timeout: 1000,
    headers: {'X-Axios-Header': 1}
});

const target = document.getElementById('equipment-list')


async function getPartial(url) {
    let response = await ax.get(url)
    let div = document.createElement('div')
    div.innerHTML = response.data.trim()
    return div.firstChild
}

async function appendChildEnd(url) {
    let element = await getPartial(url)
    target.appendChild(element)
}