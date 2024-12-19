import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { Logger } from '@common/logger.js'
import { Definitions } from '/app/common/definitions.js';

import '@fortawesome/fontawesome-free/css/all.css'
import '@/assets/styles/theme.css'
import './index.css'

const definitions = new Definitions();

// Create global logger
const logger = new Logger({
    serviceName: definitions.ui.serviceName || 'ui',
    logLevel: definitions.ui.logLevel || 'INFO',
    logFileName: definitions.ui.logFileName || 'ui.log'
})

// Create app and plugins
const app = createApp(App)
const pinia = createPinia()

// Attach logger to global properties
app.config.globalProperties.$logger = logger

// Log application startup
logger.info('Initializing Aime ui Application')
logger.info(`Using API URL: ${definitions.server.api_url}`)

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
