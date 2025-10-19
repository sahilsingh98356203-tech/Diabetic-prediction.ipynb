# diabetes-app.py
# Streamlit app converted from notebook: Diabetic prediction (2).ipynb

import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

try:
    import joblib
except Exception:
    import pickle as joblib

# Helper functions
REPO_DIR = Path(__file__).resolve().parent
MODEL_PATH = REPO_DIR / "model.pkl"
DATA_PATH = REPO_DIR / "diabetes.csv"

@st.cache_data
def load_dataset(path=None):
    if path:
        df = pd.read_csv(path)
        return df
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return None

@st.cache_data
def train_model(df, target_col='Outcome', random_state=42):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state, stratify=y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    # Save both model and scaler together
    save_obj = {"model": model, "scaler": scaler}
    try:
        joblib.dump(save_obj, MODEL_PATH)
    except Exception:
        with open(MODEL_PATH, 'wb') as f:
            joblib.dump(save_obj, f)
    return model, scaler, acc, cm, report

@st.cache_data
def load_model():
    if MODEL_PATH.exists():
        try:
            obj = joblib.load(MODEL_PATH)
        except Exception:
            with open(MODEL_PATH, 'rb') as f:
                obj = joblib.load(f)
        # Expecting dict with 'model' and 'scaler'
        if isinstance(obj, dict) and 'model' in obj and 'scaler' in obj:
            return obj['model'], obj['scaler']
        # Otherwise assume obj is model and scaler missing
        return obj, None
    return None, None

def predict_input(model, scaler, input_df):
    X = input_df.values.reshape(1, -1) if input_df.ndim == 1 else input_df.values
    if scaler is not None:
        X = scaler.transform(X)
    proba = model.predict_proba(X)[0][1]
    pred = int(model.predict(X)[0])
    return pred, proba

# Streamlit UI
st.set_page_config(page_title="Diabetes Prediction App", layout='centered')
st.title("Diabetes Prediction — Streamlit App")

st.markdown("This app predicts the probability of diabetes using a RandomForest model. You can upload a dataset, train a model, or use an existing model (model.pkl) in the repo root.")

# Sidebar for inputs
st.sidebar.header("Patient input features")
# Default feature names (Pima dataset)
feature_defaults = {
    'Pregnancies': 0,
    'Glucose': 120,
    'BloodPressure': 70,
    'SkinThickness': 20,
    'Insulin': 79,
    'BMI': 32.0,
    'DiabetesPedigreeFunction': 0.472,
    'Age': 33
}

user_inputs = {}
for fname, default in feature_defaults.items():
    if isinstance(default, int):
        user_inputs[fname] = st.sidebar.number_input(fname, value=default)
    else:
        user_inputs[fname] = st.sidebar.number_input(fname, value=float(default))

input_df = pd.DataFrame([user_inputs])[list(feature_defaults.keys())]

# Model status
model, scaler = load_model()

col1, col2 = st.columns(2)
with col1:
    if model is not None:
        st.success("Loaded existing model from model.pkl")
    else:
        st.info("No model.pkl found in repo root.")

with col2:
    if DATA_PATH.exists():
        st.write(f"Found dataset file: {DATA_PATH.name}")
    else:
        st.write("No diabetes.csv found in repo root. You can upload one.")

# Upload data
uploaded_file = st.file_uploader("Upload a diabetes CSV file (optional). If not provided, will try to use diabetes.csv in repo.", type=["csv"]) 
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Uploaded dataset loaded")
    except Exception as e:
        st.error(f"Failed to read uploaded file: {e}")
        df = None
else:
    df = load_dataset()

# Train or retrain
st.markdown("---")
train_col1, train_col2 = st.columns(2)
with train_col1:
    if df is not None:
        st.write(f"Dataset shape: {df.shape}")
        if st.button("Train model on dataset"):
            if 'Outcome' not in df.columns:
                st.error("Dataset must contain an 'Outcome' column with 0/1 labels.")
            else:
                with st.spinner('Training model...'):
                    model, scaler, acc, cm, report = train_model(df)
                st.success(f"Model trained. Test accuracy: {acc:.3f}")
                st.write('Confusion matrix:')
                st.write(cm)
                st.write('Classification report:')
                st.json(report)
    else:
        st.write("No dataset available to train.")

with train_col2:
    if st.button("Retrain (force)"):
        if df is None:
            st.error("No dataset available to retrain. Upload a CSV first.")
        elif 'Outcome' not in df.columns:
            st.error("Dataset must contain 'Outcome' column.")
        else:
            with st.spinner('Retraining model...'):
                model, scaler, acc, cm, report = train_model(df)
            st.success(f"Model retrained. Test accuracy: {acc:.3f}")

st.markdown("---")

# Prediction
st.subheader("Make a prediction")
st.write("Enter patient values in the sidebar and press Predict.")
if model is None:
    st.warning("No model available. Train one or upload model.pkl to use prediction.")

if st.button("Predict"):
    if model is None:
        st.error("No model available to predict. Train or upload one.")
    else:
        try:
            pred, proba = predict_input(model, scaler, input_df.iloc[0])
            st.write(f"Predicted outcome: {pred} ({'Diabetic' if pred==1 else 'Not diabetic'})")
            st.write(f"Predicted probability of diabetes: {proba:.3f}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

st.markdown("---")

# Download model
if MODEL_PATH.exists():
    with open(MODEL_PATH, 'rb') as f:
        bytes_data = f.read()
    st.download_button("Download model.pkl", data=bytes_data, file_name='model.pkl')

st.markdown("\n---\nBuilt from notebook: Diabetic prediction (2).ipynb")

if __name__ == '__main__':
    st.write('Streamlit app ready')
