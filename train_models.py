#%%
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from preprocessing import create_preprocessor

df = pd.read_csv("data/raw/heart_disease_uci.csv")
df.columns = df.columns.str.strip()
y = (df["num"] > 0).astype(int)

preprocessor, X = create_preprocessor(df)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

lr_pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("model", LogisticRegression(max_iter=1000))
])
lr_pipeline.fit(X_train, y_train)
joblib.dump(lr_pipeline, "models/lr_pipeline.pkl")

rf_pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42))
])
rf_pipeline.fit(X_train, y_train)
joblib.dump(rf_pipeline, "models/rf_pipeline.pkl")

X_train_ann = lr_pipeline.named_steps['preprocessing'].transform(X_train)
X_test_ann = lr_pipeline.named_steps['preprocessing'].transform(X_test)
input_dim = X_train_ann.shape[1]

ann_model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(32, activation="relu", input_shape=(input_dim,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

ann_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss="binary_crossentropy",
                  metrics=["accuracy"])

ann_model.fit(X_train_ann, y_train, epochs=50, batch_size=16,
              validation_data=(X_test_ann, y_test), verbose=0)

ann_model.save("models/ann_model.keras")

print("All models trained and saved successfully!")