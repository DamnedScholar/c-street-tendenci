import { Controller } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'

// TODO: Figure this out.
import {html, render} from 'lit-html'
import {LitElement, html as ehtml, property, css} from 'lit-element'
import {styleMap} from 'lit-html/directives/style-map.js'
import {Panel} from 'blackstone-ui/index.js'

// Tab bar documentation at https://bui.js.org/#/presenters
import Tabs from 'blackstone-ui/presenters/tabs/index.js'
// This import shouldn't be touched because even though it seems unused, it defines the custom element for `b-tabs`.

class Viewer extends LitElement {
  static get styles() { return css`
    iframe {
      width: 100%;
      height: 100%;
    }
  ` }

  static get properties() { return {
    item: {attribute: false},
    loading: {attribute: false},
    display: {attribute: false},
    sniffers: {attribute: false, type: Array}
  }}

  @property({attribute: true, type: String, reflect: true})
  current = ''
  @property({attribute: true, type: Array, reflect: true})
  links = []

  constructor() {
    super()

    // Set defaults. Nothing dynamic should go here.
    this.sniffers = []

    this.loading = ehtml`
      Loading...
    `

    this.css = {
      viewer: {
        "display": "flex",
        "flex-direction": "column-reverse"
      },
      tabs: {
        "height": "100%"
      },
      topbar: {
        "height": "200px",
        "display": "flex"
      }
    }

    // TODO: I can make forward/back buttons in b-ui's tab bar using the `.views` property (https://github.com/kjantzer/bui/blob/master/presenters/tabs/index.js#L83) and `tab_bar.views.active` with `tab_bar.views.at(active + 1)` or `(active - 1)`. I need to bind these to hotkeys using `stimulus-hotkeys` and to buttons that appear on mobile devices.
  }

  // attributeChangedCallback(name, oldval, newval) {
  //   console.log('attribute change: ', name, newval);
  //   super.attributeChangedCallback(name, oldval, newval);
  // }

  updateTab(evt) {
    // var content = ""
    var view = evt.target

    // Save a reference to each sniffer for later.
    this.sniffers.push( setInterval( (view) => {
      var tab = view.parentElement.nextElementSibling
      var content = ""

      try {
        content = view.contentDocument.title.replace(this.croptitle, "")
      }
      catch {
        // Do nothing.
      }
      
      render(content ? html`${content}` : html`No Title Found`, tab)
    }, 100, view) )
  }

  clone(node) {
    var newNode = node.cloneNode(true)
  }

  render() {
    this.item = (link, id) => ehtml`
      <section title="view-${id}">
        <iframe style="height: 500px" src="${link}" frameborder="0"
          @load="${ (evt) => this.updateTab(evt) }"
        ></iframe>
      </section>
      <span slot="menu:view-${id}">${this.loading}</span>
    `

    this.display = ehtml`
      <viewer style=${styleMap(this.css.viewer)}>
        <b-tabs style=${styleMap(this.css.tabs)} layout="left">
          ${this.links.map( (v, i) => this.item(v, i) )}
        </b-tabs>
        <topbar style=${styleMap(this.css.topbar)}>
          ${this.controller.topbarTargets.map( (t) => {
            var newNode = t.cloneNode(true)
            newNode.style = window.getComputedStyle(t)

            return newNode
          } )}
        </topbar>
      </viewer>
    `

    return ehtml`${this.display}`
  }

  // Build an API for the different organs of this component.
  //    viewer -> The top-level wrapper.
  //    views -> Nodelist of all views
  //    sidebar -> Element containing the sidebar content.
  //    topbar -> Element containing the topbar content.
  get viewer() {
    return this.shadowRoot.querySelector('viewer')
  }

  get views() {
    return this.shadowRoot.querySelectorAll('section')
  }

  get sidebar() {
    return this.shadowRoot.querySelector('sidebar')
  }

  get topbar() {
    return this.shadowRoot.querySelector('topbar')
  }
}
// Jeff from Downtown Springfield Association 234-1022
export default class extends Controller {
  static targets = ['link', 'display', 'topbar', 'sidebar']

  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    // StimulusReflex.register(this)

    // TODO: Based on a list of links passed through HTML, load several iframes into the DOM without displaying them to the user (`visibility: hidden` in CSS; avoid Tailwind since this CSS will be entirely controlled by JS). When each iframe is loaded (https://stackoverflow.com/a/21471494), make a record of its title (if it's an HTML page) and maybe other important information.

    // Need to convert the single-quotes string in the data attribute to a double-quotes string for JSON compatibility.
    const links = this.data.get("links").replaceAll('\'', '\"')
    this.links = links ? JSON.parse(links) : []

    this.current = this.linkTarget.getAttribute("href")
    this.linkTarget.setAttribute("href", "#")
    this.linkTarget.style.color = "red"

    customElements.define('d-viewer', Viewer)

    // For reference on the following, see this documentation:
    // https://github.com/kjantzer/bui/tree/master/presenters/panel#panel

    this.panelOpts = {
      type: "modal",
      anchor: "center",
      height: "95vh",
      width: "90vw",
      closeBtn: false,
      closeOnEsc: true,
    }

    this.frame = new Panel(
      'd-viewer', this.panelOpts
    )
    this.viewer = this.frame.view
    this.viewer.controller = this
    this.viewer.setAttribute("links", JSON.stringify(this.links) )
    this.viewer.setAttribute("current", JSON.stringify(this.current) )
    this.viewer.classList.add('w-full', 'h-full')

    this.viewer.croptitle = this.data.get("croptitle")

    console.log(this.frame)
    // this.frame = new Panel( () => html`this.display`, this.panelOpts )

    console.log(this)
  }

  open_viewer() {
    this.frame.open()
  }
}
