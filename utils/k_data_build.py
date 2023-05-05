import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
import time
from datetime import datetime
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode


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
    # 仅显示Name，Age和Salary列
    # for name in self.custom_columns:
    #     options.configure_column(
    #         name, editable=False, enableRowGroup=True, enablePivot=True)

    # editable = True was removed - need this to be non- editable
    # options.auto_size_columns()

    # options.set_columnDefs(columnDefs)
    options.configure_side_bar()
    # options.fit_columns_on_grid_load(True)
    options.configure_selection("single")
    if "state" in st.session_state:
        # self.logger.info(f"get it {st.session_state.state}")
        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            save_settings=True,
            load_settings=True,
            allow_unsafe_jscode=True,
            height=400,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
            column_state=st.session_state.state,
            # columns=self.custom_columns
            # key='my_grid',
        )
    else:
        # self.logger.info("not get it")
        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            save_settings=True,
            load_settings=True,
            allow_unsafe_jscode=True,
            height=400,
            # key='my_grid',
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
            # columns=self.custom_columns

        )

    return selection


class KdataStreamlitApp():

    range_dict = {
        "2023": [dict(bounds=["2023-01-21", "2023-01-30"]),
                 dict(bounds=["sat", "mon"]),
                 dict(values=["2023-04-05"]),],
        "2022": [dict(bounds=["2022-01-29", "2022-02-07"]),
                 dict(bounds=["2022-10-01", "2022-10-09"]),
                 dict(bounds=["2022-04-02", "2022-04-05"]),
                 dict(bounds=["2022-04-30", "2022-05-04"]),
                 dict(bounds=["2022-09-10", "2022-09-12"]),
                 dict(bounds=["sat", "mon"]),],
        "2021": [dict(bounds=["2021-02-11", "2021-02-18"]),
                 dict(bounds=["2021-05-01", "2021-05-05"]),
                 dict(bounds=["2021-06-12", "2021-06-14"]),
                 dict(bounds=["2021-10-01", "2021-10-07"]),
                 dict(bounds=["2021-09-18", "2021-09-21"]),
                 dict(bounds=["sat", "mon"]),
                 ],

    }

    def __init__(self, year) -> None:
        self.year = year

    def get_line_df(self):
        line_df = pd.read_csv(
            f"./data/result/min_{self.year}.csv", parse_dates=['日期'])
        # line_df.info()
        return line_df

    def main(self):

        st.set_page_config(
            page_title=f"{self.year}-k线数据分析", layout="wide")
        df = pd.read_csv(f"./data/k_data_{self.year}01-{self.year}12.csv",
                         parse_dates=['date'])
        print(df.info())
        # st.dataframe(df)
        # 生成新列，以便后面设置颜色
        df['diag'] = np.empty(len(df))
        # 设置涨/跌成交量柱状图的颜色
        df.loc[df.close > df.open, 'diag'] = 'red'
        df.loc[df.close <= df.open, 'diag'] = 'green'
        sma = df['close'].rolling(13).mean()
        df['SMA'] = sma
        ema = df['close'].rolling(55).mean()
        df['EMA'] = ema
        df.set_index("date", inplace=True)
        start_date = f'{self.year}-01-01'
        end_date = f'{self.year}-12-31'

        df = df.loc[start_date:end_date]
        df.reset_index(inplace=True)

        fig = make_subplots(rows=3,
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.09,
                            subplot_titles=('k线图', '成交量', '涨跌幅'),
                            row_width=[0.2, 0.2, 0.6])
        # 获得数据集
        line_df = self.get_line_df()

        candlestick = go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color='red',
            decreasing_line_color='green', name="k线图",
            text=[f'日期: {date:%Y-%m-%d}<br>开盘: {open_:.2f}<br>最高: {high:.2f}<br>最低: {low:.2f}<br>收盘: {close_:.2f}'
                  for date, open_, high, low, close_ in zip(df['date'], df['open'], df['high'], df['low'], df['close'])],
            hoverinfo='text'
        )

        sma = go.Scatter(x=df['date'],
                         y=df["SMA"],
                         yaxis="y1",
                         name="13MA", hovertemplate='日期: %{x|%Y-%m-%d}<br>价格: %{y:.2f}'
                         )

        ema = go.Scatter(x=df['date'],
                         y=df["EMA"],
                         yaxis="y1",
                         name="55MA", hovertemplate='日期: %{x|%Y-%m-%d}<br>价格: %{y:.2f}'
                         )

        fig.add_trace(
            candlestick,
            row=1,
            col=1
        )
        fig.add_trace(sma, row=1, col=1)
        fig.add_trace(ema, row=1, col=1)

        # volume
        df['volume_b'] = df.volume/1e9
        df['amount_b'] = df.amount/1e9
        fig.add_trace(
            go.Bar(x=df.date,
                   y=df.amount_b,
                   marker_color=df.diag, yaxis='y2', name="成交量", hovertemplate='日期: %{x|%Y-%m-%d}<br>成交量: %{y:.2f}B'),
            #    showlegend=False,marker_color=df.diag, opacity=0.5, yaxis='y2'),
            row=2,
            col=1
        )
        # Set the y-axis range to be slightly larger than the data range
        y_range = [df.amount_b.min() - 0.1 * abs(df.amount_b.min()),
                   df.amount_b.max() + 0.1 * abs(df.amount_b.max())]
        fig.update_yaxes(range=y_range, row=2, col=1)
        # Set the y-axis range to be slightly larger than the data range
        # y_range = [df['amount_b'].min() - 0.1 * abs(df['amount_b'].min()), df['amount_b'].max() + 0.1 * abs(df['amount_b'].max())]

        # 在row=2, col=1处添加红线
        fig.add_shape(type='line',
                      x0=min(line_df['日期']), y0=4, x1=max(line_df['日期']), y1=4,
                      line=dict(color='red', width=2),
                      row=3, col=1)

        # 绘制折线图
        # line_df.loc[line_df['跌幅'] > 4, '跌幅'] = 0
        fig.add_trace(
            go.Bar(x=line_df['日期'], y=line_df['涨幅'], name='涨幅总数', yaxis="y3", marker=dict(color='blue'), hovertemplate='日期: %{x|%Y-%m-%d}<br>总数: %{y:,}'), row=3, col=1)
        fig.add_trace(
            go.Bar(x=line_df['日期'], y=line_df['跌幅'], name='跌幅总数', yaxis="y3", marker=dict(color='orange'), hovertemplate='日期: %{x|%Y-%m-%d}<br>总数: %{y:,}'), row=3, col=1)
        fig.update_yaxes(range=[0, 30], row=3, col=1)

        fig.update_xaxes(tickformat='%Y-%m-%d',  type='date', row=3, col=1)
        # fig.update_xaxes(tickformat='%Y-%m-%d',  type='date', row=2, col=1)
        # # fig.update_xaxes(tickformat='%Y-%m-%d', tickangle=45, type='date', row=2, col=1)
        # fig.update_xaxes(tickformat='%Y-%m-%d', type='date', row=1, col=1)

        fig.update_xaxes(
            # dict(bounds=["2023-04-05", "2023-04-05"])  # 去除周六和周日的间隔
            rangebreaks=self.range_dict.get(self.year), row=3, col=1
        )
        # fig.update_xaxes(
        #     rangebreaks=[
        #         dict(bounds=["sat", "mon"]),
        #         dict(bounds=["2023-01-21", "2023-01-29"]),
        #         dict(bounds=["2023-04-05", "2023-04-05"])  # 去除周六和周日的间隔
        #     ], row=2, col=1
        # )
        # fig.update_xaxes(
        #     rangebreaks=[
        #         dict(bounds=["sat", "mon"]),
        #         dict(bounds=["2023-01-21", "2023-01-29"]),
        #         dict(bounds=["2023-04-05", "2023-04-05"])  # 去除周六和周日的间隔
        #     ], row=1, col=1
        # )
        fig.update_layout(xaxis_rangeslider_visible=False)
        # fig.update_layout(xaxis_rangeslider_visible=False, xaxis_title="Date",
        #                 xaxis=dict(
        #                     type='date',
        #                     tickformat='%Y-%m-%d'
        #                 ))
        # fig.update_xaxes(title_text='日期')
        # fig.update_yaxes(title_text='沪深300价格')
        fig.update_layout(title=f"{self.year}上证指数", height=900)
        # fig.update_layout(title="2020上证指数", width=900,  height=600)
        #   yaxis_title="Price (USD)",
        st.plotly_chart(fig, use_container_width=True)
        # fig.show()
        result = aggrid_interactive_table(line_df)

        # st.dataframe(line_df)


# 运行 Streamlit 应用程序
if __name__ == "__main__":
    stock = KdataStreamlitApp()
    stock.main()
    # logging.info(stock.start_day)
