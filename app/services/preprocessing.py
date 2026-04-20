import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def create_preprocessor(df):

    X = df.drop(["id", "num", "dataset"], axis=1)
    X = X.replace("?", np.nan)

    categorical_cols = X.select_dtypes(include=["object", "string"]).columns
    numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns

    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(drop="first", handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", num_pipeline, numerical_cols),
        ("cat", cat_pipeline, categorical_cols)
    ])

    return preprocessor, X