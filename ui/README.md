# Aime ui

A modern, single-page Vue.js application featuring an AI chat interface with assistant-like functionality.

## Project Structure

```
ui/
├── src/
│   ├── components/           # Reusable components
│   │   ├── NavigationBar.vue # Bottom navigation
│   │   └── ChatControl.vue   # Chat input and controls
│   ├── views/               # Page components
│   │   ├── Home.vue         # Chat interface
│   │   ├── Dashboard.vue    # Topic cards view
│   │   └── History.vue      # Past conversations and interactions
│   ├── router/              # Vue Router configuration
│   ├── App.vue              # Root component
│   └── main.js              # Application entry point
│   └── utils/               # Utility functions
```

## Features

### Home Page (Chat Interface)
- Real-time chat interface with AI
- Message bubbles with user/AI distinction
- Auto-scrolling chat container
- Control panel with:
  - Expandable text input
  - Voice input toggle
  - Send button
- Responsive design for all screen sizes

### Dashboard
- Grid layout of topic cards
- Categories include:
  - Notes
  - Topics
  - Ideas
  - News
- Each card displays:
  - Category icon
  - Title
  - Summary
  - Item count
  - Quick access button

### History
- Tabbed interface for:
  - Past conversations
  - Dashboard item interactions
- Chronological listing with:
  - Title and icon
  - Timestamp
  - Content preview

### Navigation
- Fixed bottom navigation bar
- Icons and labels for each section
- Active state indicators
- Smooth transitions

## Technical Details

### Dependencies
- Vue.js 3
- Vue Router 4
- Font Awesome 5 (for icons)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run serve
```

3. Build for production:
```bash
npm run build
```

### Design System

#### Colors
- Primary: #007AFF
- Background: #f5f5f5
- Text: #333333
- Secondary Text: #666666

#### Components
- Cards with subtle shadows
- Rounded corners (8px-12px)
- Consistent padding and spacing
- Smooth hover effects and transitions

#### Typography
- System font stack for optimal rendering
- Hierarchical sizing
- Comfortable line heights for readability

## Logging

Aime uses a custom logging utility located in `/app/common/logger.js`. 

### Logger Configuration

The logger supports multiple log levels:
- `ERROR`: Critical errors that prevent normal operation
- `WARN`: Potential issues that don't stop the application
- `INFO`: General information about application state
- `DEBUG`: Detailed debugging information

### Usage Example

```javascript
import { Logger } from '/app/common/logger';

// Create a logger instance
const logger = new Logger({
    logLevel: 'DEBUG',  // Optional: set log level (default is 'INFO')
    serviceName: 'ui',  // Optional: custom service name
    logFileName: 'ui.log'  // Optional: custom log file name
});

// Log messages
logger.error('Something went wrong');
logger.warn('Potential issue detected');
logger.info('Component initialized');
logger.debug('Detailed debug information');
```

### Log File Location

Logs are stored in `d:/coding/Aime/logs/` by default:
- Server logs: `server.log`
- ui logs: `ui.log`

Each log entry includes:
- Timestamp
- Log Level
- Service Name
- Message

## Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Responsive design works on mobile and desktop

## Development Guidelines

### Adding New Features
1. Create new components in `src/components/`
2. Add new routes in `router/index.js`
3. Follow existing style patterns
4. Maintain responsive design

### Best Practices
- Use Vue composition API for new components
- Keep components modular and reusable
- Follow Vue.js style guide
- Implement proper error handling
- Add appropriate loading states

## Future Enhancements
- [ ] Dark mode support
- [ ] User preferences storage
- [ ] Enhanced voice input
- [ ] Rich text message support
- [ ] File attachment handling
- [ ] Message search functionality

## License
[MIT License](LICENSE)
