import Vue from "vue";
import VueRouter from "vue-router";
import VueSession from "vue-session";
import DatetimePicker from "vuetify-datetime-picker";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import axios from "axios";
import Authentication from "./Authentication";
import Login from "./components/auth/Login";
import Registration from "./components/auth/Registration";
import VueNativeSock from "vue-native-websocket";
import TransactionController from "./components/util/TransactionAPI";
import AuthenticationAPI from "./components/util/AuthenticationAPI";

import "./main.css";
import CryptoMonitor from "./components/CryptoMonitor";

Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(VueSession);
Vue.use(VueNativeSock, "ws://" + window.location.host + "/ws/exchangeRate", {
  connectManually: true
});
Vue.use(DatetimePicker);

const base = axios.create({
  baseURL: "http://127.0.0.1:8000",
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN"
});

Vue.prototype.$http = base;
Vue.prototype.$socket = VueNativeSock.socket;
Vue.prototype.$transAPI = new TransactionController(Vue.prototype.$http);
Vue.prototype.$authAPI = new AuthenticationAPI(Vue.prototype.$http);

const routes = [
  {
    path: "",
    component: Authentication,
    children: [
      { path: "/login", component: Login },
      { path: "/registration", component: Registration }
    ]
  },
  {
    path: "/monitor/open",
    component: CryptoMonitor,
    alias: "/monitor/closed"
  }
];

const router = new VueRouter({
  routes,
  mode: "history",
  meta: {
    reload: true
  }
});

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount("#app");
