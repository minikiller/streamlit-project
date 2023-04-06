import streamlit as st
import time

my_list = ["item 1", "item 2", "item 3"]
progress_bar = st.progress(0)

for i, item in enumerate(my_list):
    # Do some work here...
    time.sleep(1)  # Add a sleep to simulate work being done
    # Update the progress bar
    progress_bar.progress((i + 1) / len(my_list))
