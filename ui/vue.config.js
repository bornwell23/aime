const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')
const path = require('path')
const dotenv = require('dotenv')

// Load environment variables from project root .env file
const envPath = path.resolve(__dirname, '../.env')
dotenv.config({ path: envPath })

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: 'warning',
  devServer: {
    port: process.env.FRONT_PORT || 8008
  },
  configureWebpack: {
    devtool: 'source-map',
    plugins: [
      new webpack.ProvidePlugin({
        process: 'process/browser',
        Buffer: ['buffer', 'Buffer']
      })
    ],
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
