<template>
  <div class="chat-control">
    <div class="input-container chat-input-container">
      <button class="settings-button chat-button" @click="toggleSettings">
        <i class="fas fa-cog"></i>
      </button>
      <textarea
        v-model="inputMessage"
        @keyup.enter.exact="sendMessage"
        placeholder="Type your message..."
        rows="1"
        ref="messageInput"
        class="chat-input"
      ></textarea>
      <button class="mic-button chat-button" @click="toggleMic" :class="{ active: isListening }">
        <i class="fas fa-microphone"></i>
      </button>
      <button class="send-button chat-button send" @click="sendMessage" :disabled="!inputMessage.trim()">
        <i class="fas fa-paper-plane"></i>
      </button>
    </div>
    <SettingsPanel v-model="showSettings" @settings-updated="handleSettingsUpdate" />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { Logger } from '/app/common/logger.js';
import SettingsPanel from './SettingsPanel.vue'
import apiConfig from '../services/apiConfig';
import { definitions } from '/app/common/definitions.js';

export default {
  name: 'ChatControl',
  components: {
    SettingsPanel
  },
  setup() {
    const logger = new Logger({
      serviceName: 'chat-control',
      logLevel: definitions.ui.logLevel || 'INFO',
      logFileName: definitions.ui.logFileName || 'ui.log'
    });

    // Reactive variables
    const messages = ref([]);
    const inputMessage = ref('');
    const isConnected = ref(false);
    const isListening = ref(false);
    const showSettings = ref(false);
    const historicalMessages = ref([]);

    // Simulated WebSocket connection (replace with actual implementation)
    const connectWebSocket = () => {
      try {
        logger.info('Attempting to establish WebSocket connection');
        // Simulated connection logic
        isConnected.value = true;
        logger.debug('WebSocket connection established');
      } catch (error) {
        logger.error(`WebSocket connection error: ${error.message}`);
        isConnected.value = false;
      }
    };

    // Send message method
    const sendMessage = async () => {
      if (inputMessage.value.trim().length === 0) {
        logger.warn('Attempted to send empty message');
        return;
      }

      try {
        logger.info('Sending chat message');
        logger.debug(`Message content: ${inputMessage.value}`);
        
        const apiClient = apiConfig.getClient();
        const response = await apiClient.post('/chat', {
          message: inputMessage.value
        });
        messages.value.push(response.data);
        inputMessage.value = '';
        logger.debug('Message sent successfully');
      } catch (error) {
        logger.error(`Error sending message: ${error.message}`);
      }
    };

    // Fetch historical messages
    const fetchHistoricalMessages = async () => {
      try {
        const apiClient = apiConfig.getClient();
        const response = await apiClient.get('/messages/history');
        historicalMessages.value = response.data;
      } catch (error) {
        logger.error(`Error fetching historical messages: ${error.message}`);
      }
    };

    // Toggle mic
    const toggleMic = () => {
      isListening.value = !isListening.value
      logger.info(`Microphone ${isListening.value ? 'enabled' : 'disabled'}`);
      // $emit('toggle-mic', isListening.value)
    };

    // Toggle settings
    const toggleSettings = () => {
      showSettings.value = !showSettings.value
      logger.info(`Settings ${showSettings.value ? 'opened' : 'closed'}`);
    };

    // Handle settings update
    const handleSettingsUpdate = (settings) => {
      logger.info('Settings updated');
      logger.debug(`Settings: ${JSON.stringify(settings)}`);
      // Apply settings immediately if needed
      document.documentElement.setAttribute('data-theme', settings.darkMode ? 'dark' : 'light')
      document.documentElement.style.fontSize = {
        small: '14px',
        medium: '16px',
        large: '18px'
      }[settings.fontSize] || '16px'
    };

    // Lifecycle hooks with logging
    onMounted(() => {
      logger.info('ChatControl component mounted');
      connectWebSocket();
    });

    onUnmounted(() => {
      logger.info('ChatControl component unmounted');
      // Add any cleanup logic here
    });

    return {
      messages,
      inputMessage,
      isConnected,
      isListening,
      showSettings,
      historicalMessages,
      sendMessage,
      toggleMic,
      toggleSettings,
      handleSettingsUpdate,
      logger  // Expose logger for potential external use
    };
  }
}
</script>

<style scoped>
.chat-control {
  position: fixed;
  bottom: 60px; /* Height of the navigation bar */
  left: 0;
  right: 0;
  padding: var(--spacing-md);
  background-color: var(--color-surface-raised);
  border-top: 1px solid var(--color-border);
  box-shadow: 0 -2px 10px var(--color-shadow);
  z-index: 90; /* Below the navigation bar's z-index */
}

.chat-input-container {
  display: flex;
  gap: var(--spacing-sm);
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: env(safe-area-inset-bottom); /* For devices with bottom safe area (e.g., iPhone) */
}

.chat-input {
  flex: 1;
  min-height: 40px;
  max-height: 200px;
  resize: none;
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--color-input-background);
  color: var(--color-input-text);
  border: 1px solid var(--color-input-border);
  border-radius: var(--radius-md);
  font-size: 1rem;
  line-height: 1.5;
  transition: all var(--transition-fast);
}

.chat-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(var(--color-primary), 0.2);
}

.chat-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  border-radius: var(--radius-full);
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  transition: all var(--transition-fast);
}

.chat-button:hover {
  background-color: var(--color-primary);
  color: var(--color-button-text);
  border-color: var(--color-primary);
}

.chat-button.send {
  background-color: var(--color-button-primary);
  color: var(--color-button-text);
  border-color: var(--color-button-primary);
}

.chat-button.send:hover {
  opacity: 0.9;
}

.chat-button i {
  font-size: 1.1em;
  margin: 0;
}
</style>
