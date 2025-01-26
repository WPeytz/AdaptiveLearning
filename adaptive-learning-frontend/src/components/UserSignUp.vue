<template>
    <div class="signup-container">
      <h1>Sign Up</h1>
      <form @submit.prevent="signUp">
        <label for="email">Email:</label>
        <input type="email" v-model="email" id="email" required />
  
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
  
        <button type="submit">Sign Up</button>
      </form>
      <button @click="goToLogin" class="login-button">Back to Login</button>
    </div>
  </template>
  
  <script>
  import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
  import firebaseApp from "../firebase"; // Import Firebase initialization
  
  export default {
    data() {
      return {
        email: "",
        password: "",
      };
    },
    methods: {
      async signUp() {
        const auth = getAuth(firebaseApp); // Use the initialized Firebase app
        try {
          const userCredential = await createUserWithEmailAndPassword(auth, this.email, this.password);
          console.log("User signed up:", userCredential.user);
          alert("Sign up successful! You can now log in.");
          this.$router.push("/login"); // Redirect to login after successful sign-up
        } catch (error) {
          console.error("Sign up error:", error.message);
          alert("Sign up failed: " + error.message); // Display error message
        }
      },
      goToLogin() {
        this.$router.push("/login"); // Navigate back to login
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
  </style>