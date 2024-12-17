<template>
  <div id="app" :class="{ 'dark-theme': isDarkMode }">
    <router-view />
    <NavigationBar />
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue'
import { configManager } from '@/config/configManager'

export default {
  name: 'App',
  components: {
    NavigationBar
  },
  data() {
    return {
      isDarkMode: configManager.getConfig('theme.darkMode')
    }
  },
  created() {
    // Watch for theme changes
    window.addEventListener('storage', (event) => {
      if (event.key === 'aimeConfig') {
        const config = JSON.parse(event.newValue)
        this.isDarkMode = config.theme.darkMode
      }
    })

    // Listen for custom event from configManager
    window.addEventListener('themeChanged', (event) => {
      this.isDarkMode = event.detail.darkMode
    })
  }
}
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}

/* Icon styles */
.fas, .far, .fab {
  display: inline-block;
  line-height: 1;
  vertical-align: middle;
  margin-right: var(--spacing-xs);
}
</style>
