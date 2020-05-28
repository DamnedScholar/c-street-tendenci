// Importing styles
require('./styles-bs/base.sass')
// require('./styles-tw/out/tailwind.css?tailwind')

// Importing Focuspoint
require('jquery-focuspoint')

// For Bootstrap compatibility, jQuery needs to be attached to `window`
// jquery = $
// window.jQuery = $
// window.$ = $

// Start bootstrap

bs

// Start StimulusJS
import { Application, Controller } from "stimulus"
import ImageGrid from 'stimulus-image-grid'
import { definitionsFromContext } from "stimulus/webpack-helpers"

const application = Application.start();
const context = require.context("./controllers", true, /.js$/);
application.load(definitionsFromContext(context));

// Import stimulus-image-grid
application.register('image-grid', ImageGrid)

// Import and register all TailwindCSS Components
// import { Dropdown } from "tailwindcss-stimulus-components"
// application.register('dropdown', Dropdown)
// import { Dropdown, Modal, Tabs, Popover, Toggle } from "tailwindcss-stimulus-components"
// application.register('dropdown', Dropdown)
// application.register('modal', Modal)
// application.register('tabs', Tabs)
// application.register('popover', Popover)
// application.register('toggle', Toggle)
application.register('dropdown', class extends Controller {
  static targets = ['menu']

  connect() {
    this.element[this.identifier] = this
    this.toggleClass = this.data.get('class') || 'hidden'
    console.log("-> Dropdown activated to toggle " + this.toggleClass)
  }

  toggle() {
    this.menuTarget.classList.toggle(this.toggleClass)
    console.log("-> Dropdown toggled.")
  }

  hide(event) {
    if (
      this.element.contains(event.target) === false &&
      !this.menuTarget.classList.contains(this.toggleClass)
    ) {
      this.menuTarget.classList.add(this.toggleClass)
    }
  }
})

// Application code
