import streamlit as st
import os

DISTANCE_METRICS = {
    "Euclidean": "euclidean",
    "Manhattan": "manhattan"
}

SEARCH_ALGORITHM = {
    "Auto": "auto",
    "BallTree": "ball_tree",
    "KDTree": "kd_tree",
    "Brute-Force search": "brute"
}

CLASSIFICATION_DATASETS = {
    "Diabetes": "diabetes",
    "Iris": "iris",
    "Pendigits": "pendigits"
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
        inputs['k'] = st.sidebar.number_input(
            "k?", 1, None, 10,)
        algo = st.selectbox(
            "Which nearest neighbor search algorithm do you want to use?",
            list(SEARCH_ALGORITHM.keys()))
        inputs["search_algo"] = SEARCH_ALGORITHM[algo]
        dist = st.selectbox(
            "Which distance metric do you want to use?",
            list(DISTANCE_METRICS.keys()))
        inputs["metric"] = DISTANCE_METRICS[dist]

        inputs["visualization_status"] = st.checkbox('Visualization?', False)
        if inputs["visualization_status"]:
            inputs['plots'] = st.multiselect("What metrics to plot?", ('ROC Curve', 'Precision-Recall Curve'))
    return inputs

if __name__ == "__main__":
    show()