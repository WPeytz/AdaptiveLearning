<template>
  <div class="quiz-container">
    <h1>Quiz</h1>
    <p v-if="loading">Loading quiz...</p>
    <div v-else>
      <p v-if="error">{{ error }}</p>
      <div v-else>
        <h2>{{ question.question }}</h2>
        <ul>
          <li v-for="(option, index) in question.options" :key="index">
            <button @click="checkAnswer(option)">{{ option }}</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      loading: true,
      error: null,
      question: null,
    };
  },
  async created() {
    try {
      const response = await axios.get("http://127.0.0.1:5000/questions/question_id_1");
      this.question = response.data;
      this.loading = false;
    } catch (err) {
      this.error = "Failed to load quiz question.";
      this.loading = false;
    }
  },
  methods: {
    checkAnswer(selectedOption) {
      if (selectedOption === this.question.answer) {
        alert("Correct!");
      } else {
        alert("Try again.");
      }
    },
  },
};
</script>

<style scoped>
.quiz-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>