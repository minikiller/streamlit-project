import streamlit as st
from pathlib import Path

# Read the contents of the markdown file
file_path = Path("./README.md")
markdown_text = file_path.read_text()
st.markdown("# Main page 🎈")
# Display the markdown text using st.markdown()
st.markdown(markdown_text)
st.sidebar.markdown("# Main page 🎈")
