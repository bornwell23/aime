<template>
  <div class="home">
    <h1>Welcome to Aime</h1>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HomeView',
  data() {
    return {
      message: ''
    }
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:3000')
      this.message = response.data.message
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
