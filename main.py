import streamlit as st
import pandas as pd
# 定义 Streamlit 应用程序
import plotly.express as px
from datetime import datetime


@st.cache_data
def get_data() -> tuple[pd.DataFrame, list]:
    # 显示结果
    df = pd.read_csv(
        "data/Hist_2023-03-20.csv", parse_dates=['日期'], index_col=0, dtype={"股票编号": object})
    dates = df.index.unique().sort_values().to_list()
    # print(type(dates[0]))
    # dates = [x.strftime("%Y-%m-%d") for x in dates]
    # 获得当前结果集的日期列表
    dates_list = [date.strftime('%Y-%m-%d') for date in dates]
    value = pd.read_csv(
        "./data/总股本.csv", index_col=0, dtype={"代码": object})
    value_dict = value['总股本'].to_dict()
    df['总股本'] = df['股票编号'].apply(lambda x: value_dict.get(x))
    df['总市值'] = df['总股本']*df['收盘']

    result = df.groupby(["日期", "板块名称"]).agg({"涨跌幅": "mean", "总市值": "sum"})
    return (result, dates_list)


def get_cur_date(day):
    date = datetime.now()
    year = date.year
    month = date.month
    my_date = datetime(year, month, day)
    return my_date.strftime("%Y-%m-%d")


def filter_df(df, cur_date, end_value, filter_value):
    pass


def main():

    filter_value = "包装印刷,中药"
    start_value = "10"
    end_value = "100"

    st.title("使用plotly计算板块的热力图")

    # 添加一些文本
    # st.write("使用plotly计算板块的热力图")

    # 添加一个交互式小部件
    filter_value = st.sidebar.text_input("请输入过滤的板块名字：", "包装印刷,中药")

    # create a slider widget for the low value
    start_value = st.sidebar.slider("请选择过滤的最小值(亿元)", 10, 50, 10, 5)
    end_value = st.sidebar.slider("请选择过滤的最大值(亿元)", 51, 100, 100, 5)

    df, dates_list = get_data()
    #  = get_list(df)
    # x_axis = st.sidebar.selectbox('选择日期', dates_list)
    # d = st.sidebar.date_input(
    #     "When\'s your birthday",
    #     datetime.now())

    # st.write('Your birthday is:', d)

    # create a slider widget for the low value
    cur_day = st.sidebar.slider("请选择您想查看的天", 1, 31, 1)

    # display the selected range
    # Display DataFrame
    # df = df.loc[x_axis]
    # if d:
    #     cur_date = d.strftime("%Y-%m-%d")
    #     if cur_date in dates_list:
    #         st.write("x"*10, d)
    #     else:
    #         st.write("y"*10, d)
    if cur_day:
        cur_date = get_cur_date(cur_day)
        # st.write("You selected cur date is", cur_date)
        # create a date input widget
        if cur_date in dates_list:
            # create a checkbox widget
            # df['涨跌幅'] = df['收盘价'].pct_change()
            cur_df = df.loc[cur_date]

            # cur_df
            cur_df.reset_index(inplace=True)
            _list = filter_value.split(",")
            cur_df = cur_df[~cur_df['板块名称'].isin(_list)]
            cur_df = cur_df[(cur_df['总市值'] >= int(start_value)*100_000_000)
                            & (cur_df['总市值'] <= int(end_value)*100_000_000)]

            st.subheader(f"数据集显示：{cur_date}")
            st.dataframe(cur_df)

            fig = px.treemap(cur_df, path=[px.Constant('All'), '板块名称'], values='总市值', height=1080*0.2, width=1920*0.2,
                             color='涨跌幅', color_continuous_scale='Geyser', range_color=[-0.05, 0.05], color_continuous_midpoint=0,
                             hover_data={"总市值": ':,.2f', '涨跌幅': ":.2%"})
            fig.update_traces(textinfo="label+value", textfont=dict(size=24))

            # # Display the treemap diagram in Streamlit
            st.plotly_chart(fig)
        else:
            st.write(f"您选择的数据不存在{cur_date}")


# 运行 Streamlit 应用程序
if __name__ == "__main__":
    main()
