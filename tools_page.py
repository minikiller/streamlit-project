import streamlit as st
import time
from datetime import datetime

from process import Sector

# 表格数据
data = [
    ["名称", "总数"],
    ["东方财富-板块", "86"],
    ["东方财富-概念", "418"],
    ["同花顺-板块", "306"],
    ["同花顺-概念", "603"],
    ["通达信-板块", "132"],
    ["通达信-概念", "215"]
]

# 输出表格
table = "|".join(data[0]) + "\n" + "|".join(["---"]*len(data[0])) + "\n"
for i in range(1, len(data)):
    table += "|".join(data[i]) + "\n"
st.write(table)
# 注意的是，这种方法只适用于较小的表格。如果你需要输出大量的数据或具有更复杂结构的表格，你可能需要考虑使用Pandas等数据处理工具，或者寻找第三方Streamlit小部件来输出更高级的表格。






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
