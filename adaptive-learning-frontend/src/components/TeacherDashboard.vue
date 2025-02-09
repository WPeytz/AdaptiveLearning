<template>
    <div class="dashboard-container">
      <h1>Lærer Dashboard</h1>
  
      <button @click="viewStudents">Se Elever</button>
      <button @click="createQuiz">Opret Quiz</button>
      <button @click="viewStudentProgress">Se Elevfremgang</button>
      <button @click="sendFeedback">Send Feedback</button>
      <button @click="logOut" class="logout-button">Log ud</button>
    </div>
  </template>
  
  <script>
  import { getAuth, signOut } from "firebase/auth";
  
  export default {
    methods: {
      viewStudents() {
        this.$router.push("/teacher/students");
      },
      createQuiz() {
        this.$router.push("/teacher/create-quiz");
      },
      viewStudentProgress() {
        this.$router.push("/teacher/progress");
      },
      sendFeedback() {
        this.$router.push("/teacher/feedback");
      },
      logOut() {
        const auth = getAuth();
        signOut(auth)
          .then(() => {
            this.$router.push("/login");
          })
          .catch((error) => {
            console.error("Log out error:", error.message);
            alert("Fejl ved log ud: " + error.message);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .dashboard-container {
    max-width: 500px;
    margin: 0 auto;
    text-align: center;
  }
  
  button {
    display: block;
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    font-size: 18px;
    background-color: #4287f5;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  
  button:hover {
    background-color: #2a64c7;
  }
  
  .logout-button {
    background-color: #ff5252;
  }
  
  .logout-button:hover {
    background-color: #d42e2e;
  }
  </style>