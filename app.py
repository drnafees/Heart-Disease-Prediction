from flask import Flask, redirect, render_template, request, url_for
import pandas as pd
import joblib
import tensorflow as tf
from functools import wraps

app = Flask(__name__)
session_token = None

try:
    ann_model = tf.keras.models.load_model("models/ann_model.keras")
    lr_pipeline = joblib.load("models/lr_pipeline.pkl")
    rf_pipeline = joblib.load("models/rf_pipeline.pkl")
except Exception as e:
    print(f"Error loading models: {e}")
    ann_model = None
    lr_pipeline = None
    rf_pipeline = None


def map_risk(prob):
    if prob < 0.33:
        return "Low Risk"
    elif prob < 0.66:
        return "Medium Risk"
    else:
        return "High Risk"
    
def authenticate_user(email, password):
    if email == "test@domain.com" and password == "password":
        session_token = "mock_token_12345"
        return {"email": "test@domain.com", "session_token": session_token}
    return {"email": None, "session_token": None}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session_token is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    input_data = {}
    results = None
    if request.method == "POST":
        input_data = {
            "age": int(request.form["age"]),
            "sex": int(request.form["sex"]),
            "cp": int(request.form["cp"]),
            "trestbps": float(request.form["trestbps"]),
            "chol": float(request.form["chol"]),
            "fbs": int(request.form["fbs"]),
            "restecg": int(request.form["restecg"]),
            "thalch": float(request.form["thalch"]),
            "exang": int(request.form["exang"]),
            "oldpeak": float(request.form["oldpeak"]),
            "slope": int(request.form["slope"]),
            "ca": int(request.form["ca"]),
            "thal": int(request.form["thal"])
        }

        input_df = pd.DataFrame([input_data])

        results = []

        # LR
        lr_prob = lr_pipeline.predict_proba(input_df)[0][1]
        results.append({
            "Model": "Logistic Regression",
            "Probability": round(lr_prob, 2),
            "Risk Level": map_risk(lr_prob)
        })

        # RF
        rf_prob = rf_pipeline.predict_proba(input_df)[0][1]
        results.append({
            "Model": "Random Forest",
            "Probability": round(rf_prob, 2),
            "Risk Level": map_risk(rf_prob)
        })

        # ANN
        ann_input = lr_pipeline.named_steps['preprocessing'].transform(input_df)
        ann_prob = ann_model.predict(ann_input)[0][0]
        results.append({
            "Model": "ANN",
            "Probability": round(float(ann_prob), 2),
            "Risk Level": map_risk(ann_prob)
        })

    return render_template("index.html", results=results, input_data=input_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth_result = authenticate_user(email, password)
        if auth_result["session_token"]:
            global session_token
            session_token = auth_result["session_token"]
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid credentials. Please try again.")

    return render_template("login.html")

@app.route('/logout')
def logout():
    global session_token
    session_token = None
    return redirect(url_for('login'))

@app.route('/patients')
@login_required
def patients():
    return render_template("patients.html")

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True