exports.files = {
  stylesheets: { joinTo: 'media/css/tailwind.css' },
};

exports.paths = {
  public: '.',
  watched: [
    "src/styles-tw/",
    "mock/index.html",
    "mock/files/"
  ]
}

exports.server = {
  run: true
}

exports.plugins = {
  postcss: {
    processors: [
      require('tailwindcss'),
      require('autoprefixer')(['last 8 versions']),
      // require('cssnano')()
    ]
  }
};

exports.hooks = {
  onCompile: function(generatedFiles, changedAssets) {
    JSON.stringify(generatedFiles)
    JSON.stringify(changedAssets)
  }
}

// exports.npm = {
//   globals: {
//     jQuery: 'jquery',
//     $: 'jquery',
//     bootstrap: 'bootstrap',
//   }
// };
