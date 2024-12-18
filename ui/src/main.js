import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { Logger } from '@common/logger.js'

import '@fortawesome/fontawesome-free/css/all.css'
import '@/assets/styles/theme.css'
import './index.css'

// Create global logger
const logger = new Logger({
    serviceName: 'ui',
    logLevel: process.env.VUE_APP_LOG_LEVEL || 'INFO',
    logFileName: 'ui.log'
})

// Create app and plugins
const app = createApp(App)
const pinia = createPinia()

// Attach logger to global properties
app.config.globalProperties.$logger = logger

// Log application startup
logger.info('Initializing Aime ui Application')

// Use plugins
app.use(pinia)
   .use(router)
   .mount('#app')

// Log any unhandled errors
window.addEventListener('error', (event) => {
    logger.error(`Unhandled error: ${event.message}`)
})

// Log unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    logger.error(`Unhandled promise rejection: ${event.reason}`)
})
