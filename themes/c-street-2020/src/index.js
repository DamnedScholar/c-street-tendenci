// Importing styles
require('./styles/base.sass')

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

// For Webpack, we need to call Bootstrap for it to be included in the bundle
bs

// Application code
