import { Controller } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'

// TODO: Figure this out.
import {html, render} from 'https://unpkg.com/lit-html?module'
import {LitElement, html as ehtml, property, css} from 'https://unpkg.com/lit-element?module'
import {styleMap} from 'https://unpkg.com/lit-html/directives/style-map.js?module'
import {Panel} from 'blackstone-ui/index.js'

// Tab bar documentation at https://bui.js.org/#/presenters
import Tabs from 'blackstone-ui/presenters/tabs/index.js'
// This import shouldn't be touched because even though it seems unused, it defines the custom element for `b-tabs`.

// console.log(styleMap()({
//   "display": "flex",
//   "flex-direction": "column-reverse"}))

class Viewer extends LitElement {
  static get properties() { return {
    // Trigger a redraw of the element if any of these building block properties change.
    item: {attribute: false},
    loading: {attribute: false},
    css: {attribute: false}
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
      // grid: {
        // TODO: Prototyping for a potential grid version.
        // "display": "grid",
        // "grid-template-areas": `
        //   "topbar topbar"
        //   "tabs body"
        //   "sidebar body"
        // `,
      // },
      tabs: {
        "height": "100%"
      },
      frame: {
        "height": "100%",
        "width": "100%"
      },
      topbar: {
        "height": "200px",
        "display": "flex",
        "justify-content": "space-around"
      }
    }

    // TODO: I can make forward/back buttons in b-ui's tab bar using the `.views` property (https://github.com/kjantzer/bui/blob/master/presenters/tabs/index.js#L83) and `tab_bar.views.active` with `tab_bar.views.at(active + 1)` or `(active - 1)`. I need to bind these to hotkeys using `stimulus-hotkeys` and to buttons that appear on mobile devices.
  }

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
    this.item = (link, id) => html`
      <section title="view-${id}">
        <iframe style="height: 500px" src="${link}" frameborder="0"
          @load="${ (evt) => this.updateTab(evt) }"
        ></iframe>
      </section>
      <span slot="menu:view-${id}">${this.loading}</span>
    `

    let display = html`
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

    return html`${display}`
  }

  // Build an API for the different organs of this component.
  //    viewer -> The top-level wrapper.
  //    views -> Nodelist of all views
  //    sidebar -> Element containing the sidebar content.
  //    topbar -> Element containing the topbar content.
  get viewer() {
    return this.shadowRoot.querySelector('viewer')
  }

  get content() {
    return this.shadowRoot.querySelector('b-tabs')
  }

  get sidebar() {
    return this.shadowRoot.querySelector('sidebar')
  }

  get topbar() {
    return this.shadowRoot.querySelector('topbar')
  }

  get keys() {
    // Return an array of all tab names.
    return Array.from(this.content.views.keys())
  }

  get active() {
    return this.content.active
  }

  set active(view) {
    this.content.active = view
  }

  // TODO: Test this!
  forward() {
    var len = this.keys.length
    var target = this.keys.indexOf(this.active) + 1
    this.active = this.keys[target%len]
  }

  back() {
    var len = this.keys.length
    var target = this.keys.indexOf(this.active) + len - 1
    this.active = this.keys[target%len]
  }
}

export default class extends Controller {
  static targets = ['link', 'display', 'topbar', 'sidebar']

  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    // StimulusReflex.register(this)

    // Need to convert the single-quotes string in the data attribute to a double-quotes string for JSON compatibility.
    var links = this.data.get("links").replaceAll('\'', '\"')
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
    this.viewer.links = this.links
    this.viewer.current = this.current

    this.viewer.croptitle = this.data.get("croptitle")
  }

  open_viewer() {
    this.frame.open()
  }
}
