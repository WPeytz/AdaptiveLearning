<template>
  <div class="quiz-container">
    <div class="header">
      <!-- Title -->
      <h1 class="title">Math Quiz</h1>

      <!-- Statistics and Log Out Buttons -->
      <div class="header-buttons">
        <button class="stats-btn" @click="goToStatistics">Statistics</button>
        <button class="logout-btn" @click="logout">Log Out</button>
      </div>
    </div>

    <!-- Correct Streak -->
    <div class="streak-container">
      <p class="streak-label">Current Streak:</p>
      <span class="streak-badge">{{ correctStreak }}</span>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <p>Loading question...</p>
      <div class="spinner"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadQuestion" class="retry-btn">Retry</button>
    </div>

    <!-- Quiz Question & Answers -->
    <div v-else>
      <p class="question">{{ questionData.question }}</p>
      <div class="options">
        <button
          v-for="(option, index) in questionData.options"
          :key="index"
          :class="[
            'option-btn',
            {
              correct: selectedOption === option && isCorrect,
              incorrect: selectedOption === option && !isCorrect,
              'show-correct': selectedOption !== null && option === questionData.answer && !isCorrect,
            }
          ]"
          @click="checkAnswer(option)"
          :disabled="selectedOption !== null"
        >
          {{ option }}
        </button>
      </div>

      <!-- Feedback -->
      <p
        v-if="feedback"
        class="feedback"
        :class="{ 'feedback-correct': isCorrect, 'feedback-incorrect': !isCorrect }"
      >
        {{ feedback }}
      </p>

      <!-- Difficulty Feedback Buttons -->
      <div v-if="selectedOption !== null && !feedbackSubmitted" class="feedback-buttons">
        <p class="feedback-title">How would you rate the question's difficulty?</p>
        <div class="feedback-buttons-group">
          <button class="feedback-btn" @click="submitFeedback('Very Easy')">Very Easy</button>
          <button class="feedback-btn" @click="submitFeedback('Easy')">Easy</button>
          <button class="feedback-btn" @click="submitFeedback('Medium')">Medium</button>
          <button class="feedback-btn" @click="submitFeedback('Hard')">Hard</button>
          <button class="feedback-btn" @click="submitFeedback('Wrong')">Wrong</button>
          <button class="feedback-btn skip-btn" @click="submitFeedback('Skipped')">Skip</button>
        </div>
      </div>

      <!-- Next Question Button -->
      <button
        v-if="feedbackSubmitted"
        @click="loadQuestion"
        class="next-btn"
      >
        Next Question
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuizScreen",
  data() {
    return {
      questionData: {
        question: "",
        options: [],
        answer: "",
      },
      loading: true,
      error: null,
      feedback: null,
      isCorrect: false,
      selectedOption: null, // Track the user's selected option
      correctStreak: 0, // Keep track of the correct streak
      feedbackSubmitted: false, // Track if feedback has been submitted
    };
  },
  methods: {
    async loadQuestion() {
      this.loading = true;
      this.error = null;
      this.feedback = null;
      this.selectedOption = null;
      this.feedbackSubmitted = false; // Reset feedback submission state

      try {
        const response = await fetch("http://127.0.0.1:5003/generate_question", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ user_id: "test_user" }),
        });

        if (!response.ok) {
          throw new Error("Failed to load question");
        }

        const data = await response.json();
        this.questionData = data;
        this.correctStreak = data.correct_streak || 0; // Update the correct streak from the backend
        this.loading = false;
      } catch (err) {
        this.error = "Failed to load quiz question. Please try again.";
        this.loading = false;
      }
    },

    checkAnswer(selectedOption) {
      if (this.selectedOption !== null) return; // Prevent multiple clicks

      this.selectedOption = selectedOption; // Mark the selected option
      const normalizedSelected = selectedOption.trim().toLowerCase();
      const normalizedAnswer = this.questionData.answer.trim().toLowerCase();

      if (normalizedSelected === normalizedAnswer) {
        //this.feedback = "Correct! Well done.";
        this.isCorrect = true;
        this.updateStreak(true);
      } else {
        //this.feedback = "Incorrect. Better luck next time!";
        this.isCorrect = false;
        this.updateStreak(false);
      }
    },

    async updateStreak(isCorrect) {
      try {
        const response = await fetch("http://127.0.0.1:5003/submit_answer", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: "test_user",
            is_correct: isCorrect,
          }),
        });

        const data = await response.json();
        this.correctStreak = data.correct_streak || 0; // Update the correct streak dynamically
      } catch (error) {
        console.error("Failed to update streak:", error);
      }
    },

    async submitFeedback(difficulty) {
      try {
        await fetch("http://127.0.0.1:5003/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: "test_user",
            question: this.questionData.question,
            difficulty: difficulty,
          }),
        });
        this.feedbackSubmitted = true; // Mark feedback as submitted
        console.log(`Feedback '${difficulty}' submitted successfully.`);
      } catch (error) {
        console.error("Failed to submit feedback:", error);
      }
    },

    goToStatistics() {
      this.$router.push("/statistics");
    },

    logout() {
      console.log("User logged out");
      this.$router.push("/login");
    },
  },
  mounted() {
    this.loadQuestion();
  },
};
</script>

