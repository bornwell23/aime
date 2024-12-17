import defaultConfig from './default.json'

class ConfigManager {
  constructor() {
    this.config = this.loadConfig()
    this.initializeTheme()
  }

  loadConfig() {
    try {
      const savedConfig = localStorage.getItem('aimeConfig')
      if (savedConfig) {
        return { ...defaultConfig, ...JSON.parse(savedConfig) }
      }
    } catch (error) {
      console.error('Error loading config:', error)
    }
    return defaultConfig
  }

  saveConfig() {
    try {
      localStorage.setItem('aimeConfig', JSON.stringify(this.config))
      // Dispatch storage event for other tabs
      window.dispatchEvent(new StorageEvent('storage', {
        key: 'aimeConfig',
        newValue: JSON.stringify(this.config)
      }))
    } catch (error) {
      console.error('Error saving config:', error)
    }
  }

  updateConfig(path, value) {
    let current = this.config
    const parts = path.split('.')
    const last = parts.pop()

    for (const part of parts) {
      if (!(part in current)) {
        current[part] = {}
      }
      current = current[part]
    }

    current[last] = value
    this.saveConfig()
    this.applyConfig()
    
    // Emit theme change event if theme was updated
    if (path === 'theme.darkMode') {
      window.dispatchEvent(new CustomEvent('themeChanged', {
        detail: { darkMode: value }
      }))
    }
  }

  getConfig(path = '') {
    if (!path) return this.config

    let current = this.config
    const parts = path.split('.')

    for (const part of parts) {
      if (!(part in current)) {
        return undefined
      }
      current = current[part]
    }

    return current
  }

  initializeTheme() {
    this.applyTheme(this.config.theme.darkMode)
  }

  applyTheme(isDark) {
    const colors = this.config.theme.colors[isDark ? 'dark' : 'light']
    const root = document.documentElement

    // Apply CSS variables
    Object.entries(colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value)
    })

    // Set theme attribute
    root.setAttribute('data-theme', isDark ? 'dark' : 'light')

    // Apply font size
    root.style.fontSize = this.config.ui.fontSizes[this.config.ui.fontSize]
  }

  applyConfig() {
    this.applyTheme(this.config.theme.darkMode)
  }

  toggleDarkMode() {
    this.updateConfig('theme.darkMode', !this.config.theme.darkMode)
  }
}

export const configManager = new ConfigManager()
