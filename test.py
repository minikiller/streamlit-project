import streamlit as st

# Create a text input for the date
date = st.slider("请输入日期（格式为YYYYMMDD）：")

# Convert the input date to an integer
date = int(date)

# Define the range of dates
start_date = 20220101
end_date = 20221231

list=[1,2,3,4]

# Check if the input date is within the range of dates
if date in list:
    st.write("Yes, the date is within the range!")
else:
    st.write("No, the date is not within the range.")
