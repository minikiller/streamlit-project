import streamlit as st
import pandas as pd
# 定义 Streamlit 应用程序
import plotly.express as px
from datetime import datetime
# import streamlit_aggrid as ag
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.graph_objs as go


options = ["0-100", "100-500", "500-1000", "1000-30000", "全部", ]
option_dict = {
    "全部": (float('-inf'), float('inf')),
    "0-100": (0, 100),
    "100-500": (100, 500),
    "500-1000": (500, 1000),
    "1000-30000": (1000, 30000),
}


@st.cache_data
def get_data() -> tuple[pd.DataFrame, list]:
    """
    获得股票历史信息，并计算总市值
    """
    # 显示结果
    df = pd.read_csv(
        "data/Hist_2023-03-20.csv", parse_dates=['日期'], index_col=0, dtype={"股票代码": object})
    dates = df.index.unique().sort_values().to_list()
    # print(type(dates[0]))
    # dates = [x.strftime("%Y-%m-%d") for x in dates]
    # 获得当前结果集的日期列表
    dates_list = [date.strftime('%Y-%m-%d') for date in dates]
    value = pd.read_csv("./data/总股本.csv", index_col=0, dtype={"代码": object})
    value_dict = value['总股本'].to_dict()
    df['总股本'] = df['股票代码'].apply(lambda x: value_dict.get(x))
    df['总市值'] = df['总股本']*df['收盘']

    return (df, dates_list)


def create_bar(df):

    # bins = list(range(-11, 12))
    bins = [-20, -10, -5, -3, -0.099, 0.099, 3, 5, 10, 20]

    cuts = pd.cut(df['涨跌幅'], bins=bins)
    pct_chg_list = df.groupby(cuts)['涨跌幅'].count().tolist()

    x = ["跌停", "跌<-5%",  "-5<-3%",     "-1<3%",    "平盘",
         "1<3%",     "3-5%",   "5%-涨停", "涨停"]

    y = pct_chg_list
    color = ["green", "green", "green", "green",
             "yellow", "red", "red", "red", "red"]

    data = pd.DataFrame({"x": x, "y": y, "color": color})
    return data


def get_grouped(db):
    # bins = list(range(-11, 12))

    bins = [-20, -10, -5, -3, -0.099, 0.099, 3, 5, 10, 20]

    cuts = pd.cut(db['涨跌幅'], bins=bins)
    pct_chg_list = db.groupby(["板块名称", cuts])['涨跌幅'].count()
    df = pd.DataFrame(pct_chg_list)
    # db.reset_index(inplace=True,level=[0, 1])
    df = df.unstack()
    result = pd.merge(db, df, on='板块名称')
    return result


def get_cur_date(day):
    date = datetime.now()
    year = date.year
    month = date.month
    my_date = datetime(year, month, day)
    return my_date.strftime("%Y-%m-%d")


