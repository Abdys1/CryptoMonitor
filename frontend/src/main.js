import Vue from 'vue'
import VueRouter from 'vue-router'
import VueSession from "vue-session";
import App from './App.vue'
import vuetify from './plugins/vuetify';
import axios from 'axios';
// import Authentication from "./components/Authentication";
import CryptoMonitor from "./components/CryptoMonitor";
import Registration from "./components/Registration";
import Login from "./components/Login";

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(VueSession)
axios.baseUrl = "https://127.0.0.1:8000"

const routes = [
  {path: "/registration", component: Registration},
  {path: "/login", component: Login},
  {path: "/", redirect: "/login"},
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
