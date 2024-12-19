import { Definitions } from '/app/common/definitions.js';
const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')
const path = require('path')

const definitions = new Definitions();

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: 'warning',
  devServer: {
    port: definitions.ui.port || 8008
  },
  configureWebpack: {
    devtool: 'source-map',
    plugins: [
      new webpack.ProvidePlugin({
        process: 'process/browser',
        Buffer: ['buffer', 'Buffer']
      }),
      new webpack.LoaderOptionsPlugin({
        options: {
          resolve: {
            fallback: {
              "fs": false,
              "path": require.resolve("path-browserify"),
              "assert": require.resolve("assert/"),
              "stream": require.resolve("stream-browserify")
            }
          }
        }
      })
    ],
    resolve: {
      alias: {
        '@stores': path.resolve(__dirname, 'src/stores'),
        '@common': path.resolve(__dirname, '../common')
      },
      extensions: ['.js', '.ts', '.vue', '.json']
    },
    module: {
      rules: [
        {
          test: /\.ts$/,
          loader: 'ts-loader',
          options: {
            transpileOnly: true,
            appendTsSuffixTo: ['\\.vue$']
          }
        }
      ]
    }
  }
})
