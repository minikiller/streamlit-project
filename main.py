import streamlit as st
import pandas as pd
# 定义 Streamlit 应用程序
import plotly.express as px
from datetime import datetime
# import streamlit_aggrid as ag
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.graph_objs as go
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode
from streamlit_plotly_events import plotly_events
import pytz

tz = pytz.timezone('Asia/Shanghai')

options = ["0-100", "100-500", "500-1000", "1000-30000", "all", ]
# option_dict = {
#     "全部": (float('-inf'), float('inf')),
#     "0-100": (0, 100),
#     "100-500": (100, 500),
#     "500-1000": (500, 1000),
#     "1000-30000": (1000, 30000),
# }
RANGE = ["跌停", "跌<-5%",  "-3%<-5%",     "-3<-1%",
         "平盘", "<3%",     "3-5%",   "5%-涨停", "涨停"]

stock_options = ["同花顺", '东方财富', ]
category_options = ['板块', "概念"]


def get_cur_date(day):
    date = datetime.now(tz)
    year = date.year
    month = date.month
    my_date = datetime(year, month, day)
    return my_date.strftime("%Y-%m-%d")

# Define callback to retrieve data from clicked point


# @st.cache_data
def get_data(stock, category, range) -> tuple[pd.DataFrame, list]:
    """
    获得股票历史信息，并计算总市值
    """
    # 显示结果
    df = pd.read_csv(
        f"data/sector/sector_{stock}_{category}_{range}.csv", parse_dates=['日期'], index_col=0, dtype={"股票代码": object})
    dates = df.index.unique().sort_values().to_list()
    # 获得当前结果集的日期列表
    dates_list = [date.strftime('%Y-%m-%d') for date in dates]
    return (df, dates_list)


@st.cache_data
def get_code_df():
    df = pd.read_csv(
        "data/板块名称_股票对应.csv", index_col=0, dtype={"股票代码": object})
    return df
# @st.cache_data


def get_code_data(range):
    """
    获得每个板块名称下的股票个数
    """

    data = pd.read_csv(
        f"data/股票代码个数_{range}.csv", index_col=0, )
    # data = df.groupby("板块名称")["股票代码"].count()
    data_dict = data["股票个数"].to_dict()
    return data_dict


