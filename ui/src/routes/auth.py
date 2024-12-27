from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from common.logging import logger
from services.account import AccountManager


def register_auth_routes(app):
    account_manager = AccountManager()

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Handle user login"""
        if current_user.is_authenticated:
            logger.info(f"User {current_user} already authenticated, redirecting to home")
            return redirect(url_for('home'))

        if request.method == 'POST':
            # Get login credentials from form
            username = request.form.get('username')
            password = request.form.get('password')

            logger.info(f"Login attempt for username: {username}")

            # Use AccountManager to handle login
            login_result = account_manager.login(username, password)

            if login_result.get('success'):
                user = login_result.get('user')
                login_user(user)
                logger.info(f"Login successful for {username} with roles: {user.roles}. Redirecting to home")
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

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Handle user registration"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')

            success, message = account_manager.register(username, password, email)
            if success:
                # Pass a success message to the login page
                return redirect(url_for('login', success_message='Registration successful! Please log in.'))
            return render_template('register.html', error=message)
        return render_template('register.html', error="Unknown error during registration")

    @app.route('/logout')
    @login_required
    def logout():
        """Handle user logout"""
        if current_user.is_authenticated:
            user_id = current_user.id
            username = current_user.username
            roles = current_user.roles

            account_manager.logout(user_id)
            logout_user()

            logger.info(f"Logged out user: {username} (roles: {roles})")
            flash('You have been logged out.', 'info')

        return redirect(url_for('login'))
