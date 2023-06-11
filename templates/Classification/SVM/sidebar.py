import streamlit as st
import os

CLASSIFICATION_DATASETS = {
    "Diabetes": "diabetes",
    "Iris": "iris",
    "Pendigits": "pendigits"
}

KERNELS = {
    "RBF": 'rbf',
    "Linear": "linear",
    "Polynomial": "poly",
    "Sigmoid": "sigmoid"
}

def show():
    inputs = {}

    repo_name = os.getenv("REPO_NAME")
    inputs["repo_name"] = repo_name

    with st.sidebar:
        st.write("## Input data")
        inputs["data"] = st.selectbox(
            "Which data set do you want to use?",
            ("Synthetic data", "Benchmark data"),
        )
        if inputs["data"] == "Synthetic data":
            inputs['n_samples'] = st.number_input(
                "number of data points", 100, None, 1000,
            )
            inputs['n_features'] = st.number_input(
                "number of features in data set", 10, None, 10,
            )
            inputs['n_classes'] = st.number_input(
                "number of classes", 2, None, 2,
            )
        elif inputs["data"] == "Benchmark data":
            dataset = st.selectbox(
                "Which one?", list(CLASSIFICATION_DATASETS.keys())
            )
            inputs["dataset"] = CLASSIFICATION_DATASETS[dataset]
        
        st.write("## Model Hyperparameter")
        inputs['C'] = st.number_input(
            "C (Regularization parameter)?", 1.00, 10.00, step = 0.01)
        kernel = st.selectbox(
            "Which kernel do you want to use?",
            list(KERNELS.keys()))
        inputs["kernel"] = KERNELS[kernel]
        if kernel == "Polynomial":
            inputs["degree"] = st.number_input(
                "Degree of Polynomial Kernel", 1, 10, 3
            )
        if (kernel == "RBF" or kernel == "Polynomial" or kernel == "Sigmoid"):
            inputs["gamma"] = st.selectbox("Gamma (Kernel Coefficient)", ("scale", "auto"))
        inputs["visualization_status"] = st.checkbox('Visualization?', False)
        if inputs["visualization_status"]:
            inputs['plots'] = st.multiselect("What metrics to plot?", ('ROC Curve', 'Precision-Recall Curve'))
    return inputs

if __name__ == "__main__":
    show()