def aggrid_interactive_table(df: pd.DataFrame):
    """
    Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df(pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True)
    # editable = True was removed - need this to be non- editable
    # options.auto_size_columns()
    options.configure_side_bar()
    # options.fit_columns_on_grid_load(True)
    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        height=400,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW
    )

    return selection


@st.cache_data
def get_orginal_data() -> tuple[pd.DataFrame, list]:
    """
    获得股票原始历史信息 
    """
    df = pd.read_csv(
        f"data/Hist_{datetime.now(tz).strftime('%Y-%m-%d')}.csv", parse_dates=['日期'], index_col=0, dtype={"股票代码": object})
    # dates = df.index.unique().sort_values().to_list()
    return df


def create_group(df):
    return df.groupby(df.index).sum()


def create_bar(df):

    # bins = list(range(-11, 12))
    # bins = [-20, -10, -5, -3, -0.099, 0.099, 3, 5, 10, 20]
    bins = [-20, -9.97, -5, -3, -0.099, 0.099, 3, 5, 9.97, 20]
    cuts = pd.cut(df['涨跌幅'], bins=bins)
    pct_chg_list = df.groupby(cuts)['涨跌幅'].count().tolist()

    y = pct_chg_list
    color = ["green", "green", "green", "green",
             "yellow", "red", "red", "red", "red"]

    data = pd.DataFrame({"x": RANGE, "y": y, "color": color})
    return data


def create_detail_bar(code, my_df):
    my_df = my_df[my_df['板块名称'] == code]
    if my_df.empty:
        st.warning("没有获得数据")
        return None

    color = ["green", "green", "green", "green",
             "yellow", "red", "red", "red", "red"]

    my = my_df[RANGE].unstack()
    my = my.reset_index()
    my.columns = ['x', "date", "y"]
    # my
    data = pd.DataFrame({"x": my["x"], "y": my["y"], "color": color})
    return data


def display_click_data(trace, points, state):
    if points.point_inds:
        point_index = points.point_inds[0]
        point_data = trace.data[0]['x'][point_index], trace.data[0]['y'][point_index]
        st.write(f'Clicked point data: x={point_data[0]}, y={point_data[1]}')
    else:
        st.warning("no data")


def main():
    st.set_page_config(page_title="板块的热力图", layout="wide")
    # 获取当前时区的时间

    # current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    # 显示当前时间
    # st.write("当前时间是：", current_time)

    filter_value = "包装印刷,中药"
    start_value = "10"
    end_value = "100"

    st.title("使用plotly计算板块的热力图")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        stock_value = st.sidebar.radio("请选择卷商:", stock_options)
    with col2:
        category_value = st.sidebar.radio("请选择分类:", category_options)

    # 添加一些文本
    # st.write("使用plotly计算板块的热力图")
    code_value = st.sidebar.text_input("请输入股票名字：",)
    if not "filter" in st.session_state:
        st.session_state.filter = ""
    code_df = get_code_df()
    # filter_value = st.sidebar.text_input("请输入过滤的板块名字：", "包装印刷,中药")
    if code_value.strip() != "":
        code_result = code_df[code_df['股票代码'] == code_value]
        if not code_result.empty:
            mylist = []
            for index, row in code_result.iterrows():
                mylist.append(row['板块名称'])
            mystr = ",".join(mylist)
            st.sidebar.success(f"股票名称：{ code_value},板块名称：{mystr}")
            st.session_state.filter = mystr
        else:
            st.sidebar.warning(f"股票代码：{code_value}没找到对应的板块名称！")
    # 添加一个交互式小部件
    filter_value = st.sidebar.text_input(
        "请输入过滤的板块名字：", st.session_state.filter)
    # create a slider widget for the low value
    # start_value = st.sidebar.slider("请选择过滤的最小值(亿元)", 1, 500, 10, 1)
    # end_value = st.sidebar.slider("请选择过滤的最大值(亿元)", 101, 30000, 101, 10)

    # create a radio button widget and store the user's choice in a variable
    selected_option = st.sidebar.radio("请选择过滤的数值(亿元)", options)
    # start_value, end_value = option_dict.get(selected_option)
    # dates_list 用于过滤日期
    df, dates_list = get_data(stock_value, category_value, selected_option)
    data_dict = get_code_data(selected_option)
    # print(data_dict)

    init_df = get_orginal_data()
    #  = get_list(df)
    # x_axis = st.sidebar.selectbox('选择日期', dates_list)
    # d = st.sidebar.date_input(
    #     "When\'s your birthday",
    #     datetime.now())

    # st.write('Your birthday is:', d)

    # create a slider widget for the low value
    if 'cur_day' not in st.session_state:
        st.session_state.cur_day = 1
    # stored_value = st.session_state.cur_day
    cur_day = st.sidebar.slider("请选择您想查看的天", 1, 31, st.session_state.cur_day)
    # st.session_state.cur_day = cur_day

    cur_date = get_cur_date(cur_day)
    if cur_date in dates_list:
        # create a checkbox widget
        # df['涨跌幅'] = df['收盘价'].pct_change()
        cur_df = df.loc[cur_date]
        # group_df = create_group(df)
        # group_df = group_df.loc[cur_date]
        # 过滤市值
        # cur_df = cur_df[(cur_df['总市值'] >= (start_value)*100_000_000)
        #                 & (cur_df['总市值'] <= (end_value)*100_000_000)]
        # 创建bar

        st.subheader(f"{cur_date}全部板块统计柱形图：")
        bar_df = create_bar(init_df.loc[cur_date])

        # fig = go.Figure([go.Bar(x=data['x'], y=data['y'])])
        fig = go.Figure([go.Bar(x=bar_df['x'], y=bar_df['y'], marker={
                        'color': bar_df["color"]}, text=bar_df['y'], textposition='auto')])
        fig.update_traces(
            texttemplate='%{text:.2d}', textposition='outside')
        fig.update_layout(autosize=True, margin=dict(
            l=50, r=50, t=50, b=50),)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"数据集显示：{cur_date}")
        cur_df.reset_index(inplace=True)
        if filter_value.strip() != "":
            st.success(f"板块名称是：{filter_value}")
            _list = filter_value.split(",")
            cur_df = cur_df[cur_df['板块名称'].isin(_list)]
        else:
            st.warning("板块名称是空!")
        # cur_df = cur_df[~cur_df['板块名称'].isin(_list)]
        # print(cur_df.columns)
        cur_df = cur_df.sort_values(by=['涨幅比', "总市值"], ascending=False)
        cur_df = cur_df.drop(columns="总市值")
        zero_df = cur_df[cur_df['涨幅比'] == 0]
        cur_df = cur_df[cur_df['涨幅比'] != 0]
        # st.dataframe(cur_df, use_container_width=True)

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
        st.subheader(f"显示冰点的数据:")
        st.dataframe(zero_df)

        # st.title("Netlix shows analysis")
        # add this
        # 使用beta_columns创建两个列
        st.markdown(
            f'<span style="color: blue;font-size: 24px">{cur_date} {stock_value}{category_value}名称显示的数据:</span>', unsafe_allow_html=True)
        gb = GridOptionsBuilder.from_dataframe(cur_df)
        gb.configure_pagination(paginationPageSize=25,
                                paginationAutoPageSize=True)
        gb.configure_side_bar()

        gb.configure_default_column(
            groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)

        gridOptions = gb.build()
        result = aggrid_interactive_table(cur_df)

        col1, col2 = st.columns(2)
        with col1:
            code = "国有大型银行"
            select = result["selected_rows"]
            count = 0
            if len(select) > 0:
                # st.write(select)
                code = select[0]['板块名称']
                # if 'code' not in st.session_state:
                st.session_state.code = code
                count = select[0]['涨的数量']+select[0]['跌的数量']+select[0]['平的数量']
            else:
                # print("filter"+st.session_state.filter)
                # code优先级最高
                if 'code' in st.session_state:
                    code = st.session_state.code
                # filter优先级其次
                # if 'filter' in st.session_state and st.session_state.filter != "":
                #     code = st.session_state.filter
                # print("current"+code)
                # 过滤板块其次
                # if filter_value != "":
                #     code = filter_value
            # st.write(code)title=f'{cur_date} {code}涨的数量折线图',
            st.subheader(
                # f'{cur_date} <<{code}>>涨的数量折线图,总个数：{data_dict.get(code)}')
                f'{cur_date} <<{code}>>涨的数量折线图,总个数：{count}')

            fig = go.Figure()
            data_df = df.copy()
            data_df = data_df[data_df['板块名称'] == code]

            data_df.reset_index(inplace=True)
            data_df['date'] = data_df['日期'].apply(
                lambda x: x.strftime("%Y/%m/%d"))
            fig.add_trace(go.Scatter(
                x=data_df['date'], y=data_df['涨的数量'], mode='lines', line=dict(color='red')))

            # fig.add_trace(go.Scatter(
            #     x=data_df.index, y=data_df['跌的数量'], mode='lines'))

            # add two horizontal lines at y=0 and y=1
            # fig.add_shape(type='line', x0=min(data_df.index), y0=min(data_df['涨的数量']), x1=max(data_df.index), y1=min(data_df['涨的数量']),
            #               line=dict(color='red', width=2))
            # fig.add_shape(type='line', x0=0, y0=1, x1=9, y1=1,
            #               line=dict(color='green', width=2))
            # set the title and axis labels
            fig.update_layout(
                xaxis_title='日期', yaxis_title='涨的数量', xaxis_tickangle=-45)

            # fig.update_layout(xaxis_tickformat='%Y-%m-%d')

            # set the maximum value of the y-axis to 2
            fig.update_yaxes(range=[0, count])
            # fig.update_yaxes(range=[0, data_dict.get(code)])
            # fig = fig.add_traces(fig.data)

            # mark the intervals on the y-axis
            # fig.update_layout(yaxis=dict())

            # customize the y-axis tick marks
            # fig.update_layout(yaxis=dict(
            #     tickvals=[-20, 0, 20], ticktext=['Low', 'Medium', 'High'], tickmode='linear', dtick=5))

            # display the plot
            # 加入事件
            selected_points = plotly_events(fig)
            if len(selected_points) > 0:
                a = selected_points[0]
                # st.warning(a['x'])
                data = a['x'].split("/")[2]
                # st.warning(data)
                # cur_day = int(data)
                st.session_state.cur_day = int(data)
        # st.plotly_chart(fig, use_container_width=True)
        # title=f'{cur_date} {code} 柱形图',
        with col2:
            st.subheader(f'{cur_date} <<{code}>> 柱形图',)
            print("cod value is :"+code)
            code_df = create_detail_bar(code, cur_df)
            if code_df is not None:
                # fig = go.Figure([go.Bar(x=data['x'], y=data['y'])])
                fig = go.Figure([go.Bar(x=code_df['x'], y=code_df['y'], marker={
                                'color': code_df["color"]}, text=code_df['y'], textposition='auto')])
                fig.update_traces(
                    texttemplate='%{text:.2d}', textposition='outside')
                fig.update_layout(autosize=True, margin=dict(
                    l=70, r=70, t=70, b=70),)
                fig.update_layout(
                    xaxis_title='区间', yaxis_title='数量')
                # st.plotly_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
            # st.plotly_chart(fig, use_container_width=True)
        # AgGrid(cur_df, gridOptions=gridOptions, theme='material')
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
        # cur_df = get_grouped(cur_df)
        # st.dataframe(cur_df, use_container_width=True)

    else:
        st.write(f"您选择的数据不存在{cur_date}")


# 运行 Streamlit 应用程序
if __name__ == "__main__":
    main()
