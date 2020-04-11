import Vue from "vue";
import VueRouter from "vue-router";
Vue.use(VueRouter);

import "./app.css";

import Home from "../pages/Home.vue";
import CreateGame from "../pages/CreateGame.vue";
import ChangeName from "../pages/ChangeName.vue";

window.onload = main;

function main()
{
  const router = new VueRouter({
    mode: "history",
    routes: [
      {path: "/", component: Home},
      {path: "/create-game", component: CreateGame},
      {path: "/game/:gameId/change-name", name: "change-name", component: ChangeName},
    ],
  });

  new Vue({
    router,
  }).$mount("#app");
}
