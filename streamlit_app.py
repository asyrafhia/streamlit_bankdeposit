from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
ENCODER_PATH = MODEL_DIR / "ohe.pkl"
MODEL_PATH = MODEL_DIR / "cbc_optuna.pkl"
DEFAULT_THRESHOLD = 0.4963388427754832

INPUT_COLUMNS = [
    "age",
    "job",
    "marital",
    "education",
    "default",
    "balance",
    "housing",
    "loan",
    "contact",
    "month",
    "duration",
    "campaign",
    "previous",
]

CATEGORICAL_OPTIONS = {
    "job": [
        "admin.",
        "blue-collar",
        "entrepreneur",
        "housemaid",
        "management",
        "retired",
        "self-employed",
        "services",
        "student",
        "technician",
        "unemployed",
        "unknown",
    ],
    "marital": ["divorced", "married", "single"],
    "education": ["primary", "secondary", "tertiary", "unknown"],
    "default": ["no", "yes"],
    "housing": ["no", "yes"],
    "loan": ["no", "yes"],
    "contact": ["cellular", "telephone", "unknown"],
    "month": ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"],
}

NUMERIC_DEFAULTS = {
    "age": 50,
    "balance": 5000,
    "duration": 2000,
    "campaign": 2,
    "previous": 2,
}


@st.cache_resource
def load_artifacts() -> tuple[object, object]:
    encoder = joblib.load(ENCODER_PATH)
    model = joblib.load(MODEL_PATH)
    return encoder, model


def build_input_frame(values: dict[str, object]) -> pd.DataFrame:
    ordered_values = {column: values[column] for column in INPUT_COLUMNS}
    return pd.DataFrame([ordered_values], columns=INPUT_COLUMNS)


def predict_term_deposit(
    values: dict[str, object],
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, object]:
    encoder, model = load_artifacts()
    input_frame = build_input_frame(values)
    encoded_frame = encoder.transform(input_frame)
    probabilities = model.predict_proba(encoded_frame)
    class_1_probability = float(probabilities[0][1])
    prediction = class_1_probability >= threshold

    return {
        "input_frame": input_frame,
        "encoded_frame": encoded_frame,
        "class_1_probability": class_1_probability,
        "prediction": prediction,
        "threshold": threshold,
        "prediction_label": (
            "The client is predicted to subscribe a term deposit."
            if prediction
            else "The client is predicted not to subscribe a term deposit."
        ),
    }


def numeric_input(label: str, key: str, default: int, min_value: int, max_value: int, step: int = 1) -> int:
    return st.number_input(
        label,
        min_value=min_value,
        max_value=max_value,
        value=default,
        step=step,
        key=key,
    )


