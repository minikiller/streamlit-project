import streamlit as st
import pandas as pd
# 定义 Streamlit 应用程序
import plotly.express as px


def main():
    st.title("在 Jupyter Notebook 中使用 Streamlit 示例")

    # 添加一些文本
    st.write("这是一个在 Jupyter Notebook 中使用 Streamlit 的简单示例。")

    # 添加一个交互式小部件
    name = st.text_input("请输入您的名字：")

    # 显示结果
    if name:
        st.write("你好，" + name + "！")
    # 添加一个交互式小部件
    value = st.selectbox("请输入您的名字：", ["first", "data"])

    # 显示结果
    df = pd.read_csv(
        "data/hist.csv", parse_dates=['日期'], index_col=0, dtype={"股票编号": object})
    if value:
        st.write("你好，" + value + "！")
    dates = df.index.unique().sort_values().to_list()
    dates_list = [date.strftime('%Y-%m-%d') for date in dates]

    x_axis = st.sidebar.selectbox('选择日期', dates_list)
    st.write('You selected:', x_axis)
    y_axis = st.sidebar.selectbox('Select the y-axis', df.columns)

    # create a slider widget for the low value
    low_value = st.sidebar.slider("Select the low value", 0, 99, 0)

    # create a slider widget for the max value
    max_value = st.sidebar.slider("Select the max value", low_value, 100, 100)

    # display the selected range
    st.write("You selected a range from", low_value, "to", max_value)
    # Display DataFrame
    st.subheader("DataFrame")
    df = df.loc[x_axis]
    st.dataframe(df)

    # create a date input widget
    date = st.date_input("Select a date")
    time = st.time_input("Select a time")

    # create a checkbox widget
    options = ["Option 1", "Option 2", "Option 3"]
    selected_options = st.multiselect("Select options", options)
    # fig = px.treemap(df, path=[px.Constant('All'), '股票编号'], values='成交额', height=1080, width=1920,
    #                  color='涨跌幅', color_continuous_scale='Geyser', range_color=[-0.05, 0.05], color_continuous_midpoint=0,
    #                  hover_data={"成交量": ':.2%', "成交额": ':.2f', })
    # fig.update_traces(textinfo="label+value", textfont=dict(size=24))

    # # Display the treemap diagram in Streamlit
    # st.plotly_chart(fig)


# 运行 Streamlit 应用程序
if __name__ == "__main__":
    main()
