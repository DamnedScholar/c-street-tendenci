import {html, render} from 'lit-html'
import {html as html2, render as render2} from 'https://cdn.skypack.dev/lit-html'
import {LitElement, html as ehtml} from 'lit-element'
import {LitElement as LitElement2, html as ehtml2} from 'https://cdn.skypack.dev/lit-element'

const litE = ehtml`Lit-Element!`
const litE2 = ehtml2`Lit-Element!`
const litH = html`Lit-HTML~`
const litH2 = html2`Lit-HTML~`

class LitExample extends LitElement {
    get content() {
        return this.classList.contains('lit-element-content') ?
        litE : litH
    }
    
    render() {
        return ehtml`${this.content}`
    }
}

customElements.define('lit-example', LitExample)

class LitExample2 extends LitElement2 {
    get content() {
      return this.classList.contains('lit-element-content') ?
         litE2 : litH2
    }
    
    render() {
      return ehtml2`${this.content}`
    }
}

customElements.define('lit-example2', LitExample2)

Array.from(document.querySelectorAll('section')).map( element => {
    var content = element.classList.contains('lit-element-content') ?
        litE : litH
    
    render(content, element)
})

Array.from(document.querySelectorAll('div')).map( element => {
    var content = element.classList.contains('lit-element-content') ?
        litE2 : litH2
    
    render2(content, element)
})

