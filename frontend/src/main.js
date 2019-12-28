import Vue from 'vue'
import VueRouter from 'vue-router'
import VueSession from "vue-session";
import App from './App.vue'
import vuetify from './plugins/vuetify';
import axios from 'axios';
import CryptoMonitor from "./components/CryptoMonitor";
import Authentication from "./Authentication";
import Login from "./components/Login";
import Registration from "./components/Registration";

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(VueSession)

axios.baseUrl = "https://127.0.0.1:8000"
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

const routes = [
  {path: "", component: Authentication,
    children: [
      {path: "/login", component: Login},
      {path: "/registration", component: Registration}
    ]},
  {path: "/monitor", component: CryptoMonitor}
]

const router = new VueRouter({
  routes,
  mode: "history",
  meta: {
    reload: true,
  },
})

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
