import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";

const app = createApp(App);

// TODO: Faire en sorte que MAPBOX_API_KEY soit changé dynamiquement selon l'environnement d'exécution
// NOTE: Pour l'instant, nous utilisons une clé publique pour les tests
app.config.globalProperties.MAPBOX_API_KEY =
	"pk.eyJ1IjoidmFuaXR5cHciLCJhIjoiY2t2a2FhcmxmZDNkOTJxcTYybXNkODRoZSJ9.dNeojMWUvXZH-TkiFqTexA";

import { SetupCalendar, Calendar, DatePicker } from "v-calendar";
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
	.component("Calendar", Calendar)
	.component("DatePicker", DatePicker)
	.mount("#app");
