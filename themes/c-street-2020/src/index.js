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
window.jQuery = $;
window.$ = $;

// Focuspoint adds features to jQuery's $, so it needs to follow that.
require('jquery-focuspoint')

// For Webpack, we need to call Bootstrap for it to be included in the bundle
bs

// Application code
