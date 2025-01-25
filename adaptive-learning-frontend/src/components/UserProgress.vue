<template>
    <div class="progress-container">
      <h1>Your Progress</h1>
      <ul>
        <li v-for="(topic, key) in progress" :key="key">
          <strong>{{ key }}:</strong>
          <p>Accuracy: {{ topic.accuracy }}%</p>
          <p>Completed Questions: {{ topic.completed_questions }}</p>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        progress: {},
      };
    },
    async mounted() {
      await this.fetchProgress();
    },
    methods: {
      async fetchProgress() {
        try {
          const response = await axios.get('http://localhost:5000/users/test_user_1/progress');
          this.progress = response.data;
        } catch (error) {
          console.error('Error fetching progress:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .progress-container {
    max-width: 600px;
    margin: 0 auto;
  }
  </style>