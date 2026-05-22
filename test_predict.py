import json
from pprint import pprint

from streamlit_app import predict_term_deposit


sample_values = {
    "age": 50,
    "job": "management",
    "marital": "married",
    "education": "tertiary",
    "default": "no",
    "balance": 5000,
    "housing": "yes",
    "loan": "no",
    "contact": "cellular",
    "month": "feb",
    "duration": 200,
    "campaign": 2,
    "previous": 0,
}


def run_test():
    try:
        result = predict_term_deposit(sample_values)
        out = {
            "class_1_probability": result["class_1_probability"],
            "prediction": bool(result["prediction"]),
            "threshold": result["threshold"],
        }
        print(json.dumps(out))
    except Exception as e:
        print("ERROR:", str(e))


if __name__ == "__main__":
    run_test()
