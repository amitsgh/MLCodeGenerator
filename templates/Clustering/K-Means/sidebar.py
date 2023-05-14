import streamlit as st

def show():
    inputs = {}
    with st.sidebar:
        st.write("## Input data")
        inputs["data"] = st.selectbox(
            "Which data set do you want to use?",
            ("Synthetic data",),
        )
        if inputs["data"] == "Synthetic data":
            inputs['n_samples'] = st.number_input(
                "number of data points", 100, None, 1000,
            )
            inputs['n_features'] = st.number_input(
                "number of features in data set", 2, None, 2,
            )
            inputs['n_centers'] = st.number_input(
                "number of cluster centers", 3, None, 3,
            )
            inputs['cluster_std'] = st.number_input(
                "Cluster standard deviation", 0.1, None, 1.0, 
            )
        st.write("## Model Hyperparameter")
        inputs['n_centroids'] = st.number_input(
            "number of cluster/ number of centroids", 2, None, 3)
        inputs['max_iter'] = st.number_input(
            "Maximum number of interation to perform in single run?", 100, None, 300,
        )
    return inputs

if __name__ == "__main__":
    show()