import os
import joblib
import tensorflow as tf
import pandas as pd
from config import Config

class PredictionEngine:
    model_path = Config.MODEL_PATH

    def __init__(self):

        missing_models = [m for m in Config.REQUIRED_MODELS if not os.path.exists(f"{self.model_path}/{m}")]
        if missing_models:
            print(f"Warning: Missing model(s) - {', '.join(missing_models)}. Training now...")
            from app.services.train_models import train_models
            train_models()

        try:
            self.ann_model = tf.keras.models.load_model(f"{self.model_path}/ann_model.keras")
            self.lr_pipeline = joblib.load(f"{self.model_path}/lr_pipeline.pkl")
            self.rf_pipeline = joblib.load(f"{self.model_path}/rf_pipeline.pkl")
        except Exception as e:
            print(f"Error loading models: {e}. Prediction Engine will not function properly.")
            self.ann_model = self.lr_pipeline = self.rf_pipeline = None

    def map_risk(self, prob):
        if prob < 0.33: return "Low Risk"
        return "Medium Risk" if prob < 0.66 else "High Risk"

    def get_predictions(self, input_data):
        input_df = pd.DataFrame([input_data])
        results = []
        
        # LR & RF
        for name, pipe in [("Logistic Regression", self.lr_pipeline), ("Random Forest", self.rf_pipeline)]:
            prob = pipe.predict_proba(input_df)[0][1]
            results.append({"Model": name, "Probability": round(prob, 2), "Risk Level": self.map_risk(prob)})

        # ANN
        ann_input = self.lr_pipeline.named_steps['preprocessing'].transform(input_df)
        ann_prob = self.ann_model.predict(ann_input)[0][0]
        results.append({"Model": "ANN", "Probability": round(float(ann_prob), 2), "Risk Level": self.map_risk(ann_prob)})
        
        return results