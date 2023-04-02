import streamlit as st

# 定义选项卡的标签和内容
tabs = {
    "Tab 1": "This is the content of Tab 1",
    "Tab 2": "This is the content of Tab 2",
    "Tab 3": "This is the content of Tab 3"
}

# 创建选项卡
selected_tab = st.sidebar.selectbox("Select a tab", list(tabs.keys()))

# 创建选项卡的内容
tab_content = [tabs[label] for label in tabs.keys()]

# 显示选项卡
current_tab = st.tabs(tabs.keys(), tab_content)[selected_tab]
