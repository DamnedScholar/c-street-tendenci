import {html} from 'lit-element'

const styleTag = (href) => html`
    <link rel="stylesheet" type="text/css" href="${href}">
`

export const injectStyle = (query) => {
    var sheet = Array.from(
        document.styleSheets
    ).filter(
        // This is necessary because not all entries include a href.
        i => i.href
    ).filter(
        i => i.href.includes(query)
    )[0]
    
    return html`
        ${ sheet ?
            styleTag(sheet.href) :
            console.log(`Style Injector -> A stylesheet matching "${query}" was not found.`)
        }
    `
}
