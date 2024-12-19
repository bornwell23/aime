<template>
  <div class="home">
    <h1>Welcome to Aime</h1>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import { definitions } from '/app/common/definitions.js';

export default {
  name: 'HomeView',
  data() {
    return {
      message: ''
    }
  },
  async created() {
    try {
      const response = await axios.get(`http://${definitions.api.serviceName}:${definitions.api.port}/health`)
      this.message = response.data.message
      console.log(`Received data from server: ${this.message}`)
    } catch (error) {
      console.error('Error fetching data:', error)
      this.message = 'Error connecting to server'
    }
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
}
</style>
