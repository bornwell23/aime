# Aime Microservice Project

This project consists of two main components:
- `server`: Node.js + Express backend service
- `ui`: Vue.js web interface

## Project Structure
```
Aime/
├── server/         # Backend Node.js + Express service
└── ui/       # ui Vue.js application
```

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Environment Configuration
Create a `.env` file in the project root with the following variables:
```
UI_PORT=8008
SERVER_PORT=3000
NODE_ENV=development
VUE_APP_API_VERSION=V1
VUE_APP_LOG_LEVEL=INFO
```

### Running the Application

#### Development Mode

##### Note
If you are using windows, make sure Docker Desktop is running.

```bash
docker-compose up --build
```

#### Production Mode
```bash
docker-compose -f docker-compose.yml up --build -d
```

### Accessing the Application
- ui: `http://localhost:8008`
- server API: `http://localhost:3000`

### Stopping the Application
```bash
docker-compose down
```

## Setup Instructions

### server
1. Navigate to the server directory: `cd server`
2. Install dependencies: `npm install`
3. Start the server: `npm start`
4. For development with hot-reload: `npm run dev`

### ui
1. Navigate to the ui directory: `cd ui`
2. Install dependencies: `npm install`
3. Start the development server: `npm run serve`
4. For production build: `npm run build`

## Local Development

### Ui
```bash
cd ui
npm install
npm run serve
```

### Server
```bash
cd server
npm install
npm start
```

## Deployment Notes
- The application uses multi-stage Docker builds
- ui is served via Nginx
- server is a Node.js application
- Environment variables can be customized in the `.env` file
- To use a custom url for the ui instead of localhost:
  - c:\Windows\System32\Drivers\etc\hosts
  - `aime localhost`