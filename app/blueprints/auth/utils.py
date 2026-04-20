from functools import wraps
from flask import redirect, session, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "session_token" not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function