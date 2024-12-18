import { createApp } from 'vue';
import FloatingVue from 'floating-vue'
import './style.css';
import App from './App.vue';
import routes from './router/routes';

import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
  const app = createApp(App);
  app.use(router);
  app.use(FloatingVue);
  app.mount('#app');