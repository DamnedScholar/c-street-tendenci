const webpack = require('webpack');
const glob = require('glob');


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

const config = {
    mode: process.env.NODE_ENV,
    entry: entryObj,
    output: {
        path: __dirname + '/static/js',
        filename: '[name].js'
    },
    optimization: {
        minimize: false
    },
    resolve: {
        alias: {
            "jquery": "blackstone-ui/helpers/backbone/jquery-shim"
        }
    },
    module: {
        rules: [
            {
                test: /\.less$/,
                loader: 'less-loader', // compiles Less to CSS
            },
            {
                test: /_controller\.js/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            '@babel/preset-env'
                        ],
                        plugins: [
                            '@babel/plugin-proposal-class-properties'
                        ]
                    }
                }
              }
        ],
    }
}

module.exports = config
