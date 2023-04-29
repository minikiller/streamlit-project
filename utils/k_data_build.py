import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
import time
from datetime import datetime
import pandas as pd

"""_summary_

Returns:
    _type_: _description_
"""

class KdataStreamlitApp():
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
                         parse_dates=True)
        st.dataframe(df)
        # 生成新列，以便后面设置颜色
        df['diag'] = np.empty(len(df))
        # 设置涨/跌成交量柱状图的颜色
        df.diag[df.close > df.open] = 'red'
        df.diag[df.close <= df.open] = 'green'

        fig = make_subplots(rows=3,
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.09,
                            subplot_titles=('k线图', '成交量', '涨跌幅'),
                            row_width=[0.3, 0.3, 0.4])
        line_df = self.get_line_df()
        # candlestick
        # candlestick = go.Candlestick(
        #     x=df.date,
        #     open=df['Open'],
        #     high=df['High'],
        #     low=df['Low'],
        #     close=df['Close'],
        #     showlegend=False,
        #     increasing_line_color='red',
        #     decreasing_line_color='green'
        # )

        candlestick = go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color='red',
            decreasing_line_color='green', name="k线图"
        )

        # set the hovertemplate
        # fig.update_traces(hovertemplate='Open: %{open}<br>High: %{high}<br>Low: %{low}<br>Close: %{close}<br>date: %{x|%Y-%m-%d}')

        # candlestick_fig = go.Figure(candlestick)

        # # candlestick.update_layout(xaxis_rangeslider_visible=False)
        # candlestick_fig.update_layout(xaxis=dict(
        #     tickformat='%Y-%m-%d'
        # ))
        sma = df['close'].rolling(13).mean()
        df['SMA'] = sma
        sma = go.Scatter(x=df.date,
                         y=df["SMA"],
                         yaxis="y1",
                         name="13MA"
                         )

        ema = df['close'].rolling(55).mean()
        df['EMA'] = ema

        ema = go.Scatter(x=df.date,
                         y=df["EMA"],
                         #  yaxis="y1",
                         name="55MA"
                         )

        fig.add_trace(
            candlestick,
            row=1,
            col=1
        )
        # fig.add_trace(candlestick, row=1, col=1)
        fig.add_trace(sma, row=1, col=1)
        fig.add_trace(ema, row=1, col=1)

        # volume
        fig.add_trace(
            go.Bar(x=df.date,
                   y=df.volume,
                   marker_color=df.diag, yaxis='y2', name="成交量"),
            #    showlegend=False,marker_color=df.diag, opacity=0.5, yaxis='y2'),
            row=2,
            col=1
        )
        #
        # fig.update(data=[candlestick, sma],row=1,
        #     col=1)
        # candlestick.update_layout(xaxis=dict(
        #     tickformat='%Y-%m-%d'
        # ))
        # 在row=2, col=1处添加红线
        fig.add_shape(type='line',
                      x0=min(line_df['日期']), y0=4, x1=max(line_df['日期']), y1=4,
                      line=dict(color='red', width=2),
                      row=3, col=1)

        # 绘制折线图
        fig.add_trace(
            go.Bar(x=line_df['日期'], y=line_df['涨幅'], name='涨幅总数', marker=dict(color='blue')), row=3, col=1)
        fig.add_trace(
            go.Bar(x=line_df['日期'], y=line_df['跌幅'], name='跌幅总数', marker=dict(color='orange')), row=3, col=1)
        fig.update_yaxes(range=[0, 30], row=3, col=1)

        # fig.update(layout_xaxis_rangeslider_visible=False)
        # fig.update_layout(xaxis=dict(
        #     tickformat='%Y-%m-%d',  # Set the date format here
        #     tickangle=45,
        #     type='date'
        # ))
        fig.update_xaxes(tickformat='%Y-%m-%d',  type='date', row=3, col=1)
        fig.update_xaxes(tickformat='%Y-%m-%d',  type='date', row=2, col=1)
        # fig.update_xaxes(tickformat='%Y-%m-%d', tickangle=45, type='date', row=2, col=1)
        fig.update_xaxes(tickformat='%Y-%m-%d', type='date', row=1, col=1)
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # 去除周六和周日的间隔
            ], row=3, col=1
        )
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # 去除周六和周日的间隔
            ], row=2, col=1
        )
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # 去除周六和周日的间隔
            ], row=1, col=1
        )
        # fig.update_xaxes(title_text='日期')
        # fig.update_yaxes(title_text='沪深300价格')
        fig.update_layout(title=f"{self.year}上证指数", height=900)
        # fig.update_layout(title="2020上证指数", width=900,  height=600)
        #   yaxis_title="Price (USD)",
        st.plotly_chart(fig, use_container_width=True)
        # fig.show()


# 运行 Streamlit 应用程序
if __name__ == "__main__":
    stock = KdataStreamlitApp()
    stock.main()
    # logging.info(stock.start_day)
