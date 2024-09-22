import "./assets/main.css";
import { createApp } from "vue";
import VNetworkGraph from "v-network-graph";
import App from "./App.vue";

//import { createRouter } from "vue-router";
import router from "./router";
import "v-network-graph/lib/style.css";
import { createPinia } from "pinia";

const app = createApp(App);

app.use(VNetworkGraph);
app.use(createPinia());
app.use(router);

app.mount("#app");
