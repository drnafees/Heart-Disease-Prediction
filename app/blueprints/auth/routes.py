from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)
    
def authenticate_user(email, password):
    if email == "test@domain.com" and password == "password":
        session["session_token"] = "mock_token_12345"
        return {"email": "test@domain.com", "session_token": session["session_token"]}
    return {"email": None, "session_token": None}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth_result = authenticate_user(email, password)
        if auth_result["session_token"]:
            global session_token
            session_token = auth_result["session_token"]
            return redirect(url_for('main.index'))
        else:
            return render_template("login.html", error="Invalid credentials. Please try again.")

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.pop("session_token", None)
    return redirect(url_for('auth.login'))