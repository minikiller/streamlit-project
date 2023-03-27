import streamlit as st

# 设置侧边栏宽度
st.set_page_config(layout="wide")

# 创建侧边栏
sidebar = st.sidebar
sidebar.header("侧边栏标题")

# 在侧边栏中添加内容
with sidebar:
    sidebar.subheader("子标题1")
    sidebar.text("内容1")

    # 将内容放在第二列
    with st.sidebar:
        st.write("---")
    with st.sidebar:
        sidebar.subheader("子标题2")
        sidebar.text("内容2")
