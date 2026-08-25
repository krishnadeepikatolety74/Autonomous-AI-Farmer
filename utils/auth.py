from functools import wraps
from flask import session, redirect, url_for, g, request, jsonify
from models.user_model import UserModel

def login_required(f):
    """Decorator to protect authenticated routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Return JSON 401 for AJAX/API requests so fetch() can parse it
            is_ajax = (
                request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                or request.accept_mimetypes.accept_json
                or request.path.startswith('/api/')
            )
            if is_ajax:
                return jsonify({"success": False, "error": "Session expired. Please sign in again."}), 401
            return redirect(url_for('auth.signin'))
        return f(*args, **kwargs)
    return decorated_function

def load_logged_in_user():
    """Load logged in user information into flask global variables container."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = UserModel.find_by_id(user_id)
