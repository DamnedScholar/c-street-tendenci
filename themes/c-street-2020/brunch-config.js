exports.files = {
  stylesheets: { joinTo: 'media/css/tailwind.css' },
};

exports.paths = {
  watched: [ "src/styles-tw/" ]
}

exports.plugins = {
  postcss: {
    processors: [
      require('tailwindcss'),
      require('autoprefixer')(['last 8 versions']),
      require('cssnano')()
    ]
  }
};

// exports.npm = {
//   globals: {
//     jQuery: 'jquery',
//     $: 'jquery',
//     bootstrap: 'bootstrap',
//   }
// };
