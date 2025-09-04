import streamlit as st
from typing import Optional, List, Dict, Union


# Page Layout Components
def page_container(title: str, description: Optional[str] = None, show_sidebar: bool = True) -> None:
    """Creates a standard page layout with title and optional description.
    
    Usage:
        page_container("Recipe Manager", "Manage your favorite recipes")
    """
    st.title(title)
    if description:
        st.write(description)
    
    # Return the container for potential future use
    return st.container()

def section_container(title: str, border: bool = True, padding: bool = True):
    """Creates a section with title and customizable border/padding.
    
    Usage:
        with section_container("Add New Recipe"):
            st.write("Section content here")
    """
    container = st.container(border=border)
    with container:
        st.subheader(title)
        if padding:
            st.write("")  # Adds some spacing
    return container

def tabbed_container(tabs_dict: Dict[str, callable]) -> None:
    """Creates tabs from a dictionary of {tab_name: content_function}.
    
    Usage:
        tabs = {
            "Details": lambda: st.write("Tab 1 content"),
            "History": lambda: st.write("Tab 2 content")
        }
        tabbed_container(tabs)
    """
    tabs = st.tabs(list(tabs_dict.keys()))
    for tab, content_func in zip(tabs, tabs_dict.values()):
        with tab:
            content_func()


# Form Components
def text_input_group(
    label: str,
    placeholder: str = "",
    required: bool = False,
    default: str = "",
    help_text: str = ""
) -> str:
    """Creates a text input field with label and validation.
    
    Usage:
        name = text_input_group("Recipe Name", required=True)
    """
    input_value = st.text_input(
        label=f"{label}{'*' if required else ''}",
        placeholder=placeholder,
        value=default,
        help=help_text
    )
    
    if required and not input_value:
        st.warning(f"{label} is required")
    
    return input_value

def number_input_group(
    label: str,
    min_val: float = 0,
    max_val: float = 100,
    default: float = None,
    required: bool = False,
    help_text: str = "",
    step: float = 1
) -> float:
    """Creates a number input with constraints and validation.
    
    Usage:
        servings = number_input_group("Servings", min_val=1, max_val=20)
    """
    if default is None:
        default = min_val
        
    value = st.number_input(
        label=f"{label}{'*' if required else ''}",
        min_value=min_val,
        max_value=max_val,
        value=default,
        help=help_text,
        step=step
    )
    
    if required and value == min_val:
        st.warning(f"{label} is required")
        
    return value

def selection_group(
    label: str,
    options: List[str],
    multiple: bool = False,
    default: Union[str, List[str]] = None,
    required: bool = False
) -> Union[str, List[str]]:
    """Creates a dropdown/multi-select component.
    
    Usage:
        categories = selection_group(
            "Categories", 
            ["Breakfast", "Lunch", "Dinner"],
            multiple=True
        )
    """
    if multiple:
        value = st.multiselect(
            label=f"{label}{'*' if required else ''}",
            options=options,
            default=default if default else []
        )
    else:
        value = st.selectbox(
            label=f"{label}{'*' if required else ''}",
            options=options,
            index=0 if default is None else options.index(default)
        )
    
    if required and not value:
        st.warning(f"{label} is required")
        
    return value


# ---------- OLD COMPONENTS -------------
# Text Components
def heading(heading_text: str):
    st.header(heading_text)

def subheading(subheading_text: str):
    st.subheader(subheading_text)

def paragraph(paragraph_text: str):
    st.write(paragraph_text)


# Layout Components
def full_width_layout(heading_text: str, content_layout: str):
    with st.container(border=True):
        heading(heading_text)
        if content_layout == "two_columns":
            two_column_layout("Left Subheading", "Right Subheading")

def two_column_layout(left_subheading: str, right_subheading: str):
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            subheading(left_subheading)
    with col2:
        with st.container(border=True):
            subheading(right_subheading)


# Debugging Components
def code_box(code_text: str, language: str):
    with st.container(border=True):
        subheading("Output")
        
        with st.expander("View Code"):
            st.code(code_text, language=language)
