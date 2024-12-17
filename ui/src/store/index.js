import { createStore } from 'vuex'

export default createStore({
  state() {
    return {
      chatHistory: [],
      currentConversation: null
    }
  },
  mutations: {
    ADD_MESSAGE(state, message) {
      if (state.chatHistory) {
        state.chatHistory.push(message)
      } else {
        state.chatHistory = [message]
      }
    },
    SET_CHAT_HISTORY(state, history) {
      state.chatHistory = history
    },
    CLEAR_CHAT_HISTORY(state) {
      state.chatHistory = []
    },
    SET_CURRENT_CONVERSATION(state, conversation) {
      state.currentConversation = conversation
    }
  },
  actions: {
    addMessage({ commit }, message) {
      commit('ADD_MESSAGE', message)
    },
    setChatHistory({ commit }, history) {
      commit('SET_CHAT_HISTORY', history)
    },
    clearChatHistory({ commit }) {
      commit('CLEAR_CHAT_HISTORY')
    },
    setCurrentConversation({ commit }, conversation) {
      commit('SET_CURRENT_CONVERSATION', conversation)
    }
  },
  getters: {
    getChatHistory: state => state.chatHistory || [],
    getCurrentConversation: state => state.currentConversation
  }
})
