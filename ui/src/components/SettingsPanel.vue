<template>
  <div class="settings-overlay" v-if="modelValue" @click.self="close">
    <div class="settings-panel">
      <div class="settings-header">
        <h2>Settings</h2>
        <button class="close-button" @click="close">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="settings-content">
        <div class="setting-group">
          <h3>Appearance</h3>
          <div class="setting-item">
            <label>
              <input 
                type="checkbox" 
                :checked="settings.darkMode" 
                @change="toggleTheme"
              >
              Dark Mode
            </label>
          </div>
          <div class="setting-item">
            <label>Font Size</label>
            <select v-model="settings.fontSize" @change="updateSetting('ui.fontSize')">
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="large">Large</option>
            </select>
          </div>
        </div>
        
        <div class="setting-group">
          <h3>Chat</h3>
          <div class="setting-item">
            <label>
              <input type="checkbox" v-model="settings.autoScroll" @change="updateSetting('chat.autoScroll')">
              Auto-scroll to new messages
            </label>
          </div>
          <div class="setting-item">
            <label>
              <input type="checkbox" v-model="settings.sendOnEnter" @change="updateSetting('chat.sendOnEnter')">
              Send message on Enter
            </label>
          </div>
        </div>

        <div class="setting-group">
          <h3>AI Model</h3>
          <div class="setting-item">
            <label>Model</label>
            <select v-model="settings.aiModel" @change="updateSetting('chat.defaultModel')">
              <option value="gpt-3.5">GPT-3.5</option>
              <option value="gpt-4">GPT-4</option>
            </select>
          </div>
          <div class="setting-item">
            <label>Temperature</label>
            <input 
              type="range" 
              min="0" 
              max="100" 
              v-model.number="settings.temperature"
              @change="updateSetting('chat.temperature')"
            >
            <span>{{ settings.temperature }}%</span>
          </div>
        </div>
      </div>
      <div class="settings-footer">
        <button class="save-button" @click="saveSettings">Save Changes</button>
      </div>
    </div>
  </div>
</template>

<script>
import { configManager } from '@/config/configManager'

export default {
  name: 'SettingsPanel',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      settings: {
        darkMode: true, // Default to dark mode
        fontSize: 'medium',
        autoScroll: true,
        sendOnEnter: true,
        aiModel: 'gpt-3.5',
        temperature: 70
      }
    }
  },
  methods: {
    close() {
      this.$emit('update:modelValue', false)
    },
    toggleTheme(event) {
      this.settings.darkMode = event.target.checked
      this.updateSetting('theme.darkMode')
    },
    updateSetting(path) {
      const pathParts = path.split('.')
      const key = pathParts[pathParts.length - 1]
      configManager.updateConfig(path, this.settings[key])
      this.$emit('settings-updated', this.settings)
    },
    saveSettings() {
      configManager.saveConfig()
      this.$emit('settings-updated', this.settings)
      this.close()
    }
  },
  created() {
    // Load settings from config manager
    const config = configManager.getConfig()
    this.settings = {
      darkMode: config.theme.darkMode,
      fontSize: config.ui.fontSize,
      autoScroll: config.chat.autoScroll,
      sendOnEnter: config.chat.sendOnEnter,
      aiModel: config.chat.defaultModel,
      temperature: config.chat.temperature
    }
  }
}
</script>

<style scoped>
.settings-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--color-overlay);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.settings-panel {
  background-color: var(--color-surface-raised);
  border-radius: var(--radius-lg);
  box-shadow: 0 4px 20px var(--color-shadow);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  color: var(--color-text);
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

.settings-header h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: var(--radius-full);
  transition: all var(--transition-fast);
}

.close-button:hover {
  color: var(--color-text);
  background-color: var(--color-surface);
}

.settings-content {
  padding: var(--spacing-md);
}

.setting-group {
  margin-bottom: var(--spacing-xl);
}

.setting-group h3 {
  color: var(--color-text);
  margin-bottom: var(--spacing-md);
  font-size: 1.2rem;
}

.setting-item {
  margin-bottom: var(--spacing-md);
}

.setting-item label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--color-text);
  cursor: pointer;
}

.setting-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.setting-item input[type="range"] {
  width: 100%;
  margin: var(--spacing-xs) 0;
}

.setting-item select {
  width: 100%;
  padding: var(--spacing-sm);
  background-color: var(--color-input-background);
  color: var(--color-input-text);
  border: 1px solid var(--color-input-border);
  border-radius: var(--radius-sm);
}

.settings-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
}

.save-button {
  background-color: var(--color-button-primary);
  color: var(--color-button-text);
  border: none;
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-weight: 500;
  transition: all var(--transition-fast);
}

.save-button:hover {
  opacity: 0.9;
}
</style>
