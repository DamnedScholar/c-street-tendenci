import { Controller } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
import {html, render} from 'lit-html'
import {styleMap} from 'lit-html/directives/style-map.js'
import {Panel} from 'blackstone-ui'

// Tab bar documentation at https://bui.js.org/#/presenters
import Tabs from 'blackstone-ui/presenters/tabs'
// This import shouldn't be touched because even though it seems unused, it defines the custom element for `b-tabs`.


export default class extends Controller {
  static targets = ['link', 'display']

  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    // StimulusReflex.register(this)

    // TODO: Based on a list of links passed through HTML, load several iframes into the DOM without displaying them to the user (`visibility: hidden` in CSS; avoid Tailwind since this CSS will be entirely controlled by JS). When each iframe is loaded (https://stackoverflow.com/a/21471494), make a record of its title (if it's an HTML page) and maybe other important information.

    // Need to convert the single-quotes string in the data attribute to a double-quotes string for JSON compatibility.
    const links = this.data.get("links").replaceAll('\'', '\"')
    const empty = []
    this.links = links ? JSON.parse(links) : empty
    this.current = this.linkTarget.getAttribute("href")
    this.linkTarget.setAttribute("href", "#")

    this.loading = html`
      Loading...
    `
    
    this.item = (link) => html`
      <section title="${this.loading}" class="w-full border-1 m-1 py-4 px-2">
        <iframe class="w-0 h-0" src="${link}" frameborder="0"
          @load="${(evt) => evt.target.parentElement.setAttribute("title", "Video Loaded")}"
        ></iframe>
      </section>
    `

    this.display = html`
      <b-tabs name="viewer">
          ${this.links.map( (i) => this.item(i) )}
      </b-tabs>
    `

    // TODO: I can make forward/back buttons in b-ui's tab bar using the `.views` property (https://github.com/kjantzer/bui/blob/master/presenters/tabs/index.js#L83) and `tab_bar.views.active` with `tab_bar.views.at(active + 1)` or `(active - 1)`. I need to bind these to hotkeys using `stimulus-hotkeys` and to buttons that appear on mobile devices.

    // For reference on the following, see this documentation:
    // https://github.com/kjantzer/bui/tree/master/presenters/panel#panel

    this.panelOpts = {
      type: "modal",
      anchor: "center",
      height: "95vh",
      width: "90vw",
      closeBtn: true,
      closeOnEsc: true,
    }

    this.frame = new Panel( () => html`this.display`, this.panelOpts )

    console.log(this)
  }

  open_viewer() {
    this.frame.open()
  }

  changeDisplay(evt) {
    let content = evt.target.firstElementChild.cloneNode()
    content.removeAttribute('@load')
    content.classList.remove('w-0', 'h-0')
    content.classList.add('w-full', 'h-full')
    
    render(
      html`${content}`,
      this.frame.querySelector('[name="display"]')
    )
  }
}
