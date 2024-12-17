# Aime Common Utilities

## Overview
This directory contains shared utilities and common modules used across the Aime application.

## Contents
- `logger.js`: A centralized logging utility for both ui and server services

## Installation
```bash
npm install
```

## Usage
### Logging
```javascript
import { Logger } from '/app/common/logger.js'

const logger = new Logger({
  serviceName: 'my-service',
  logLevel: 'INFO',
  logFileName: 'my-service.log'
});

logger.info('Application started');
```

## Dependencies
- `winston`: Flexible logging library
- `fs-extra`: Enhanced file system operations

## Configuration
Logging can be configured via environment variables or direct configuration.

## Contributing
Please ensure all shared utilities maintain high quality and are framework-agnostic.
