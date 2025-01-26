<template>
  <div class="quiz-container">
    <h1>Quiz</h1>

    <!-- Loading State -->
    <div v-if="loading">
      <p>Loading question...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error">
      <p>{{ error }}</p>
      <button @click="loadQuestion">Retry</button>
    </div>

    <!-- Quiz Question & Answers -->
    <div v-else>
      <p><strong>Question: </strong> {{ questionData.question }}</p>
      <div class="options">
        <button
          v-for="(option, index) in questionData.options"
          :key="index"
          @click="checkAnswer(option)"
        >
          {{ option }}
        </button>
      </div>

      <!-- Feedback -->
      <p 
        v-if="feedback" 
        :class="{ correct: isCorrect, incorrect: !isCorrect }"
      >
        {{ feedback }}
      </p>

      <!-- Next Question Button -->
      <button v-if="isCorrect" @click="loadQuestion">
        Next Question
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuizScreen',
  data() {
    return {
      questionData: {
        question: '',
        options: [],
        answer: ''
      },
      loading: true,
      error: null,
      feedback: null,
      isCorrect: false
    };
  },
  methods: {
    async loadQuestion() {
      this.loading = true;
      this.error = null;
      this.feedback = null;

      try {
        const response = await fetch("http://127.0.0.1:5003/generate_question", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ topic: "Fractions", difficulty: "Easy" }),
        });

        if (!response.ok) {
          throw new Error("Failed to load question");
        }

        const data = await response.json();

        // If your backend returns something like:
        // {
        //   "question": {
        //     "question": "What is 1/4 of 3/4?",
        //     "options": [ "A) 1/16", "B) 3/16", ... ],
        //     "answer": "B) 3/16"
        //   }
        // }
        //
        // then set questionData to data.question.
        // Otherwise, if the backend returns:
        // {
        //   "question": "What is 1/4 of 3/4?",
        //   "options": [ "A) 1/16", "B) 3/16", ... ],
        //   "answer": "B) 3/16"
        // }
        // then set questionData to data.

        if (data.question && typeof data.question === 'object') {
          // Nested object
          this.questionData = data.question;
        } else {
          // Top-level fields
          this.questionData = data;
        }

        this.loading = false;
      } catch (err) {
        this.error = "Failed to load quiz question. Please try again.";
        this.loading = false;
      }
    },

    checkAnswer(selectedOption) {
      const normalizedSelected = selectedOption.trim().toLowerCase();
      const normalizedAnswer = this.questionData.answer.trim().toLowerCase();

      if (normalizedSelected === normalizedAnswer) {
        this.feedback = "Correct! Well done.";
        this.isCorrect = true;
      } else {
        this.feedback = "Incorrect. Please try again.";
        this.isCorrect = false;
      }
    }
  },
  mounted() {
    this.loadQuestion();
  }
};
</script>

<style scoped>
.quiz-container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

.options button {
  display: inline-block;
  margin: 10px 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.options button:hover {
  background-color: #0056b3;
}

.correct {
  color: green;
  font-weight: bold;
  margin-top: 20px;
}

.incorrect {
  color: red;
  font-weight: bold;
  margin-top: 20px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>