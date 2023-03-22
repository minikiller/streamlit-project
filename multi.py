import streamlit as st
from multiapp import MultiPage

# Create an instance of the MultiPage class
app = MultiPage()

# Define your pages as functions


def page1():
    st.title('Page 1')
    st.write('This is page 1')


def page2():
    st.title('Page 2')
    st.write('This is page 2')


# Add your pages to the app
app.add_page("Page 1", page1)
app.add_page("Page 2", page2)

# Run the app
app.run()
