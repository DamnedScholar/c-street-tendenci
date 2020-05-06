// Importing styles
require('./styles/base.sass')
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
jquery = $
window.jQuery = $
window.$ = $

// Application code
