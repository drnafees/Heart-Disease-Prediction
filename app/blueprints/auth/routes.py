from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

class HealthcareProfessional:
    def __init__(self, email, password):
        self.email = email
        self.__password = password
        self.session_token = None
        self.patients = []  # This will hold Patient instances associated with the professional

    def login(self):
        if self.email == "test@domain.com" and self.__password == "password":
            self.session_token = "mock_token_12345"
            return {"email": self.email, "session_token": self.session_token}
        return {"email": None, "session_token": None}
    
    def logout(self):
        self.session_token = None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        professional = HealthcareProfessional(email, password)
        auth_result = professional.login()
        if auth_result["session_token"]:
            global session_token
            session_token = auth_result["session_token"]
            return redirect(url_for('main.index'))
        else:
            return render_template("login.html", error="Invalid credentials. Please try again.")

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    professional = HealthcareProfessional(session.get("email"), None)
    professional.logout()
    return redirect(url_for('auth.login'))