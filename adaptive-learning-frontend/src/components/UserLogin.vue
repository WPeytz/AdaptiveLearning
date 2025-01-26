<template>
  <div class="login-container">
    <div class="login-box">
      <h1>Welcome Back!</h1>
      <p>Please log in to continue to your learning journey.</p>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="Enter your email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Enter your password"
            required
          />
        </div>
        <button class="login-button" type="submit">Log In</button>
      </form>
      <div class="additional-links">
        <p>Don't have an account? <button @click="goToSignUp" class="link-button">Sign Up</button></p>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import firebaseApp from "../firebase";

export default {
  name: "UserLogin",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      const auth = getAuth(firebaseApp);
      try {
        const userCredential = await signInWithEmailAndPassword(
          auth,
          this.email,
          this.password
        );
        console.log("User logged in:", userCredential.user);
        this.$router.push("/quiz");
      } catch (error) {
        console.error("Login error:", error.message);
        alert("Login failed: " + error.message);
      }
    },
    goToSignUp() {
      this.$router.push("/signup");
    },
  },
};
</script>

<style scoped>
/* Container styling */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f9;
  font-family: Arial, sans-serif;
}

/* Login box */
.login-box {
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

/* Heading */
h1 {
  color: #333;
  margin-bottom: 10px;
}

p {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
}

/* Form group */
.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Login button */
.login-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #2a864e;
}

/* Additional links */
.additional-links {
  margin-top: 15px;
}

.link-button {
  background: none;
  border: none;
  color: #42b983;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
}

.link-button:hover {
  color: #2a864e;
}

/* Responsive design */
@media (max-width: 768px) {
  .login-box {
    padding: 15px;
    border-radius: 8px;
  }

  h1 {
    font-size: 20px;
  }

  p {
    font-size: 13px;
  }

  input,
  .login-button {
    font-size: 14px;
  }
}
</style>