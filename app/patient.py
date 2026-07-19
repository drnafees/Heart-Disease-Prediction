class Prediction:
    def __init__(self, results):
        self.results = results

class MedicalHistory:
    def __init__(self, inputdata, results):
        self.input_data = inputdata
        self.prediction = Prediction(results)

class Patient:
    def __init__(self, mr, first_name, last_name, date_of_birth, gender, medical_history=None):
        self.mr = mr
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.medical_history = medical_history or MedicalHistory(inputdata={}, results=None)