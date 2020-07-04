import Vue from "vue";
import VueRouter from "vue-router";
Vue.use(VueRouter);

import "./app.css";

import Home from "../pages/Home.vue";
import Cookies from "../pages/Cookies.vue";
import CreateGame from "../pages/CreateGame.vue";
import JoinGame from "../pages/JoinGame.vue";
import ChangeName from "../pages/ChangeName.vue";
import Lobby from "../pages/Lobby.vue";
import Game from "../pages/Game.vue";
import PageNotFound from "../pages/PageNotFound.vue";

window.onload = main;

function main()
{
  const router = new VueRouter({
    mode: "history",
    routes: [
      {path: "/", component: Home, props: {version: __VERSION__}},
      {path: "/cookies", name: "cookies", component: Cookies},
      {path: "/create-game", component: CreateGame},
      {path: "/join-game", component: JoinGame},
      {path: "/game/:gameId/change-name", name: "change-name", component: ChangeName},
      {path: "/game/:gameId/lobby", name: "lobby", component: Lobby},
      {path: "/game/:gameId", name: "game", component: Game},
      {path: "*", component: PageNotFound},
    ],
  });

  new Vue({
    router,
  }).$mount("#app");
}
