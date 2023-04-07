import streamlit as st
import time
from datetime import datetime

from process import Sector

# Define the date ranges
date_ranges = [(datetime(2021, 1, 1), datetime(2021, 7, 1)),
               (datetime(2021, 7, 1), datetime(2022, 1, 1)),
               (datetime(2022, 1, 1), datetime(2022, 7, 1)),
               (datetime(2022, 7, 1), datetime(2023, 1, 1)),
               (datetime(2023, 7, 1), datetime(2023, 7, 1)),
               ]

file_dict = {"20210101": "Hist_20210101_20210701", "20210701": "Hist_20210701_20220101",
             "20220101": "Hist_20220101_20220701", "20220701": "Hist_20220701_20230101",
             "20230101": "Hist_20230101_20230701", }


selected_date = st.date_input('Select a month:', datetime(
    2022, 3, 1), min_value=datetime(2021, 1, 1), max_value=datetime(2023, 3, 1), )

selected_year = selected_date.year
selected_month = selected_date.month

st.write('Selected year:', selected_year)
st.write('Selected month:', selected_month)


def get_file_name(input_date):
    for date_range in date_ranges:
        # Check if the datetime is within the range
        if date_range[0].date() <= input_date < date_range[1].date():
            result = date_range[0]
            print("Date is within the range")
            break
        # else:
        #     print("Date is outside the range")
    return result.strftime('%Y%m%d')


def my_button_callback():
    progress_bar = st.progress(0)
    file_name = file_dict[get_file_name(selected_date)]
    sector = Sector(selected_date.strftime('%Y-%m-%d'), file_name)
    sector.pipeline()
    # for i in range(100):
    #     # Do some computation here
    #     time.sleep(0.1)
    #     # Update the progress bar with the current progress
    #     progress_bar.progress(i + 1)

    # # Replace the progress bar with the final output
    # progress_bar.empty()
    # st.write('Task finished!')


# st.session_state.disabled

if st.button('run me'):
    my_button_callback()
