import { Controller } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
import {html, render} from 'lit-html'
import {styleMap} from 'lit-html/directives/style-map.js'

export default class extends Controller {
  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    // StimulusReflex.register(this)

    // TODO: Based on a list of links passed through HTML, load several iframes into the DOM without displaying them to the user (`visibility: hidden` in CSS; avoid Tailwind since this CSS will be entirely controlled by JS). When each iframe is loaded (https://stackoverflow.com/a/21471494), make a record of its title (if it's an HTML page) and maybe other important information.

    this.container = document.createElement("div")
    document.body.prepend(this.container)

    this.styles = {
      overlay: {
        height: "100vh",
        width: "100vw",
        backgroundColor: "rgba(0, 0, 0, 0.5)"
      }
    }

    this.links = [
      "https://eclectic-co.com",
      "https://pinboard.com"
    ]
    
    this.current = "https://eclectic-co.com"

    this.display = html`
      <div style=${styleMap(this.styles.overlay)}>
        <div style=${styleMap(this.styles.viewer)}>
          <nav></nav>
          <div>
            ${this.links.map( (link) => {
              // TODO: Is there a convenient way to programmatically set up a two-way reference between the button element and a particular viewer element? I need to have each viewer set the button's name once it loads, and for each button to know which viewer to recall, but I don't want to use unique IDs to find them because there could conceivably be more than one viewer controller on a page. I could embed and search for the URL or a hash of it. Each link should be a <button> that updates `current` and the rendered template should display `current` and hide the others, possibly by setting their height to 0px. It might even be a good idea to render all of the iframes at 0px inside their nav bar buttons and then have the viewer frame copy whichever is active. Or maybe the iframe is positioned as overflow at the end of the button element, and the button with `overflow: visible` is the current one.
            })}
          </div>
        </div>
      </div>
    `
  }

  open_viewer() {
    // TODO: Create a lightbox-style modal overlay for the whole window with a panel displaying the requested document (the one in the `href` attribute on the link) and a panel of links to the other URIs passed in the context.
  }
}
