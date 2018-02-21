# lektor-webpack-support

[![Build Status](https://travis-ci.org/lektor/lektor-webpack-support.svg)](https://travis-ci.org/lektor/lektor-webpack-support) [![Code Coverage](https://codecov.io/gh/lektor/lektor-webpack-support/branch/master/graph/badge.svg)](https://codecov.io/gh/lektor/lektor-webpack-support)

This is a plugin for Lektor that adds support for webpack to projects.  When
enabled it can build a webpack project from the `webpack/` folder into the
asset folder automatically when the server (or build process) is run with
the `-f webpack` flag. 
In addition. it can be configured to run arbitrary `npm` scripts to support
arbitrary build tools, such as [Parcel](https://parceljs.org).

## Enabling the Plugin

To enable the plugin add this to your project file, run this command while
sitting in your Lektor project directory:

```bash
lektor plugins add lektor-webpack-support
```

## Example 1: Creating a Webpack Project

First create a webpack project. Create a `webpack/` folder and
inside that folder create `package.json` and a `webpack.config.js`

### `webpack/package.json`

This file instructs `npm` which packages we will need.  All we need for a
start is to create an almost empty file (name and version fields are mandatory
but not important for functionality, change them to suit your own needs):

```json
{
  "name": "lektor-webpack",
  "version": "1.0.0",
  "private": true
}
```

Now we can `npm install` (or `yarn add`) the rest:

```
$ cd </path/to/your/lektor/project>/webpack
$ npm install --save-dev webpack babel-core node-sass babel-loader sass-loader css-loader url-loader style-loader file-loader extract-text-webpack-plugin
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
const webpack = require('webpack');
const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

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
```

### Creating the App

Now we can start building our app.  We configured at least two files
in webpack: `js/main.js` and `scss/main.scss`.  Those are the entry
points we need to have.  You can create them as empty files in
`webpack/js/main.js` and `webpack/scss/main.scss`.

## Example 2: Creating a [Parcel](https://parceljs.org/) Project

To create a Parcel project, create a `parcel/` folder and inside that folder create the following files:

### `configs/webpack-support.ini`

This file instructs the plugin how to generate the assets. 

* `name` will be used in the output instead of 'webpack',
* `folder` should point to the project subforlder containing the parcel project, 
* `watch_script` is the npm script used in `lektor server -f webpack`,
* `build_script` is the npm script used in `lektor build -f webpack`.

```ini
name = Parcel
folder = parcel
watch_script = watch
build_script = build
```

### `parcel/package.json`

Similar to the webpack example above we need a `package.json` file. But in addition, we need to provide the npm scripts to use for `lektor build -f webpack` and `lektor watch -f webpack`.

```json
{
  "name": "lektor-webpack",
  "version": "1.0.0",
  "scripts": {
    "watch": "NODE_ENV=development parcel --out-dir=../assets/static/gen --out-file=main.js --public-url=./assets/ js/main.js",
    "build": "NODE_ENV=production parcel build --out-dir=../assets/static/gen --out-file=main.js --public-url=./assets/ js/main.js"
  },
  "private": true
}
```

Now we can `npm install` (or `yarn add`) the rest:

```
$ cd </path/to/your/lektor/project>/parcel
$ npm install --save-dev parcel-bundler babel-preset-env node-sass
```

This will install Parcel, babel and sass. 

### `parcel/babelr.rc`

Next up is a simple Babel config file, using the recommened env preset.

```json
{
  "presets": ["env"]
}
```

### `parcel/main.scss`

A simple SCSS file.

```scss
body {
  border: 10px solid red;
}
```

### `parcel/main.js`

A simple Javascript file that imports the SCSS file so that Parcel will know to include it as well.

```javascript
import './main.scss';
```

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
