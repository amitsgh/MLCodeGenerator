import streamlit as st

CLASSIFICATION_DATASETS = {
    "Diabetes": "diabetes",
    "Iris": "iris",
    "Pendigits": "pendigits"
}


def show():
    inputs = {}

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
        inputs['criterion'] = st.selectbox(
            "Which funtion to measure the quality of split you want to use?", ("Gini", "Entropy"))
        inputs['max_depth'] = st.number_input(
            "The maximum depth of the tree", 1, 20, 1
        )
        inputs['splitter'] = st.radio(
            "Which strategy do you want to use to choose the split at each node?", ("Best", "Random")
        )
        inputs["visualization_status"] = st.checkbox('Visualization?', False)
        if inputs["visualization_status"]:
            inputs['plots'] = st.multiselect("What metrics to plot?", ('ROC Curve', 'Precision-Recall Curve'))
    return inputs

if __name__ == "__main__":
    show()