import Vue from "vue";
import VueRouter from "vue-router";
Vue.use(VueRouter);

import "./app.css";

import Home from "../pages/Home.vue";
import CreateGame from "../pages/CreateGame.vue";

window.onload = main;

function main()
{
  const router = new VueRouter({
    mode: "history",
    routes: [
      {path: "/", component: Home},
      {path: "/create-game", component: CreateGame},
    ],
  });

  new Vue({
    router,
  }).$mount("#app");
}
