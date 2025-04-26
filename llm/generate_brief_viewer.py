import streamlit as st
import os

def load_brief(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

st.set_page_config(page_title="Investor Brief Viewer", layout="wide")

st.title("Investor Brief")

brief_path = "output/ci-financial_wikipedia_brief.md"

if os.path.exists(brief_path):
    markdown_content = load_brief(brief_path)
    st.markdown(markdown_content)
else:
    st.error("Investor brief not found. Please run the generation script first.")
