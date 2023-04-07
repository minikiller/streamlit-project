import streamlit as st
import time
from stqdm import stqdm
from time import sleep

# my_list = ["item 1", "item 2", "item 3"]
# progress_bar = st.progress(0)

# for i, item in enumerate(my_list):
#     # Do some work here...
#     time.sleep(1)  # Add a sleep to simulate work being done
#     # Update the progress bar
#     progress_bar.progress((i + 1) / len(my_list))
# Default to frontend only


class Dog():
    def show(self):
        for i in stqdm(range(50), backend=False, frontend=True):
            sleep(0.5)


dog = Dog()
dog.show()
