import Vue from "vue";
import VueRouter from "vue-router";
Vue.use(VueRouter);

import "./app.css";

import Home from "../pages/Home.vue";
import CreateGame from "../pages/CreateGame.vue";
import ChangeName from "../pages/ChangeName.vue";
import Game from "../pages/Game.vue";
import PageNotFound from "../pages/PageNotFound.vue";

window.onload = main;

function main()
{
  const router = new VueRouter({
    mode: "history",
    routes: [
      {path: "/", component: Home, props: {version: __VERSION__}},
      {path: "/create-game", component: CreateGame},
      {path: "/game/:gameId/change-name", name: "change-name", component: ChangeName},
      {path: "/game/:gameId", name: "game", component: Game},
      {path: "*", component: PageNotFound},
    ],
  });

  new Vue({
    router,
  }).$mount("#app");
}
