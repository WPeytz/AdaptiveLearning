<template>
  <div class="signup-container">
    <h1>Tilmeld dig</h1>
    <form @submit.prevent="signUp">
      <label for="email">Email:</label>
      <input type="email" v-model="email" id="email" required />

      <label for="password">Adgangskode:</label>
      <input type="password" v-model="password" id="password" required />

      <label for="role">Vælg din rolle:</label>
      <select v-model="role" id="role" required>
        <option value="student">Elev</option>
        <option value="teacher">Lærer</option>
      </select>

      <button type="submit">Tilmeld dig</button>
    </form>
    <button @click="goToLogin" class="login-button">Tilbage til login</button>
  </div>
</template>

<script>
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
import { getFirestore, doc, setDoc } from "firebase/firestore";
import firebaseApp from "../firebase"; // Firebase initialization

export default {
  data() {
    return {
      email: "",
      password: "",
      role: "student", // Default role is student
    };
  },
  methods: {
    async signUp() {
      const auth = getAuth(firebaseApp);
      const db = getFirestore(firebaseApp);

      try {
        // Create user in Firebase Authentication
        const userCredential = await createUserWithEmailAndPassword(auth, this.email, this.password);
        const user = userCredential.user;

        // Store user role in Firestore
        await setDoc(doc(db, "users", user.uid), {
          email: this.email,
          role: this.role,
        });

        console.log("User signed up:", user);
        alert("Tilmelding lykkedes! Du bliver nu omdirigeret.");

        // Redirect based on role
        if (this.role === "teacher") {
          this.$router.push("/teacher-dashboard");
        } else {
          this.$router.push("/student-dashboard");
        }

      } catch (error) {
        console.error("Sign up error:", error.message);
        alert("Tilmelding mislykkedes: " + error.message);
      }
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  margin-top: 10px;
  background-color: #42b983;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  width: 100%;
}

button:hover {
  background-color: #2a864e;
}

.login-button {
  margin-top: 10px;
  background-color: #888;
}

.login-button:hover {
  background-color: #555;
}

select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}
</style>