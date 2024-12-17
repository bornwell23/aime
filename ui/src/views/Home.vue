<template>
  <div class="home">
    <div class="messages-container" ref="messagesContainer" @scroll="handleScroll">
      <div class="messages-wrapper">
        <div v-for="(message, index) in chatStore.chatHistory" :key="index" class="message" :data-role="message.role">
          <div class="message-header">
            <span class="message-role">{{ message.role }}</span>
            <span class="message-time">{{ formatTime(message.timestamp) }}</span>
          </div>
          <markdown-renderer :content="message.content" />
        </div>
        <!-- Anchor div for scrolling -->
        <div ref="messagesEnd" class="scroll-anchor"></div>
      </div>
    </div>
    
    <!-- Scroll buttons -->
    <Transition name="fade">
      <button v-if="showScrollTop" 
              @click="scrollToTop" 
              class="scroll-button scroll-top" 
              aria-label="Scroll to top">
        <i class="fas fa-arrow-up"></i>
      </button>
    </Transition>
    
    <Transition name="fade">
      <button v-if="showScrollBottom" 
              @click="scrollToBottom" 
              class="scroll-button scroll-bottom" 
              aria-label="Scroll to bottom">
        <i class="fas fa-arrow-down"></i>
      </button>
    </Transition>
    
    <div class="chat-control-wrapper">
      <chat-control @send-message="handleMessage" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useChatStore } from '@/store/chat'
import ChatControl from '@/components/ChatControl.vue'
import MarkdownRenderer from '@/components/MarkdownRenderer.vue'

export default {
  name: 'Home',
  components: {
    ChatControl,
    MarkdownRenderer
  },
  setup() {
    const chatStore = useChatStore()
    const messagesContainer = ref(null)
    const messagesEnd = ref(null)
    const showScrollTop = ref(false)
    const showScrollBottom = ref(false)

    const scrollToBottom = () => {
      if (messagesEnd.value) {
        nextTick(() => {
          messagesEnd.value.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'end',
            inline: 'nearest'
          })
        })
      }
    }

    const scrollToTop = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTo({
          top: 0,
          behavior: 'smooth'
        })
      }
    }

    const handleScroll = () => {
      if (!messagesContainer.value) return

      const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
      const scrolledToBottom = Math.ceil(scrollTop + clientHeight) >= scrollHeight - 10 // Add small threshold
      const scrolledToTop = scrollTop === 0

      // Show/hide scroll buttons based on position
      showScrollTop.value = scrollTop > 100
      showScrollBottom.value = !scrolledToBottom && scrollHeight > clientHeight
    }

    // Watch for changes in chat history
    watch(
      () => chatStore.chatHistory,
      () => {
        nextTick(() => {
          scrollToBottom()
          handleScroll()
        })
      },
      { deep: true }
    )

    // Initial scroll on mount
    onMounted(() => {
      scrollToBottom()
      handleScroll()
    })

    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString()
    }

    const handleMessage = async (message) => {
      // Add user message to chat
      const userMessage = {
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      }
      chatStore.addMessage(userMessage)

      try {
        // Add AI response
        const aiMessage = {
          role: 'assistant',
          content: 'This is a placeholder response. Implement actual AI response here.',
          timestamp: new Date().toISOString()
        }
        chatStore.addMessage(aiMessage)
      } catch (error) {
        console.error('Error processing message:', error)
        chatStore.addMessage({
          role: 'system',
          content: 'Error processing message. Please try again.',
          timestamp: new Date().toISOString()
        })
      }
    }

    return {
      chatStore,
      formatTime,
      handleMessage,
      messagesContainer,
      messagesEnd,
      scrollToTop,
      scrollToBottom,
      handleScroll,
      showScrollTop,
      showScrollBottom
    }
  }
}
</script>

<style scoped>
.home {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--color-background);
  position: relative;
  padding-bottom: 120px; /* Reserve space for chat control */
}

.messages-container {
  flex: 1;
  margin-top: auto;
  overflow-y: scroll;
  background-color: var(--color-background);
  padding: 0px;
  margin-bottom: 0px;
}

.messages-wrapper {
  max-width: 1200px;
  max-height: 10px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  min-height: 50%;
  padding-bottom: var(--spacing-lg);
}

.message {
  background-color: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  box-shadow: 0 2px 4px var(--color-shadow);
  width: 100%;
}

.scroll-anchor {
  height: 1px;
  margin-bottom: var(--spacing-lg);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-secondary);
  font-size: 0.9em;
}

.message-role {
  font-weight: 600;
  text-transform: capitalize;
}

.message-time {
  font-size: 0.9em;
}

/* Role-specific styling */
.message[data-role="assistant"] {
  background-color: var(--color-surface-raised);
}

.message[data-role="system"] {
  background-color: var(--color-surface);
  border-left: 4px solid var(--color-error);
}

.message[data-role="user"] {
  background-color: var(--color-surface);
  border-left: 4px solid var(--color-primary);
}

/* Chat control wrapper */
.chat-control-wrapper {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px; /* Fixed height for chat control */
  background-color: var(--color-background);
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border);
  box-shadow: 0 -4px 12px var(--color-shadow);
  z-index: 1;
  margin-top: auto;
}

/* Scroll buttons */
.scroll-button {
  position: fixed;
  right: var(--spacing-lg);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--color-surface-raised);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px var(--color-shadow);
  transition: all 0.2s ease;
  z-index: 95;
}

.scroll-button:hover {
  background-color: var(--color-primary);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--color-shadow);
}

.scroll-button:active {
  transform: translateY(0);
}

.scroll-top {
  bottom: calc(180px + var(--spacing-lg)); /* Increased distance from bottom */
}

.scroll-bottom {
  bottom: calc(120px + var(--spacing-lg)); /* Increased distance from bottom */
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* Custom scrollbar styling */
.messages-container::-webkit-scrollbar {
  width: 8px;
}

.messages-container::-webkit-scrollbar-track {
  background: var(--color-background);
}

.messages-container::-webkit-scrollbar-thumb {
  background-color: var(--color-border);
  border-radius: 4px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background-color: var(--color-text-secondary);
}
</style>
