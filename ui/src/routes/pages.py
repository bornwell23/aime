from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from common.definitions import UI_SETTINGS, AI_MODEL_SETTINGS
from common.logging import logger

def register_main_routes(app):
    @app.route('/')
    @login_required
    def index():
        return render_template('home.html', 
                             user=current_user,
                             UI_SETTINGS=UI_SETTINGS,
                             AI_MODEL_SETTINGS=AI_MODEL_SETTINGS)

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html', 
                             user=current_user,
                             UI_SETTINGS=UI_SETTINGS,
                             AI_MODEL_SETTINGS=AI_MODEL_SETTINGS)

    @app.route('/history')
    @login_required
    def history():
        return render_template('history.html', user=current_user)

    @app.route('/chat')
    @login_required
    def chat():
        return render_template('chat.html', user=current_user)
