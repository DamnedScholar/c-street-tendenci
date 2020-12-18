import {html} from 'lit-element'

const scriptTag = (id, src) => html`
    <script id=${id} src="${src}">
`

export const injectScript = (query) => {
    var script = document.scripts[query]
    
    return html`
        ${ script ?
            scriptTag(query, script.src) :
            console.log(`Script Injector -> A script matching "${query}" was not found.`)
        }
    `
}
