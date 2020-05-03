const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const webpack = require("webpack");
const {VueLoaderPlugin} = require("vue-loader");

const gitCount = require("child_process").execSync("git rev-list HEAD --count").toString().trim();
const gitTag = require("child_process").execSync("git tag --points-at HEAD").toString().trim();
const versionId = gitTag != "" ? gitTag : "DEV." + gitCount;

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
        test: /\.(png)$/,
        loader: "file-loader",
        options: {
          outputPath: "assets",
        },
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
      filename: "index.html",
    }),
    new VueLoaderPlugin(),
    new webpack.DefinePlugin({
      "__VERSION__": JSON.stringify(versionId),
    }),
  ],
};
