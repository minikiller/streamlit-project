import streamlit as st
import pandas as pd
# 定义 Streamlit 应用程序
import plotly.express as px
from datetime import datetime


@st.cache_data
def get_data():
    # 显示结果
    df = pd.read_csv(
        "data/hist.csv", parse_dates=['日期'], index_col=0, dtype={"股票编号": object})
    return df


@st.cache_data
def get_list(df):
    dates = df.index.unique().sort_values().to_list()
    # print(type(dates[0]))
    # dates = [x.strftime("%Y-%m-%d") for x in dates]
    # 获得当前结果集的日期列表
    dates_list = [date.strftime('%Y-%m-%d') for date in dates]
    return dates_list


def get_cur_date(day):
    date = datetime.now()
    year = date.year
    month = date.month
    my_date = datetime(year, month, day)
    return my_date.strftime("%Y-%m-%d")


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

    if value:
        st.write("你好，" + value + "！")
    df = get_data()
    dates_list = get_list(df)
    # x_axis = st.sidebar.selectbox('选择日期', dates_list)
    d = st.sidebar.date_input(
        "When\'s your birthday",
        datetime.now())

    st.write('Your birthday is:', d)

    # create a slider widget for the low value
    cur_day = st.sidebar.slider("请选择您想查看的天", 1, 31, 1)

    # display the selected range
    st.write("You selected a range from", cur_day)
    # Display DataFrame
    st.subheader("DataFrame")
    # df = df.loc[x_axis]
    # if d:
    #     cur_date = d.strftime("%Y-%m-%d")
    #     if cur_date in dates_list:
    #         st.write("x"*10, d)
    #     else:
    #         st.write("y"*10, d)
    if cur_day:
        cur_date = get_cur_date(cur_day)
        st.write("You selected cur date is", cur_date)
        # create a date input widget
        if cur_date in dates_list:
            # create a checkbox widget
            cur_df = df.loc[cur_date]
            st.dataframe(cur_df)

            fig = px.treemap(cur_df, path=[px.Constant('All'), '股票编号'], values='成交额', height=1080, width=1920,
                             color='涨跌幅', color_continuous_scale='Geyser', range_color=[-0.05, 0.05], color_continuous_midpoint=0,
                             hover_data={"成交量": ':.2%', "成交额": ':.2f', })
            fig.update_traces(textinfo="label+value", textfont=dict(size=24))

            # # Display the treemap diagram in Streamlit
            st.plotly_chart(fig)
        else:
            st.write(f"您选择的数据不存在{cur_date}")


# 运行 Streamlit 应用程序
if __name__ == "__main__":
    main()
