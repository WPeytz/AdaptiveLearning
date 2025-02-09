import { createRouter, createWebHistory } from 'vue-router';
import { getAuth } from 'firebase/auth'; //AuthStateChanged
import { getFirestore, doc, getDoc } from 'firebase/firestore';
import UserLogin from '../components/UserLogin.vue';
import QuizScreen from '../components/QuizScreen.vue';
import UserProgress from '../components/UserProgress.vue';
import UserSignUp from "../components/UserSignUp.vue";
import StudentDashboard from "../components/StudentDashboard.vue";
import TeacherDashboard from "../components/TeacherDashboard.vue";

const routes = [
  { path: '/', redirect: '/login' }, // Default redirect to login
  { path: '/login', component: UserLogin },
  { path: '/signup', component: UserSignUp },
  { path: '/quiz', component: QuizScreen, meta: { requiresAuth: true } },
  { path: '/progress', component: UserProgress, meta: { requiresAuth: true } },
  { path: '/student-dashboard', component: StudentDashboard, meta: { requiresAuth: true, role: 'student' } },
  { path: '/teacher-dashboard', component: TeacherDashboard, meta: { requiresAuth: true, role: 'teacher' } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Authentication & Role-Based Navigation Guard
router.beforeEach(async (to, from, next) => {
  const auth = getAuth();
  const user = auth.currentUser;

  if (to.meta.requiresAuth) {
    if (!user) {
      next('/login'); // Redirect to login if not authenticated
    } else {
      const db = getFirestore();
      const userRef = doc(db, "users", user.uid);
      const userDoc = await getDoc(userRef);

      if (userDoc.exists()) {
        const userRole = userDoc.data().role;
        
        if (to.meta.role && to.meta.role !== userRole) {
          next('/login'); // Redirect if role doesn't match
        } else {
          next();
        }
      } else {
        next('/login');
      }
    }
  } else {
    next();
  }
});

export default router;