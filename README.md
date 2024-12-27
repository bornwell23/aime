# Aime Microservice Project

This project consists of three main components:
- `server`: Main backend service that handles business logic and database operations
- `auth-service`: Authentication service for user management and token handling
- `ui`: Flask web interface

## Project Structure
```
Aime/
├── server/         # Main backend service
├── auth-service/   # Authentication service
└── ui/            # Flask web application
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
- UI: `http://localhost:8081`
- Server API: `http://localhost:8001` (for internal use only)
- Auth Service: `http://localhost:8000` (for internal use only)

### Stopping the Application
```bash
docker-compose down
```

## Architecture

### Authentication Flow
1. The UI communicates only with the main server
2. The server proxies authentication requests to the auth service
3. The auth service handles token generation and validation
4. Session management is handled at both UI and auth service levels

### Database Architecture
- Main application database (`aime_app`): Used by the server for application data
- Authentication database (`aime_auth`): Used by the auth service for user management
- Default credentials:
  - Username: `aime_admin`
  - Password: `aime_password`

## Setup Instructions

### Server
1. Navigate to the server directory: `cd server`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server: `python src/app.py`

### Auth Service
1. Navigate to the auth service directory: `cd auth-service`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the service: `python src/app.py`

### UI
1. Navigate to the UI directory: `cd ui`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the development server: `python src/app.py`

## Local Development



## Deployment Notes
- The application uses multi-stage Docker builds
- UI is served via Flask development server (production should use gunicorn)
- All services use Python with Flask
- Environment variables can be customized in the environment or `.env` files
- To use a custom URL instead of localhost:
  - Edit: `c:\Windows\System32\Drivers\etc\hosts`
  - Add: `aime localhost`

### Security Notes
- All authentication tokens are handled securely through the auth service
- The UI never directly communicates with the auth service
- User sessions are managed both at the UI level and through token validation
- All user input is validated and sanitized
- Secure headers and CORS policies are implemented

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