def main() -> None:
    st.set_page_config(page_title="Bank Term Deposit Predictor", page_icon="📈", layout="wide")

    st.title("Bank Term Deposit Predictor")
    st.caption("Inference-only Streamlit app using the saved encoder and CatBoost model.")

    if not ENCODER_PATH.exists() or not MODEL_PATH.exists():
        st.error(
            "Required model artifacts are missing. Expected `ohe.pkl` and `cbc_optuna.pkl` in the `models/` folder."
        )
        st.stop()

    with st.sidebar:
        st.header("Prediction Settings")
        threshold = st.slider(
            "Decision threshold",
            min_value=0.0,
            max_value=1.0,
            value=float(DEFAULT_THRESHOLD),
            step=0.001,
        )
        st.write("Higher threshold makes the positive class harder to predict.")

        use_sample = st.button("Load sample values")

    sample_values = {
        "age": 50,
        "job": "management",
        "marital": "married",
        "education": "tertiary",
        "default": "yes",
        "balance": 5000,
        "housing": "yes",
        "loan": "yes",
        "contact": "cellular",
        "month": "feb",
        "duration": 2000,
        "campaign": 2,
        "previous": 2,
    }

    if "form_values" not in st.session_state:
        st.session_state.form_values = sample_values.copy()

    if use_sample:
        st.session_state.form_values = sample_values.copy()
        st.rerun()

    col_left, col_right = st.columns(2)

    with col_left:
        age = numeric_input("Age", "age", int(st.session_state.form_values["age"]), 18, 100)
        job = st.selectbox("Job", CATEGORICAL_OPTIONS["job"], index=CATEGORICAL_OPTIONS["job"].index(st.session_state.form_values["job"]), key="job")
        marital = st.selectbox("Marital status", CATEGORICAL_OPTIONS["marital"], index=CATEGORICAL_OPTIONS["marital"].index(st.session_state.form_values["marital"]), key="marital")
        education = st.selectbox("Education", CATEGORICAL_OPTIONS["education"], index=CATEGORICAL_OPTIONS["education"].index(st.session_state.form_values["education"]), key="education")
        default = st.selectbox("Default credit?", CATEGORICAL_OPTIONS["default"], index=CATEGORICAL_OPTIONS["default"].index(st.session_state.form_values["default"]), key="default")
        balance = numeric_input("Balance", "balance", int(st.session_state.form_values["balance"]), -100000, 1000000, step=1)

    with col_right:
        housing = st.selectbox("Housing loan?", CATEGORICAL_OPTIONS["housing"], index=CATEGORICAL_OPTIONS["housing"].index(st.session_state.form_values["housing"]), key="housing")
        loan = st.selectbox("Personal loan?", CATEGORICAL_OPTIONS["loan"], index=CATEGORICAL_OPTIONS["loan"].index(st.session_state.form_values["loan"]), key="loan")
        contact = st.selectbox("Contact type", CATEGORICAL_OPTIONS["contact"], index=CATEGORICAL_OPTIONS["contact"].index(st.session_state.form_values["contact"]), key="contact")
        month = st.selectbox("Last contact month", CATEGORICAL_OPTIONS["month"], index=CATEGORICAL_OPTIONS["month"].index(st.session_state.form_values["month"]), key="month")
        duration = numeric_input("Duration", "duration", int(st.session_state.form_values["duration"]), 0, 100000, step=1)
        campaign = numeric_input("Campaign", "campaign", int(st.session_state.form_values["campaign"]), 0, 1000, step=1)
        previous = numeric_input("Previous contacts", "previous", int(st.session_state.form_values["previous"]), 0, 1000, step=1)

    current_values = {
        "age": int(age),
        "job": job,
        "marital": marital,
        "education": education,
        "default": default,
        "balance": int(balance),
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "month": month,
        "duration": int(duration),
        "campaign": int(campaign),
        "previous": int(previous),
    }

    st.session_state.form_values = current_values.copy()

    submit = st.button("Predict", type="primary")

    if submit:
        with st.spinner("Running prediction..."):
            result = predict_term_deposit(current_values, threshold)

        probability_percentage = result["class_1_probability"] * 100
        predicted_label = "Subscribe" if result["prediction"] else "Not subscribe"

        metric_left, metric_right, metric_threshold = st.columns(3)
        metric_left.metric("Prediction", predicted_label)
        metric_right.metric("Probability", f"{probability_percentage:.2f}%")
        metric_threshold.metric("Threshold", f"{result['threshold']:.3f}")

        if result["prediction"]:
            st.success(result["prediction_label"])
        else:
            st.warning(result["prediction_label"])

        with st.expander("Prediction details"):
            st.write("Input row")
            st.dataframe(result["input_frame"], use_container_width=True)
            st.write("Encoded row")
            st.dataframe(result["encoded_frame"], use_container_width=True)

        st.info(
            "This app uses the saved one-hot encoder and CatBoost model from the `models/` folder. The threshold can be adjusted from the sidebar."
        )

    with st.expander("What this app uses"):
        st.markdown(
            """
            - Saved encoder: `models/ohe.pkl`
            - Saved model: `models/cbc_optuna.pkl`
            - Inference schema: 13 columns from the deployed notebook
            - No retraining, no Google Sheets dependency
            """
        )


if __name__ == "__main__":
    main()