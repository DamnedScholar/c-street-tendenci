import { Controller } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'

import {html, render} from 'https://unpkg.com/lit-html?module'
import {LitElement, html as ehtml, property, css} from 'https://unpkg.com/lit-element?module'

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

  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    StimulusReflex.register(this)

    // Need to convert the single-quotes string in the data attribute to a double-quotes string for JSON compatibility.
    var links = this.data.get("links")
    this.links = links ? JSON.parse(links.replaceAll('\'', '\"')) : []

    // TODO: Add support for full-page vs modal modes, determined by a data-attribute.

    this.current = this.linkTarget.getAttribute("href")
    this.linkTarget.setAttribute("href", "#")

    customElements.define('document-viewer', DocumentViewer)

    console.log("Viewer connected.")

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
      'document-viewer', this.panelOpts
    )
    this.viewer = this.frame.view
    this.viewer.controller = this
    this.viewer.links = this.links
    this.viewer.current = this.current

    // TODO: This feature should be expanded and made more intuitive.
    this.viewer.croptitle = this.data.get("croptitle")
  }

  open_viewer() {
    this.frame.open()
  }
}
