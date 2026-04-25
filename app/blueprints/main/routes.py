from flask import Blueprint, render_template, request, session

from app.blueprints.auth.utils import login_required
from app.services.ai_service import AIService
from database.models import Patient, db

main_bp = Blueprint("main", __name__)
ai_service = AIService()


@main_bp.route("/", methods=["GET", "POST"])
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
            "thal": int(request.form["thal"]),
        }

        results = ai_service.get_predictions(input_data)
        session["results"] = results
        session["input_data"] = input_data

    return render_template("index.html", results=results, input_data=input_data)


@main_bp.route("/patients", methods=["GET", "POST"])
@login_required
def patients():
    if request.method == "POST":
        new_patient = Patient(
            mr=request.form["mr_number"],
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            date_of_birth=request.form["dob"],
            gender=request.form["gender"],
            medical_history={
                "history": session["input_data"],
                "result": session["results"],
            },
        )
        db.session.add(new_patient)
        db.session.commit()
        print(f"Added new patient: {new_patient}")

    patients = Patient.query.all()
    output = []
    patient_data = {}
    for patient in patients:
        patient_data = {
            "mr": patient.mr,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": patient.date_of_birth.isoformat(),
            "medical_history": patient.medical_history,
            "created_at": patient.created_at.isoformat(),
        }
        output.append(patient_data)

    return render_template("patients.html", patients=output)


@main_bp.route("/patient/<mr>", methods=["GET"])
@login_required
def patient_detail(mr):
    patient = Patient.query.get_or_404(mr)
    return render_template(
        "patient_detail.html",
        patient=patient,
        results=patient.medical_history["result"],
    )


@main_bp.route("/about")
def about():
    return render_template("about.html")