<style scoped>
/* General Container Styles */
.quiz-container {
  max-width: 600px;
  margin: 40px auto;
  text-align: center;
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 15px;
  background: linear-gradient(135deg, #f9f9f9, #ffffff);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

/* Header Styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

/* Button Styles */
.stats-btn, .logout-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 15px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stats-btn:hover, .logout-btn:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

/* Loading State */
.loading p {
  font-size: 1.2rem;
  color: #333;
}

.spinner {
  margin: 10px auto;
  width: 30px;
  height: 30px;
  border: 4px solid #ccc;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Error State */
.error {
  color: red;
  font-weight: bold;
}

.retry-btn {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.retry-btn:hover {
  background-color: #c62828;
}

/* Question & Options */
.question {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  background-color: #e7e7e7;
  border: none;
  padding: 10px 15px;
  font-size: 1.1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.option-btn:hover {
  background-color: #d6d6d6;
  transform: scale(1.05);
}

.option-btn.correct {
  background-color: #4caf50; /* Green for correct answers */
  color: white;
}

.option-btn.incorrect {
  background-color: #f44336; /* Red for incorrect answers */
  color: white;
}

.option-btn.show-correct {
  background-color: #4caf50; /* Highlight the correct answer */
  color: white;
}

/* Feedback */
.feedback {
  margin-top: 20px;
  font-size: 1.2rem;
}

.feedback-correct {
  color: #4caf50;
}

.feedback-incorrect {
  color: #f44336;
}

/* Next Question Button */
.next-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.next-btn:hover {
  background-color: #0056b3;
}

/* Styles for Feedback Buttons */
.feedback-buttons {
  margin-top: 20px;
  text-align: center;
}

.feedback-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  font-weight: bold;
}

.feedback-buttons-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.feedback-btn {
  background-color: #f0f0f0;
  color: #333;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.feedback-btn:hover {
  background-color: #007bff;
  color: white;
  transform: scale(1.05);
}

.skip-btn {
  background-color: #f0f0f0;
  color: black;
}

.skip-btn:hover {
  background-color: #c62828;
}

/* Next Button */
.next-btn {
  margin-top: 20px;
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.2rem;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.next-btn:hover {
  background-color: #218838;
}

/* Streak Container */
.streak-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  font-family: 'Arial', sans-serif;
}

/* Streak Label */
.streak-label {
  font-size: 1.2rem;
  font-weight: bold;
  margin-right: 10px;
  color: #333;
}

/* Streak Badge */
.streak-badge {
  display: inline-block;
  background-color: #4caf50; /* Green for success */
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  padding: 5px 15px;
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  /* animation: streak-pulse 1.5s infinite ease-in-out; */
}

/* Badge Animation */
@keyframes streak-pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

</style>