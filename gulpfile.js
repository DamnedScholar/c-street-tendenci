// This is being used specifically for auto-building Tailwind, since Webpack wasn't cooperating.

var gulp = require('gulp');
var browserSync = require('browser-sync').create();
var exec = require('child_process').exec;

// Build CSS
function tailwind(cb) {
  exec('cd themes/c-street-2020 && npm run tw')

  cb()
}

// Start static server
function browsersync() {
  browserSync.init({
    server: {
      baseDir: "./"
    }
  });
}

exports.tw = function() {
  gulp.series(tailwind)
}
exports.default = function() {
  gulp.watch(
    ['themes/c-street-2020/src/styles-tw/tailwind.css'], gulp.series(tailwind, browsersync)
  )
}
