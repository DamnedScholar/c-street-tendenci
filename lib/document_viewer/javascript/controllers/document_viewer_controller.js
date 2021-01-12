import { Controller } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'

import {html, render} from 'lit-html'
import {LitElement, html as ehtml, property, css} from 'lit-element'

import {Panel} from 'blackstone-ui/index.js'

// Tab bar documentation at https://bui.js.org/#/presenters
import 'blackstone-ui/presenters/tabs/index.js'
import 'blackstone-ui/presenters/tabs/app.js'
import 'blackstone-ui/presenters/tabs/app-tab-bar.js'
import 'blackstone-ui/elements/btn.js'
import device from 'blackstone-ui/util/device.js'

import DocumentViewer from '../components/viewer.js'


export default class extends Controller {
  static targets = ['link', 'display', 'topbar', 'sidebar']
  static values = {
    links: Array,
    current: String,
    croptitle: String
  }

  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    StimulusReflex.register(this)

    // Need to convert the single-quotes string in the data attribute to a double-quotes string for JSON compatibility.

    // TODO: Add support for full-page vs modal modes, determined by a data-attribute.

    customElements.define('document-viewer', DocumentViewer)

    console.log(this)

    // try {
    //   // This expression will return false if the controller was configured correctly, true if the element has a different idea of what its links need to be (we'll prefer the controller's worldview here since it is "closer" to the server), and an exception if `this.element.links` is undefined (which means `this.element` isn't the custom component we were looking for).
    //   console.log(this.element.links)
    //   if (this.element.links != this.linksValue)
    //     this.element.links = this.linksValue

    //   this.viewer = this.element
    //   console.log(this.element.links)
    // }
    // catch {
    //   // If `this.element` isn't the right custom element, fall back to grabbing control of the link target (which should exist).
    //   // TODO: Write logic against edge cases where `linkTarget` doesn't exist.
    //   this.linkTarget.setAttribute("href", "#")

    //   // For reference on the following, see this documentation:
    //   // https://github.com/kjantzer/bui/tree/master/presenters/panel#panel
    //   this.panelOpts = {
    //     type: "modal",
    //     anchor: "center",
    //     height: "95vh",
    //     width: "90vw",
    //     closeBtn: false,
    //     closeOnEsc: true,
    //   }

    //   this.frame = new Panel(
    //     'document-viewer', this.panelOpts
    //   )
    //   this.viewer = this.frame.view
    //   this.viewer.controller = this
    //   this.viewer.links = this.linksValue
    //   this.viewer.current = this.currentValue
    // }

    this.viewer = this.element // TODO: The viewer might not always be the element.

    // TODO: This feature should be expanded and made more intuitive.
    this.viewer.croptitle = this.croptitleValue
  }

  open_viewer() {
    this.frame.open()
  }
}
