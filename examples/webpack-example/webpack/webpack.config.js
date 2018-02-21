const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const webpack = require('webpack');

const extractPlugin = new ExtractTextPlugin({ filename: 'styles.css' });

const config = {

  context: path.resolve(__dirname),

  entry: {
    app: './js/main.js',
    styles: './scss/main.scss'
  },

  output: {
    path: path.dirname(__dirname) + '/assets/static/gen',
    filename: '[name].js'
  },

  module: {
    rules: [

      //babel-loader
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ['env']
          }
        }
      },

      //sass-loader
      {
        test: /\.scss$/,
        use: extractPlugin.extract({
          use: [
            {
              loader: 'css-loader',
              options: {
                sourceMap: true
              }
            },
            {
              loader: 'sass-loader',
              options: {
                sourceMap: true
              }
            }
          ],
          fallback: 'style-loader'
        })
      }

    ]
  },

  plugins: [
    extractPlugin
  ],

  devtool: 'inline-source-map'
 
}

module.exports = config;
