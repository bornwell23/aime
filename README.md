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
- server API: `http://localhost:8001`

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
- Environment variables can be customized in the environment or a `.env` file
- To use a custom url for the ui instead of localhost:
  - c:\Windows\System32\Drivers\etc\hosts
  - `aime localhost`

### Database Configuration
- PostgreSQL is used as the primary database
- Database name: `aime_app`
- Default credentials:
  - Username: `aime_admin`
  - Password: `aime_password`

#### Database Initialization
- The database is automatically created during container startup
- Connection details are configured in `docker-compose.yml`
- Database connection is tested during server initialization

## Testing Docker Builds

### `test_docker_builds.py`

This script is used to validate and fix Docker image builds for services in the project.

#### Usage

```bash
python test_docker_builds.py [--fix] [--dontfix] [service_name]
```

##### Options
- `--fix`: Automatically fix PEP8 issues in Python files
- `--dontfix`: Run checks without fixing files - default functionality
- `service_name`: (Optional) Specify a specific service to build/check. If not provided, all services will be processed.

##### Example Commands
- Check all services: `python test_docker_builds.py`
- Check a specific service: `python test_docker_builds.py server`
- Fix PEP8 issues: `python test_docker_builds.py --fix`

#### Features
- Runs Docker image builds
- Checks Python code syntax using Flake8 and Pylint
- Optionally fixes PEP8 style issues
- Generates detailed logs in `test/logs/` directory

#### Logging
- Logs are saved in timestamped directories under `test/logs/`
- Includes console and file logging
- Diff logs show code changes when fixing PEP8 issues