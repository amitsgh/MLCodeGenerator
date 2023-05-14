import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
import uuid
from github import Github
from dotenv import load_dotenv
from collections import defaultdict
import utils


# Set page title and favicon.
st.set_page_config(
    page_title="ML Code Generator",
)

# Set up github access for "Open in Colab" button.
load_dotenv()  # load environment variables from .env file
print(os.getenv('REPO_NAME'))
if os.getenv("GITHUB_TOKEN") and os.getenv("REPO_NAME"):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(os.getenv("REPO_NAME"))
    colab_enabled = True

    def add_to_colab(notebook):
        """Adds notebook to Colab by pushing it to Github repo and returning Colab link."""
        notebook_id = str(uuid.uuid4())
        repo.create_file(
            f"notebooks/{notebook_id}/generated-notebook.ipynb",
            f"Added notebook {notebook_id}",
            notebook,
        )
        colab_link = f"http://colab.research.google.com/github/{os.getenv('REPO_NAME')}/blob/main/notebooks/{notebook_id}/generated-notebook.ipynb"
        return colab_link
else:
    colab_enabled = False


# Page title.
st.title("Machine Learning Code Generator")

# st.markdown("-----")
st.markdown("<br>", unsafe_allow_html=True)
"""

Generate your machine learning starter code in five simple steps. 

1. Select Task (Anomaly Detection or Classification or Clustering).
2. Select Algorithm
3. Specify data set and hyperparameters.
4. Starter code will be generated below.
5. Download the code.
"""

st.markdown("<br>", unsafe_allow_html=True)

# templates = {
#     'Anomaly Detection': {
#         'LOF': 'templates/Anomaly Detection/LOF',
#         'iForest': 'templates/Anomaly Detection/iForest',
#         'kNN': 'templates/Anomaly Detection/kNN'
#     },
#     'Classification': {
#         'Logistic Regression': 'templates/Classification/Logistic Regression',
#         'kNN': 'templates/Classification/kNN',
#         'SVM': 'templates/Classification/SVM',
#         'Random Forest': 'templates/Classification/Random Forest',
#         'Decision Tree': 'templates/Classification/Decision Trees'
#     },
#     'Clustering': {
#         'DBSCAN': 'templates/Clustering/DBSCAN',
#         'K-Means': 'templates/Clustering/K-Means',
#         'OPTICS': 'templates/Clustering/OPTICS',
#     }
# }

template_dir = 'templates'

template_dirs = defaultdict(dict)

for dirpath, dirnames, filenames in os.walk(template_dir):
    task = os.path.basename(dirpath)
    print(task)
    if not task:
        continue
    for framework in dirnames:
        if framework == '__pycache__':
            continue
        print(framework, '------')
        template_dirs[task][framework] = os.path.join(template_dir, task, framework)

del template_dirs['templates']

import json
print(json.dumps(template_dirs, indent=4))

# Show selectors for task and framework in sidebar (based on template_dict). These
# selectors determine which template (from template_dict) is used (and also which
# template-specific sidebar components are shown below).
with st.sidebar:
    st.write("## Task")
    task = st.selectbox(
        "Which problem do you want to solve?", list(template_dirs.keys())
    )
    if isinstance(template_dirs[task], dict):
        framework = st.selectbox(
            "In which framework?", list(template_dirs[task].keys())
        )
        template_path = template_dirs[task][framework]
    else:
        template_path = template_dirs[task]

# Show template-specific sidebar components (based on sidebar.py in the template dir).
template_sidebar = utils.import_from_file(
    "template_sidebar", os.path.join(template_path, "sidebar.py")
)

inputs = template_sidebar.show()


print(template_path, '000000000000000000000000')
# Generate code and notebook based on template.py.jinja file in the template dir.
env = Environment(
    loader=FileSystemLoader(template_path), 
    trim_blocks=True, 
    lstrip_blocks=True,
)

template = env.get_template("code-template.py.jinja")
code = template.render(header=utils.code_header, notebook=False, **inputs)
notebook_code = template.render(header=utils.notebook_header, notebook=True, **inputs)
notebook = utils.to_notebook(notebook_code)


st.write("")  # add vertical space
col1, col2, col3 = st.columns(3)
open_colab = col1.button("🚀 Open in Colab")  # logic handled further down
with col2:
    utils.download_button(code, "generated-code.py", "🐍 Download (.py)")
with col3:
    utils.download_button(notebook, "generated-notebook.ipynb", "📓 Download (.ipynb)")
colab_error = st.empty()


st.code(code)


# Handle "Open Colab" button. Down here because to open the new web page, it
# needs to create a temporary element, which we don't want to show above.
if open_colab:
    if colab_enabled:
        colab_link = add_to_colab(notebook)
        utils.open_link(colab_link)
    else:
        colab_error.error(
            """
            **Colab support is disabled.** (If you are hosting this: Create a Github 
            repo to store notebooks and register it via a .env file)
            """
        )