import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../components/UserLogin.vue';
import QuizScreen from '../components/QuizScreen.vue';
import UserProgress from '../components/UserProgress.vue';
import UserSignUp from "../components/UserSignUp.vue";

const routes = [
  { path: '/', redirect: '/login' }, // Redirect to login as the default
  { path: '/login', component: UserLogin },
  { path: '/quiz', component: QuizScreen },
  { path: '/progress', component: UserProgress },
  { path: "/signup", component: UserSignUp },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;