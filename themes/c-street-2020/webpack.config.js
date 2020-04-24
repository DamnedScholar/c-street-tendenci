const webpack = require('webpack')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

module.exports = {
  mode: "production",
  // entry: "./src/index.js",
  // output: {
  //   path: __dirname + '/dist',
  //   filename: "[name].js"
  // },
  experiments: {
    asset: true
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /node_modules/,
      use: {
        loader: "babel-loader",
        options: {
          presets: ['@babel/preset-env']
        }
      }
    },
    {
      test: /\.s[a]ss$/i,
      type: 'asset/resource',
      use: [
        "sass-loader"
      ],
      generator: {
        filename: '../media/css/[name].css'
      }
    },
    {
      test: /heroes\/\.(jpe?g|png)$/i,
      loader: 'responsive-loader',
      options: {
        outputPath: '../media/img/heroes/',
        name: '[name][ext]'
        // If you want to enable sharp support:
        // adapter: require('responsive-loader/sharp')
      }
    }
  ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new webpack.ProvidePlugin({
      // $: 'jquery',
      // jQuery: 'jquery',
      // _: 'lodash',
      // pop: 'popper',
      // bs: 'bootstrap',
      // fa: '@fortawesome/fontawesome-pro'
    })
  ],
  resolve: {
    alias: {
      "popper.js": "@popperjs/core"
    }
  }
}
