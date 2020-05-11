const webpack = require('webpack')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
  mode: "production",
  entry: "./src/index.js",
  output: {
    path: __dirname + '/media/js',
    filename: "[name].js"
  },
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
          presets: ['@babel/preset-env'],
          plugins: ['@babel/plugin-proposal-class-properties']
        }
      }
    },
    // {
    //   test: /\.s[a]ss$/i,
    //   resourceQuery: /tailwind/,
    //   use: [
    //     {
    //       loader: MiniCssExtractPlugin.loader,
    //       options: {
    //         publicPath: '../css/',
    //       },
    //     },
    //     {
    //       loader: 'css-loader',
    //       // options: { importLoaders: 1 }
    //     },
    //     {
    //       loader: 'postcss-loader',
    //       options: {
    //         ident: 'postcss',
    //         plugins: [
    //           require('postcss-import'),
    //           require('tailwindcss'),
    //           require('autoprefixer'),
    //         ],
    //       }
    //     },
    //     'sass-loader'
    //   ]
    // },
    {
      test: /\.s[a]ss$/i,
      type: 'asset/resource',
      use: [
        "sass-loader"
      ],
      generator: {
        filename: '../css/[name].css'
      }
    },
    {
      test: /heroes\/.*\.(jpe?g|png)$/i,
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
    new MiniCssExtractPlugin(),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      _: 'lodash',
      bs: 'bootstrap',
      fa: '@fortawesome/fontawesome-pro'
    })
  ],
  resolve: {
    alias: {
      "popper.js": "@popperjs/core"
    }
  },
  externals: {
    // jquery: 'jQuery'
  }
}