def main():

    filter_value = "包装印刷,中药"
    start_value = "10"
    end_value = "100"
    st.set_page_config(page_title="板块的热力图", layout="wide")

    st.title("使用plotly计算板块的热力图")

    # 添加一些文本
    # st.write("使用plotly计算板块的热力图")

    # 添加一个交互式小部件
    filter_value = st.sidebar.text_input("请输入过滤的板块名字：", "包装印刷,中药")

    # create a slider widget for the low value
    # start_value = st.sidebar.slider("请选择过滤的最小值(亿元)", 1, 500, 10, 1)
    # end_value = st.sidebar.slider("请选择过滤的最大值(亿元)", 101, 30000, 101, 10)

    # create a radio button widget and store the user's choice in a variable
    selected_option = st.sidebar.radio("请选择过滤的数值(亿元)", options)
    start_value, end_value = option_dict.get(selected_option)
    # dates_list 用于过滤日期
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
    cur_date = get_cur_date(cur_day)
    # st.write("You selected cur date is", cur_date)
    # create a date input widget
    if cur_date in dates_list:
        # create a checkbox widget
        # df['涨跌幅'] = df['收盘价'].pct_change()
        cur_df = df.loc[cur_date]

        # 创建bar
        bar_df = create_bar(cur_df)

        # fig = go.Figure([go.Bar(x=data['x'], y=data['y'])])
        fig = go.Figure([go.Bar(x=bar_df['x'], y=bar_df['y'], marker={
                        'color': bar_df["color"]}, text=bar_df['y'], textposition='auto')])
        fig.update_traces(
            texttemplate='%{text:.2d}', textposition='outside')
        fig.update_layout(autosize=True, margin=dict(
            l=20, r=20, t=20, b=20),)
        st.plotly_chart(fig, use_container_width=True)

        # 按股票名称分组，并统计涨幅大于0和小于0的股票数量
        result = cur_df.groupby(['板块名称'])['涨跌幅'].agg(
            [('涨的数量', lambda x: sum(x > 0)), ('跌的数量', lambda x: sum(x < 0))])
        result['涨幅比'] = result['涨的数量']/(result['涨的数量']+result['跌的数量'])*100

        cur_df = cur_df[(cur_df['总市值'] >= (start_value)*100_000_000)
                        & (cur_df['总市值'] <= (end_value)*100_000_000)]
        # cur_df
        cur_df = cur_df.groupby(["板块名称"]).agg(
            {"涨跌幅": "mean", "总市值": "sum"})
        cur_df = result.join(cur_df, on=["板块名称"])
        cur_df.dropna(inplace=True, axis=0)
        # 将Salary列格式化为亿元
        cur_df['总市值亿元'] = cur_df['总市值'].apply(
            lambda x: '{:.2f}'.format(x/100000000))

        st.subheader(f"数据集显示：{cur_date}")
        cur_df.reset_index(inplace=True)
        _list = filter_value.split(",")
        cur_df = cur_df[cur_df['板块名称'].isin(_list)]
        # cur_df = cur_df[~cur_df['板块名称'].isin(_list)]
        cur_df = cur_df.sort_values(by=['涨幅比', "总市值"], ascending=False)
        cur_df = cur_df.drop(columns="总市值")
        zero_df = cur_df[cur_df['涨幅比'] == 0]
        cur_df = cur_df[cur_df['涨幅比'] != 0]
        st.dataframe(cur_df, use_container_width=True)

        # fig = px.treemap(cur_df, path=[px.Constant('All'), '板块名称'], values='涨幅比', height=800, width=600,
        #                  color='涨幅比', color_continuous_scale='Geyser',  color_continuous_midpoint=0,
        #                  hover_data={'涨的数量': ":.d", "跌的数量": ":.d", })
        # fig.update_traces(textinfo="label+value", textfont=dict(size=24))

        # # Set the layout to center the figure
        # fig.update_layout(
        #     width=1080,
        #     height=1920,
        #     margin=dict(autoexpand=True),
        # )
        # # Display the treemap diagram in Streamlit
        # st.plotly_chart(fig)
        # st.plotly_chart(fig, use_container_width=True)
        st.subheader(f"显示为0的数据:")
        st.dataframe(zero_df, use_container_width=True)

        # st.title("Netlix shows analysis")
        # add this
        st.subheader(f"AgGrid 显示的数据:")
        gb = GridOptionsBuilder.from_dataframe(cur_df)
        gb.configure_pagination(
            paginationPageSize=25, paginationAutoPageSize=True)
        gb.configure_side_bar()

        gb.configure_default_column(
            groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)

        gridOptions = gb.build()
        AgGrid(cur_df, gridOptions=gridOptions, theme='material')
        #    data_return_mode='AS_INPUT',
        #    update_mode='MODEL_CHANGED',
        #    fit_columns_on_grid_load=False,
        #    theme='material',  # Add theme color to the table
        #    enable_enterprise_modules=True,
        #    height=350,
        #    width='100%',
        #    reload_data=True)
        # ag.grid(cur_df, height=300, width='100%',
        #         enableSorting=True, enableFilter=True)
        # ag.grid(data, enableSorting=True, enableFilter=True)
        cur_df = get_grouped(cur_df)
        st.dataframe(cur_df, use_container_width=True)

    else:
        st.write(f"您选择的数据不存在{cur_date}")


# 运行 Streamlit 应用程序
if __name__ == "__main__":
    main()
