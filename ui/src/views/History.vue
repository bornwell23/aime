<template>
  <div class="history">
    <div class="history-header">
      <h1>Chat History</h1>
      <div class="search-bar">
        <i class="fas fa-search"></i>
        <input type="text" placeholder="Search conversations..." v-model="searchQuery">
      </div>
    </div>
    <div class="history-content">
      <div class="conversation-list">
        <div v-for="(conversation, index) in conversations" :key="index" class="conversation-card">
          <div class="conversation-header">
            <span class="date">{{ conversation.date }}</span>
            <div class="actions">
              <button class="action-button">
                <i class="fas fa-star"></i>
              </button>
              <button class="action-button">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          <h3 class="conversation-title">{{ conversation.title }}</h3>
          <p class="conversation-preview">{{ conversation.preview }}</p>
          <div class="conversation-footer">
            <span class="message-count">{{ conversation.messageCount }} messages</span>
            <button class="view-button">View</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'History',
  data() {
    return {
      searchQuery: '',
      conversations: [
        {
          date: 'Today',
          title: 'Project Planning',
          preview: 'Discussion about the new feature implementation...',
          messageCount: 15
        },
        {
          date: 'Yesterday',
          title: 'Code Review',
          preview: 'Reviewing the latest pull request for the dashboard...',
          messageCount: 23
        },
        {
          date: '2 days ago',
          title: 'Bug Investigation',
          preview: 'Analyzing the reported performance issues...',
          messageCount: 8
        }
      ]
    }
  }
}
</script>

<style scoped>
.history {
  padding: var(--spacing-lg);
  min-height: 100vh;
  background-color: var(--color-background);
}

.history-header {
  margin-bottom: var(--spacing-xl);
}

.history-header h1 {
  color: var(--color-text);
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: var(--spacing-lg);
}

.search-bar {
  position: relative;
  max-width: 600px;
}

.search-bar i {
  position: absolute;
  left: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-secondary);
}

.search-bar input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) var(--spacing-xl);
  background-color: var(--color-input-background);
  color: var(--color-input-text);
  border: 1px solid var(--color-input-border);
  border-radius: var(--radius-md);
  font-size: 1rem;
}

.history-content {
  max-width: 1200px;
  margin: 0 auto;
}

.conversation-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.conversation-card {
  background-color: var(--color-surface-raised);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: 0 2px 8px var(--color-shadow);
  transition: transform var(--transition-fast);
}

.conversation-card:hover {
  transform: translateY(-2px);
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.date {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
}

.actions {
  display: flex;
  gap: var(--spacing-xs);
}

.action-button {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  padding: var(--spacing-xs);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-button:hover {
  color: var(--color-text);
  background-color: var(--color-surface);
}

.conversation-title {
  color: var(--color-text);
  font-size: 1.2rem;
  margin-bottom: var(--spacing-sm);
}

.conversation-preview {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  margin-bottom: var(--spacing-md);
  line-height: 1.5;
}

.conversation-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-count {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
}

.view-button {
  background-color: var(--color-button-primary);
  color: var(--color-button-text);
  border: none;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.view-button:hover {
  opacity: 0.9;
}
</style>
