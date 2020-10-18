const webpack = require('webpack');
const glob = require('glob');
const TerserPlugin = require('terser-webpack-plugin')


let globOptions = {
    ignore: ['node_modules/**', 'venv/**']
}

let entryFiles = glob.sync("**/javascript/*.js", globOptions)

let entryObj = {};
entryFiles.forEach(function(file){
    if (file.includes('.')) {
        let parts = file.split('/')
        let path = parts.pop()
        let fileName = path.split('.')[0];
        entryObj[fileName] = `./${file}`;
    }
});

const optimize = {
    production: {
        usedExports: true,
        minimize: true
    },
    development: {
        minimize: false
    }
}

// const mode = 'production'
const mode = 'development'

// const babel = {
//     presets: [
//         '@babel/preset-env'
//     ],
//     plugins: [
//         '@babel/plugin-proposal-class-properties'
//     ]
// }

// https://medium.com/@craigmiller160/how-to-fully-optimize-webpack-4-tree-shaking-405e1c76038

const babel = {
    env: {
        development: {
            presets: [
                '@babel/preset-env'
            ]
        },
        production: {
            presets: [
                '@babel/preset-env'
            ]
        }
    },
    plugins: [
        '@babel/plugin-proposal-class-properties'
    ]
}



const config = {
    // mode: process.env.NODE_ENV,
    mode: mode,
    entry: entryObj,
    output: {
        path: __dirname + '/static/js',
        filename: '[name].js'
    },
    optimization: optimize[mode],
    resolve: {
        alias: {
            "jquery": "blackstone-ui/helpers/backbone/jquery-shim"
        }
    },
    module: {
        rules: [
            {
                test: /\.less$/,
                use: [ 
                    'style-loader',
                    'css-loader', 
                    'less-loader'
                ]
            },
            {
                test: /\.svg(\.html)?$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: "[name].[ext]",
                        outputPath: 'images',
                        publicPath: '/js/'
                    }
                },
            },
            {
                test: /_controller\.js/,
                use: {
                    loader: 'babel-loader',
                    options: babel
                }
              }
        ],
    }
}

module.exports = config
