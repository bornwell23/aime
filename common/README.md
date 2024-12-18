# Aime Common Utilities

## Overview
This directory contains shared utilities and common modules used across the Aime application.

## Contents
- `logger.js`: A centralized logging utility for both ui and server services
- `apiContract.ts`: Shared API contract for type-safe interactions

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

### API Contract
#### Overview
This package defines a type-safe, flexible API contract that can be used across both UI and server implementations.

#### Key Features
- Type-safe interfaces using TypeScript
- Standardized response handling
- Pagination support
- Generic CRUD operations
- Flexible authentication mechanisms

#### Structure
- `types.ts`: Defines core interfaces and types
- `apiContract.ts`: Specifies API endpoint contracts and provides a base implementation

#### Usage Example

```typescript
// In your UI service
import { createApiClient } from './apiContract';

const apiClient = createApiClient('https://api.yourapp.com');

// Authenticate
const loginResponse = await apiClient.auth.login({
  email: 'user@example.com',
  password: 'password123'
});

// Create a generic resource
const todoClient = apiClient.createGenericCrudEndpoints<Todo>('todos');
const newTodo = await todoClient.create({ title: 'Learn API Design' });
```

#### Design Principles
1. **Type Safety**: All interactions are strongly typed
2. **Flexibility**: Easy to extend and modify
3. **Separation of Concerns**: Clear distinction between types and implementation

#### Error Handling
Use the `ApiResponse<T>` interface for consistent error management:
- `success`: Boolean indicating operation success
- `data`: Optional payload
- `error`: Optional error message

#### Pagination
Supports consistent pagination across all list endpoints:
- `page`: Current page number
- `limit`: Items per page
- `sortBy`: Field to sort on
- `sortOrder`: 'asc' or 'desc'

## Dependencies
- `winston`: Flexible logging library
- `fs-extra`: Enhanced file system operations

## Configuration
Logging can be configured via environment variables or direct configuration.

## Contributing
Please ensure all shared utilities maintain high quality and are framework-agnostic.
