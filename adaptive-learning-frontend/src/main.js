import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Set up global API URL
const API_URL = "https://adaptive-learning-489216095849.europe-west1.run.app"; // Cloud Run backend URL
window.API_URL = API_URL; // Make it accessible globally

createApp(App).use(store).use(router).mount('#app')