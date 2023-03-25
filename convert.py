import pandas as pd
from datetime import datetime
# import sys
# sys.path.append('../utils')
# import constants
from functools import lru_cache
OPTION_DICT = {
    "all": (float('-inf'), float('inf')),
    "0-100": (0, 100),
    "100-500": (100, 500),
    "500-1000": (500, 1000),
    "1000-30000": (1000, 30000),
}

RANGE = ["跌停", "跌<-5%",  "-3%<-5%",     "-3<-1%",
         "平盘", "<3%",     "3-5%",   "5%-涨停", "涨停"]


def get_data() -> tuple[pd.DataFrame, list]:
    """
    获得股票历史信息，并计算总市值
    """
    # 显示结果
    df = pd.read_csv(
        f"./data/merge_{datetime.now().strftime('%Y-%m-%d')}.csv", parse_dates=['日期'], index_col=0, dtype={"股票代码": object})
    # dates = df.index.unique().sort_values().to_list()
    # print(type(dates[0]))
    # dates = [x.strftime("%Y-%m-%d") for x in dates]
    # 获得当前结果集的日期列表
    # dates_list = [date.strftime('%Y-%m-%d') for date in dates]
    value = pd.read_csv("./data/总股本.csv", index_col=0, dtype={"股票代码": object})
    value_dict = value['总股本'].to_dict()
    df['总股本'] = df['股票代码'].apply(lambda x: value_dict.get(x))
    df['总市值'] = df['总股本']*df['收盘']

    return df


def get_count(_df):
    """
    根据日期,板块名称对涨跌幅进行
    """
    cur_df = _df.copy()
    # 按股票名称分组，并统计涨幅大于0和小于0的股票数量
    result = cur_df.groupby(['日期', '板块名称'])['涨跌幅'].agg(
        [('涨的数量', lambda x: sum(x > 0)), ('跌的数量', lambda x: sum(x < 0)), ('平的数量', lambda x: sum(x == 0))])
    result['涨幅比'] = result['涨的数量'] / \
        (result['涨的数量']+result['跌的数量']+result['平的数量'])*100
    # result.reset_index(inplace=True)
    # my_df = result.loc[("2023-03-01", "其他传媒")]
    # dd = my_df[my_df.loc['板块名称'] == "其他传媒"]
    # print(my_df)
    return result


def get_sum(_df):
    """
    根据start_value, end_value过滤总市值
    """
    cur_df = _df.copy()
    value_df = cur_df.groupby(['日期', "板块名称"]).agg(
        {"涨跌幅": "mean", "总市值": "sum"})
    # value_df.reset_index(inplace=True)
    return value_df


def get_range(_df):  # 按涨跌幅统计

    # db = df.loc['2023-03-01']
    cur_df = _df.copy()
    bins = [-20, -10, -5, -3, -0.099, 0.099, 3, 5, 10, 20]
    # bins = list(range(-11, 12))
    cuts = pd.cut(cur_df['涨跌幅'], bins=bins)
    pct_chg_list = cur_df.groupby(["日期", "板块名称", cuts])['涨跌幅'].count()
    cur_df = pct_chg_list.unstack()
    # my_df = cur_df.loc["2023-03-01"]
    # dd = my_df[my_df.loc['板块名称'] == "其他传媒"]
    # print(dd)
    # my_df = cur_df.loc[("2023-03-01", "其他传媒")]
    # dd = my_df[my_df.loc['板块名称'] == "其他传媒"]
    # print(f'range {my_df}')
    return cur_df


def runit():
    df = get_data()
    for key, value in OPTION_DICT.items():
        start_value, end_value = value

        # start_value, end_value = OPTION_DICT["100-500"]
        cur_df = df.copy()
        cur_df = cur_df[(cur_df['总市值'] >= (start_value)*100_000_000)
                        & (cur_df['总市值'] <= (end_value)*100_000_000)]
        result = get_count(cur_df)
        value_df = get_sum(cur_df)
        final_df = result.join(value_df, on=["日期", "板块名称"])
        # final_df.dropna(inplace=True, axis=0)
        # 将Salary列格式化为亿元
        final_df['总市值亿元'] = final_df['总市值'].apply(
            lambda x: '{:.2f}'.format(x/100000000))

        db = get_range(cur_df)
        result = pd.merge(final_df, db, on=["日期", '板块名称'])
        result.reset_index(inplace=True, level=[0, 1])
        # 获得字段的前八列
        a = result.columns[:9].to_list()
        a.extend(RANGE)
        result.columns = a
        result.to_csv(
            f"./data/result_{key}_{datetime.now().strftime('%Y%m%d')}.csv", index=False)
        # result.to_csv(
        #     f"./data/result_100-500_{datetime.now().strftime('%Y%m%d')}.csv", index=False)
        # result.set_index
        # result.set_index("日期",inplace=True)
        # my_df = result.loc["2023-03-01"]
        # dd=my_df[my_df['板块名称'] == "其他传媒"]
        # print(dd)


if __name__ == "__main__":
    runit()
