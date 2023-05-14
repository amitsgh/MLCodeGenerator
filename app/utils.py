import streamlit as st
import base64
import uuid
import re
import jupytext
from bokeh.models.widgets import Div
import math
import importlib.util


def import_from_file(module_name: str, filepath: str):
    """
    Imports a module from file.

    Args:
        module_name (str): Assigned to the module's __name__ parameter (does not 
            influence how the module is named outside of this function)
        filepath (str): Path to the .py file

    Returns:
        The module
    """
    try:
        # Create a module spec from the file path
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        # Create a module from the spec
        module = importlib.util.module_from_spec(spec)
        # Execute the module's code
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        # Handle any exceptions that may occur during module import
        st.error(f"Error importing module {module_name}: {e}")


def notebook_header(text):
    """
    Insert section header into a jinja file, formatted as notebook cell.
    
    Leave 2 blank lines before the header.
    """
    return f"""# # {text}"""


def code_header(text):
    """
    Insert section header into a jinja file, formatted as Python comment.
    
    Leave 2 blank lines before the header.
    """
    seperator_len = (75 - len(text)) / 2
    seperator_len_left = math.floor(seperator_len)
    seperator_len_right = math.ceil(seperator_len)
    return f"# {'-' * seperator_len_left} {text} {'-' * seperator_len_right}"


def to_notebook(code):
    """Converts Python code to Jupyter notebook format."""
    try:
        # Read the Python code as a notebook
        notebook = jupytext.reads(code, fmt="py")
        # Write the notebook as a .ipynb file
        return jupytext.writes(notebook, fmt="ipynb")
    except Exception as e:
        # Handle any exceptions that may occur during notebook conversion
        st.error(f"Error converting code to notebook: {e}")


def open_link(url, new_tab=True):
    """Dirty hack to open a new web page with a streamlit button."""
    try:
        if new_tab:
            # Open the URL in a new tab or window
            js = f"window.open('{url}')"
        else:
            # Open the URL in the current tab
            js = f"window.location.href = '{url}'"
        # Create an HTML div with the JavaScript code to open the URL
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        # Display the HTML div with the Bokeh chart widget
        st.bokeh_chart(div)
    except Exception as e:
        # Handle any exceptions that may occur during link opening
        st.error(f"Error opening link: {e}")


def download_button(object_to_download, download_filename, button_text):
    try:
        # Try encoding object_to_download as a string and then encoding as base64
        b64 = base64.b64encode(object_to_download.encode()).decode()
    except AttributeError:
        # If object_to_download is already bytes, just encode as base64
        b64 = base64.b64encode(object_to_download).decode()

    # Generate unique ID for button element
    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    # Define custom CSS styles for button element
    custom_css = f""" 
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
            }}
        </style> """

    # Generate HTML for download link with button element
    dl_link = (
        custom_css
        + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br><br>'
    )

    # Render the download link with button element using Streamlit
    st.markdown(dl_link, unsafe_allow_html=True)