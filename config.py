import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "models")
    DATASET_PATH = os.path.join(BASE_DIR, "dataset/heart_disease_uci.csv")
    REQUIRED_MODELS = ["ann_model.keras", "lr_pipeline.pkl", "rf_pipeline.pkl"]

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY")

    VERSION = "1.0.0"
