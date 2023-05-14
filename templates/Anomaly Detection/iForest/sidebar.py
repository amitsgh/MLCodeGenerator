import streamlit as st

ANOMALY_DETECTION_DATASETS = {
    "Glass": "glass",
    "Heart Disease": "heart_disease",
    "KDDCup99": "kddcup99",
    "Mnist": "mnist"
}

def show():
    """Shows the sidebar components for the template and returns user inputs as dict."""
    
    inputs = {}

    with st.sidebar:
        st.write("## Input data")
        inputs["data"] = st.selectbox(
            "Which data set do you want to use?",
            ("Synthetic data", "Benchmark data"),
        )
        if inputs["data"] == "Synthetic data":
            inputs['contamination'] = st.number_input(
                "Contamination (percentage of outliers)", 0.0, None, 0.1, format="%f",
            )
            inputs['n_train'] = st.number_input(
                "number of training data points", 100, None, 200,
            )
            inputs['n_test'] = st.number_input(
                "number of testing data points", 50, None, 100,
            )
            inputs['n_features'] = st.number_input(
                "number of features in data set", 1, None, 2,
            )
        elif inputs["data"] == "Benchmark data":
            dataset = st.selectbox(
                "Which one?", list(ANOMALY_DETECTION_DATASETS.keys())
            )
            inputs["dataset"] = ANOMALY_DETECTION_DATASETS[dataset]
        st.write("## Model Hyperparameter")
        inputs['samples'] = st.number_input(
            "samples?", 2, None, 128,
        )
        inputs['trees'] = st.number_input(
            "trees?", 100, None, 100,
        )
        inputs["visualization_status"] = st.checkbox('Visualization?', False)
        if inputs["visualization_status"]:
            inputs["save"] = st.checkbox('Do you want to save the figure?', False)
    return inputs


if __name__ == "__main__":
    show()