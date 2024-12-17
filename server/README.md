# Aime Server

A modular, versioned REST API server built with Express.js.

## Project Structure

```
server/
├── src/
│   ├── api/              # API version routing
│   │   ├── v1/          # v1 API implementation
│   │   │   ├── routes/  # Route definitions
│   │   │   └── index.js # v1 router
│   │   └── index.js     # API version handler
│   ├── controllers/      # Business logic
│   ├── middleware/       # Custom middleware
│   ├── services/        # Business services
│   ├── utils/           # Utility functions
│   └── index.js         # Main application file
├── ecosystem.config.js   # PM2 configuration
├── package.json         # Dependencies and scripts
├── startup.bat          # Windows startup script
└── restart.bat          # Service restart script
```

## Getting Started

### Prerequisites
- Node.js (Latest LTS version recommended)
- npm or yarn

### Installation

1. Run the startup script as administrator:
```bash
startup.bat
```

This will:
- Install all dependencies
- Set up PM2 globally
- Start the service
- Configure the service to run on system startup

### Managing the Service

- To restart the service:
```bash
restart.bat
```

- PM2 Commands:
  - Check status: `pm2 status`
  - View logs: `pm2 logs`
  - Restart service: `pm2 restart aime-server`
  - Stop service: `pm2 stop aime-server`

## API Structure

### Current Endpoints (v1)

- Base URL: `/api/v1`

#### Health Check
- `GET /api/v1/health` - Service health status

#### Example Routes
- `GET /api/v1/examples` - Get all examples
- `GET /api/v1/examples/:id` - Get example by ID
- `POST /api/v1/examples` - Create new example
- `PUT /api/v1/examples/:id` - Update example
- `DELETE /api/v1/examples/:id` - Delete example

### Error Handling

The API includes centralized error handling with different responses for:
- Validation errors (400)
- Authorization errors (401)
- Internal server errors (500)

Error details in responses depend on the NODE_ENV setting:
- Development: Includes error message and stack trace
- Production: Generic error message only

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
const { Logger } = require('/app/common/logger');

// Create a logger instance
const logger = new Logger({
    logLevel: 'DEBUG',  // Optional: set log level (default is 'INFO')
    serviceName: 'server',  // Optional: custom service name
    logFileName: 'server.log'  // Optional: custom log file name
});

// Log messages
logger.error('Something went wrong');
logger.warn('Potential issue detected');
logger.info('Application started');
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

## Adding New Features

### Adding a New API Version

1. Create a new version directory:
```bash
mkdir src/api/v2
```

2. Copy and modify the routes from v1
3. Add the new router to `src/api/index.js`

### Adding New Endpoints

1. Create a new route file in `src/api/v1/routes/`
2. Create corresponding controller in `src/controllers/`
3. Register the route in `src/api/v1/index.js`

## Development

### Scripts

- `npm start` - Start the server normally
- `npm run dev` - Start with nodemon for development
- `npm run prod` - Start with PM2 for production

### Environment Variables

Create a `.env` file in the root directory:
```env
BACK_PORT=3000
NODE_ENV=development
```

## License

[MIT License](LICENSE)
