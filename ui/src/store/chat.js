import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    chatHistory: [],
    currentConversation: null
  }),
  
  actions: {
    addMessage(message) {
      this.chatHistory.push(message)
    },
    setChatHistory(history) {
      this.chatHistory = history
    },
    clearChatHistory() {
      this.chatHistory = []
    },
    setCurrentConversation(conversation) {
      this.currentConversation = conversation
    }
  },

  getters: {
    getChatHistory: (state) => state.chatHistory,
    getCurrentConversation: (state) => state.currentConversation
  }
})
