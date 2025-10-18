from flask import Blueprint, redirect, request, session, jsonify, url_for
from backend.auth.auth import auth
import os

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/auth/login')
def login():
    """Redirects to Discord's OAuth2 login page."""
    state = auth.generate_auth_url()
    session['oauth2_state'] = state
    return redirect(auth.generate_auth_url(state=state))

@auth_bp.route('/auth/callback')
def callback():
    """Handles the OAuth2 callback from Discord."""
    state = session.pop('oauth2_state', None)
    if state is None or request.args.get('state') != state:
        return 'Invalid state', 400

    code = request.args.get('code')
    if not code:
        return 'Missing code', 400

    token_data = auth.exchange_code(code)
    if not token_data:
        return 'Failed to exchange code', 500

    user_info = auth.get_user_info(token_data['access_token'])
    if not user_info:
        return 'Failed to get user info', 500

    session_id = auth.create_session(user_info['id'], user_info, token_data)
    session['session_id'] = session_id
    
    return redirect(url_for('index'))

@auth_bp.route('/auth/logout')
def logout():
    """Logs the user out by clearing the session."""
    session_id = session.pop('session_id', None)
    if session_id:
        auth.logout(session_id)
    return redirect(url_for('index'))

@auth_bp.route('/api/user')
def get_user():
    """Returns the current user's data if logged in."""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Not authenticated'}), 401

    user_session = auth.validate_session(session_id)
    if not user_session:
        return jsonify({'error': 'Invalid or expired session'}), 401

    return jsonify(user_session['user'])
