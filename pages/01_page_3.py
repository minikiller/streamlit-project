import streamlit as st
import pandas as pd

st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")
df = pd.read_csv(
    f"./data/constant/data.csv", dtype={"股票代码": object})
print(df.info())