import {
    createApp
} from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import {
    SetupCalendar,
    Calendar,
    DatePicker
} from 'v-calendar';
if (process.env.VUE_APP_AXIOS_URL === undefined) {
    if (window.location.hostname.includes("dev-"))
        axios.defaults.baseURL = "https://dev-api-communoservice.herokuapp.com/";
    else axios.defaults.baseURL = "https://api-communoservice.herokuapp.com/";
}

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

createApp(App)
    .use(store)
    .use(router, axios)
    .component('Calendar', Calendar)
    .component('DatePicker', DatePicker)
    .mount("#app");