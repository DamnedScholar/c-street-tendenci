// Importing styles
require('./styles-bs/base.sass')
require('./styles/tailwind.sass')

// Importing JQuery and Lodash
// const $ = require('jquery')
// const jQuery = require('jquery')
// const _ = require('lodash')
//
// // Importing Bootstrap and FontAwesome
// const bs = require('bootstrap')
// const fa = require('@fortawesome/fontawesome-pro')

// For Bootstrap compatibility, jQuery needs to be attached to `window`
// jquery = $
// window.jQuery = $
// window.$ = $

// Start StimulusJS
import { Application } from "stimulus"
import { definitionsFromContext } from "stimulus/webpack-helpers"

const application = Application.start();
const context = require.context("./controllers", true, /.js$/);
application.load(definitionsFromContext(context));

// Import and register all TailwindCSS Components
// import { Dropdown, Modal, Tabs, Popover, Toggle } from "tailwindcss-stimulus-components"
// application.register('dropdown', Dropdown)
// application.register('modal', Modal)
// application.register('tabs', Tabs)
// application.register('popover', Popover)
// application.register('toggle', Toggle)

// Application code
