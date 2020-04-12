const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const {VueLoaderPlugin} = require("vue-loader");

module.exports = {
  entry: [path.resolve(__dirname, "src/index.js")],
  output: {
    filename: "game.js",
    path: path.resolve(__dirname, "..", "dist"),
    publicPath: "/",
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: "vue-loader",
      },
      {
        test: /\.css$/,
        use: [
          "vue-style-loader",
          "css-loader",
        ],
      },
    ],
  },
  resolve: {
    alias: {
      vue: "vue/dist/vue.js",
    },
  },
  devtool: "inline-source-map",
  devServer: {
    stats: "errors-only",
    host: process.env.HOST,
    port: process.env.PORT,
    open: true,
    overlay: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: "Forest Game",
      template: path.resolve(__dirname, "index.html"),
    }),
    new VueLoaderPlugin(),
  ],
};
