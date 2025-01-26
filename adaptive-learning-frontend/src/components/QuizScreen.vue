<template>
  <div class="quiz-container">
    <h1>Quiz</h1>
    <p v-if="loading">Loading quiz...</p>
    <div v-else>
      <p v-if="error">
        {{ error }}
        <button @click="fetchQuestion">Retry</button>
      </p>
      <div v-else>
        <h2>{{ question.question }}</h2>
        <ul v-if="!answeredCorrectly">
          <li v-for="(option, index) in question.options" :key="index">
            <button @click="checkAnswer(option)">{{ option }}</button>
          </li>
        </ul>
        <div v-if="answeredCorrectly" class="correct-answer">
          <p>Correct!</p>
          <button @click="fetchNextQuestion" class="next-button">Next Question</button>
        </div>
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
      questionId: 1, // Start with the first question
      answeredCorrectly: false,
    };
  },
  methods: {
    async fetchQuestion() {
      this.loading = true;
      this.error = null;
      this.answeredCorrectly = false; // Reset the state for the new question
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/questions/question_id_${this.questionId}`
        );
        this.question = response.data;
      } catch (err) {
        console.error("Error fetching question:", err);
        this.error = "Failed to load quiz question. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    checkAnswer(selectedOption) {
      if (selectedOption === this.question.answer) {
        this.answeredCorrectly = true; // Mark as correct
      } else {
        alert("Try again.");
      }
    },
    fetchNextQuestion() {
      this.questionId++; // Increment the question ID
      this.fetchQuestion(); // Fetch the next question
    },
  },
  created() {
    this.fetchQuestion();
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
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

ul {
  list-style-type: none;
  padding: 0;
}

button {
  display: block;
  margin: 0.5rem 0;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

.correct-answer {
  text-align: center;
  margin-top: 20px;
}

.next-button {
  background-color: #28a745;
}

.next-button:hover {
  background-color: #218838;
}
</style>