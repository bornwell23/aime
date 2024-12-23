from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import os
from services.auth_service import AuthService
from services.api_config import APIConfig
from dotenv import load_dotenv
from logger import logger
import requests
import time

# Load environment variables
load_dotenv()

def check_server_health(max_retries=3, delay=5):
    """
    Perform health check on the server with retry mechanism
    """
    api_config = APIConfig()
    health_url = api_config.get_api_url('/system/health')
    
    for attempt in range(max_retries):
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                logger.info('Server health check successful')
                return True
            logger.warning(f'Health check failed. Status code: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logger.error(f'Health check error (attempt {attempt + 1}): {e}')
        
        # Wait before retrying
        time.sleep(delay)
    
    logger.error('Server health check failed after maximum retries')
    return False

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    
    # Perform server health check before creating the app
    time.sleep(5)  # Wait for services to start
    if not check_server_health():
        raise RuntimeError('Unable to establish connection with server')
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        """
        Callback to reload the user object from the user ID stored in the session
        """
        try:
            # In a real app, you'd fetch user details from a database or service
            # For now, we'll create a minimal user object
            logger.info(f"Loading user with ID: {user_id}")
            return AuthService().get_user(user_id)
        except Exception as e:
            logger.error(f"Error loading user: {e}")
            return None

    # Initialize services
    auth_service = AuthService()
    api_config = APIConfig()

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        Handle user login
        - GET: Render login page
        - POST: Process login credentials
        """
        # If user is already logged in, redirect to home
        if current_user.is_authenticated:
            logger.info(f"User already authenticated, redirecting to home")
            return redirect(url_for('home'))

        # Handle login form submission
        if request.method == 'POST':
            # Get login credentials from form
            username = request.form.get('username')
            password = request.form.get('password')

            logger.info(f"Login attempt for username: {username}")

            # Use AuthService to handle login
            login_result = auth_service.login(username, password)

            logger.info(f"Login result: {login_result}")

            # Check login result
            if login_result.get('success'):
                logger.info(f"Login successful for user: {username}")
                
                # Create user object for Flask-Login
                user_data = login_result.get('user')
                user = user_data
                
                # Use Flask-Login to log in the user
                login_user(user)
                
                logger.info(f"Redirecting {username} to home page")
                return redirect(url_for('home'))
            else:
                # Login failed - render login page with error
                logger.warning(f"Login failed: {login_result.get('error', 'Unknown error')}")
                return render_template('login.html', error=login_result.get('error', 'Login failed'))

        # GET request - render login page
        success_message = request.args.get('success_message')
        if success_message:
            return render_template('login.html', success_message=success_message)
        return render_template('login.html')

    @app.route('/home')
    @login_required
    def home():
        """
        Render home page for authenticated users
        """
        return render_template('home.html', user=current_user)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            data = request.form
            success, error_message = auth_service.register(
                data.get('username'),
                data.get('password'),
                data.get('email')
            )
            if success:
                # Pass a success message to the login page
                return redirect(url_for('login', success_message='Registration successful! Please log in.'))
            return render_template('register.html', error=error_message)
        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/api/chat', methods=['POST'])
    @login_required
    def chat():
        message = request.json.get('message')
        # Implement chat functionality here
        return jsonify({"response": "Message received"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)), debug=True)
