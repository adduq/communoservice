// import Vue from 'vue'
// import store from '@/store'
// import router from '@/router'

// import axios from 'axios'
// axios.defaults.xsrfCookieName = 'csrftoken'
// axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// import App from '@/App.vue'
// import './registerServiceWorker'

// Vue.config.productionTip = false

// new Vue({
//   router,
//   store,

// render: h => h(App)
// }).$mount('#app')

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import './assets/reset.css';

axios.defaults.baseURL = "http://127.0.0.1:8000/";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

createApp(App)
    .use(store)
    .use(router, axios)
    .mount("#app");