import { createApp } from "vue";
import App from "./App.vue";
import router from "./routes";
import { pinia } from "./plugins/pinia";
import "./style.css";

// Punto de entrada de la app Vue
const app = createApp(App);
app.use(pinia); // registra Pinia: estado global (tokens y usuario de la sesión)
app.use(router); // registra Vue Router: navegación entre vistas
app.mount("#app"); // monta la app sobre el <div id="app"> del index.html
