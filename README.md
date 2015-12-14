# lektor-webpack-support

This is a plugin for Lektor that adds support for webpack to projects.  When
enabled it can build a webpack project from the `webpack/` folder into the
asset folder automatically when the server (or build process) is run with
the `-f webpack` flag.

## Enabling the Plugin

To enable the plugin add this to your project file:

```ini
[packages]
lektor-webpack-support = 0.1
```

## Creating a Webpack Project

Next you need to create a webpack project in the `webpack/` folder.  You
will need a `package.json` as well as a `webpack.config.js`

### `webpack/package.json`

This file instructs `npm` which packages we will need.  All we need for a
start is to create an almost empty file:

```json
{
  "private": true
}
```

Now we can npm install the rest:

```
$ npm install --save-dev webpack babel-core node-sass babel-loader sass-loader css-loader url-loader style-loader file-loader
```

This will install webpack itself together with babel and sass as well as
a bunch of loaders we need for getting all that configured.  Because we
created a `package.json` before and we use `--save-dev` the dependencies
will be remembered in the `package.json` file.

### `webpack/webpack.config.js`

Next up is the webpack config file.  Here we will go with a very basic
setup that's good enough to cover most things you will encounter.  The
idea is to build the files from `webpack/scss` and `webpack/js` into
`assets/static/gen` so that we can use it even if we do not have webpack
installed for as long as someone else ran it before.

```javascript
var webpack = require('webpack');
var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');


var options = {
  entry: {
    'app': './js/main.js',
    'styles': './scss/main.scss'
  },
  output: {
    path: path.dirname(__dirname) + '/assets/static/gen',
    filename: '[name].js'
  },
  devtool: '#cheap-module-source-map',
  resolve: {
    modulesDirectories: ['node_modules'],
    extensions: ['', '.js']
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader!sass-loader')
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
      },
      {
        test: /\.woff2?$|\.ttf$|\.eot$|\.svg$|\.png|\.jpe?g\|\.gif$/,
        loader: 'file'
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin('styles.css', {
      allChunks: true
    }),
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.optimize.DedupePlugin()
  ]
};

module.exports = options;
```

## Creating the App

Now we can start building our app.  We configured at least two files
in webpack: `js/main.js` and `scss/main.scss`.  Those are the entry
points we need to have.  You can create them as empty files in
`webpack/js/main.js` and `webpack/scss/main.scss`.

## Running the Server

Now you're ready to go.  When you run `lektor server` webpack will not
run, instead you need to now run it as `lektor server -f webpack` which
will enable the webpack build.  Webpack automatically builds your files
into `assets/static/gen` and this is where Lektor will then pick up the
files.  This is done so that you can ship the webpack generated assets
to others that do not have webpack installed which simplifies using a
Lektor website that uses webpack.

## Manual Builds

To manually trigger a build that also invokes webpack you can use
`lektor build -f webpack`.

## Including The Files

Now you need to include the files in your template.  This will do it:

```html
<link rel="stylesheet" href="{{ '/static/gen/styles.css'|asseturl }}">
<script type=text/javascript src="{{ '/static/gen/app.js'|asseturl }}" charset="utf-8"></script>
```
