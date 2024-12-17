<template>
  <div class="markdown-content" v-html="renderedContent"></div>
</template>

<script>
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import 'highlight.js/styles/github-dark.css'
import DOMPurify from 'dompurify'
import { configManager } from '@/config/configManager'

export default {
  name: 'MarkdownRenderer',
  props: {
    content: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isDarkMode: configManager.getConfig('theme.darkMode')
    }
  },
  computed: {
    renderedContent() {
      // Ensure content is a string
      if (!this.content) return ''

      // Configure marked with highlight.js
      marked.setOptions({
        highlight: (code, lang) => {
          if (lang && hljs.getLanguage(lang)) {
            try {
              return hljs.highlight(code, { language: lang }).value
            } catch (err) {
              console.error('Highlight error:', err)
            }
          }
          return code // Return unchanged code for unknown languages
        }
      })

      // Convert markdown to HTML
      const html = marked(this.content)
      
      // Sanitize HTML
      const cleanHtml = DOMPurify.sanitize(html, {
        ADD_ATTR: ['target', 'rel'],
        ADD_TAGS: ['iframe']
      })

      return cleanHtml
    }
  },
  created() {
    // Listen for theme changes
    window.addEventListener('themeChanged', (event) => {
      this.isDarkMode = event.detail.darkMode
      this.updateCodeTheme()
    })
  },
  methods: {
    updateCodeTheme() {
      // Logic to update code highlighting theme based on dark/light mode
      const codeBlocks = this.$el.querySelectorAll('pre code')
      codeBlocks.forEach(block => {
        block.classList.toggle('hljs-dark', this.isDarkMode)
        block.classList.toggle('hljs-light', !this.isDarkMode)
      })
    }
  },
  mounted() {
    this.updateCodeTheme()
  }
}
</script>

<style>
.markdown-content {
  line-height: 1.6;
  word-wrap: break-word;
}

.markdown-content pre {
  background-color: #f4f4f4;
  border-radius: 4px;
  padding: 15px;
  overflow-x: auto;
}

.markdown-content code {
  font-family: 'Courier New', monospace;
  background-color: #f1f1f1;
  padding: 2px 4px;
  border-radius: 3px;
}

.markdown-content blockquote {
  border-left: 4px solid #ccc;
  margin: 0;
  padding-left: 10px;
  color: #666;
  font-style: italic;
}

.markdown-content h1, 
.markdown-content h2, 
.markdown-content h3, 
.markdown-content h4, 
.markdown-content h5, 
.markdown-content h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-content img {
  max-width: 100%;
  height: auto;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  color: var(--color-text);
  margin: var(--spacing-lg) 0 var(--spacing-md);
}

.markdown-content p {
  margin: var(--spacing-md) 0;
}

.markdown-content a {
  color: var(--color-primary);
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}

.markdown-content ul,
.markdown-content ol {
  margin: var(--spacing-md) 0;
  padding-left: var(--spacing-xl);
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--spacing-md) 0;
}

.markdown-content th,
.markdown-content td {
  padding: var(--spacing-sm);
  border: 1px solid var(--color-border);
  text-align: left;
}

.markdown-content th {
  background-color: var(--color-surface);
  font-weight: 600;
}

/* Hide default highlight.js themes */
:root .hljs {
  display: none;
}

/* Light theme styles */
.light-code .hljs {
  display: block;
  background-color: var(--color-surface) !important;
  color: #24292e !important;
}

/* Dark theme styles */
.dark-code .hljs {
  display: block;
  background-color: var(--color-surface) !important;
  color: #c9d1d9 !important;
}

.dark-code .hljs-keyword,
.dark-code .hljs-selector-tag {
  color: #ff7b72 !important;
}

.dark-code .hljs-string,
.dark-code .hljs-doctag {
  color: #a5d6ff !important;
}

.dark-code .hljs-title,
.dark-code .hljs-section {
  color: #d2a8ff !important;
}

.dark-code .hljs-type,
.dark-code .hljs-built_in {
  color: #ffa657 !important;
}

.dark-code .hljs-literal,
.dark-code .hljs-number {
  color: #79c0ff !important;
}

.dark-code .hljs-comment {
  color: #8b949e !important;
}

.dark-code .hljs-attr,
.dark-code .hljs-attribute {
  color: #7ee787 !important;
}

.dark-code .hljs-variable,
.dark-code .hljs-template-variable {
  color: #ffa198 !important;
}
</style>
