"""
自动生成按照板块的统计结果文件，以用于streamlit中调用
"""

import pandas as pd
from datetime import datetime as dt
from functools import lru_cache
from constants import OPTION_DICT, RANGE
from tqdm import tqdm


class Stock():
    """
    管理股票历史数据
    """

    def get_stock_data(self) -> pd.DataFrame:
        df = pd.read_csv(
            f"./data/Hist_{dt.now().strftime('%Y-%m-%d')}.csv", parse_dates=['日期'], index_col=0, dtype={"股票代码": object})
        df.reset_index(inplace=True)
        df.drop(columns=['板块名称'], inplace=True)
        return df


class Sector():
    """
    管理股票板块
    """
    stock_options = ["同花顺", '东方财富', ]
    category_options = ['板块', "概念"]

    def create(self) -> dict:
        df_dict = {}
        stock = Stock()
        # 获得股票历史信息
        df = stock.get_stock_data()
        for stock in self.stock_options:
            for category in self.category_options:
                sector_df = pd.read_csv(f"./data/constant/{stock}_{category}名称_股票对应.csv",
                                        index_col=0, dtype={"股票代码": object})
                # df_list.append(sector_df)
                merged_df = pd.merge(df, sector_df, on='股票代码')
                file_name = f"./data/merge/merge_{stock}_{category}名称_{dt.now().strftime('%Y-%m-%d')}.csv"
                merged_df.to_csv(file_name, index=False)
                df_dict[(stock, category)] = merged_df
        return df_dict

    @lru_cache
    def get_capital_dict(self) -> dict:
        """
        获得总股本字典
        """
        capital_df = pd.read_csv("./data/总股本_em.csv",
                                 index_col="股票代码", dtype={"股票代码": object})
        capital_dict = capital_df['总股本'].to_dict()
        return capital_dict

    def calcu_capital(self, df, capital_dict):
        """
        计算总股本
        """
        df['总股本'] = df['股票代码'].apply(lambda x: capital_dict.get(x))
        df['总市值'] = df['总股本']*df['收盘']
        df.fillna(0, inplace=True)
        return df

    def to_csv(self, df, info) -> None:
        """
        save to csv file
        """
        stock, category, range = info
        file_name = f"./data/sector/sector_{stock}_{category}_{range}.csv"
        df.to_csv(file_name, index=False)

    def get_count(self, _df):
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
        return result

    def get_sum(self, _df):
        """
        根据start_value, end_value过滤总市值
        """
        cur_df = _df.copy()
        value_df = cur_df.groupby(['日期', "板块名称"]).agg(
            {"涨跌幅": "mean", "总市值": "sum"})
        # value_df.reset_index(inplace=True)
        return value_df

    def get_range(self, _df):  #
        """
        按涨跌幅统计
        """
        # db = df.loc['2023-03-01']
        cur_df = _df.copy()
        bins = [-20, -9.97, -5, -3, -0.099, 0.099, 3, 5, 9.97, 20]
        # bins = list(range(-11, 12))
        cuts = pd.cut(cur_df['涨跌幅'], bins=bins)
        pct_chg_list = cur_df.groupby(["日期", "板块名称", cuts])['涨跌幅'].count()
        cur_df = pct_chg_list.unstack()
        return cur_df

    def runit(self, _df, info):
        for key, value in OPTION_DICT.items():
            start_value, end_value = value
            cur_df = _df.copy()
            if key != "all":
                cur_df = cur_df[(cur_df['总市值'] >= (start_value)*100_000_000)
                                & (cur_df['总市值'] <= (end_value)*100_000_000)]
            result = self.get_count(cur_df)
            value_df = self.get_sum(cur_df)
            final_df = result.join(value_df, on=["日期", "板块名称"])
            # final_df.dropna(inplace=True, axis=0)
            # 将Salary列格式化为亿元
            final_df['总市值亿元'] = final_df['总市值'].apply(
                lambda x: '{:.2f}'.format(x/100000000))

            db = self.get_range(cur_df)
            result = pd.merge(final_df, db, on=["日期", '板块名称'])
            result.reset_index(inplace=True, level=[0, 1])
            # 获得字段的前八列
            a = result.columns[:9].to_list()
            a.extend(RANGE)
            result.columns = a

            # 计算冰点和沸点
            # hot_ice_df = self.create_hot_ice(result)
            # create_another_hot
            hot_ice_df = self.create_another_hot(cur_df)
            print("x"*10)
            print(hot_ice_df[(hot_ice_df['板块名称'] == "游戏") &
                  (hot_ice_df['日期'] == "2023-03-24")])
            print("-"*10)
            hot_date = self.get_hot_date(hot_ice_df)
            ice_date = self.get_ice_date(hot_ice_df)
            final_hot = self.calcu_hot(hot_ice_df, hot_date)
            hot_ice_df = pd.merge(hot_ice_df, final_hot, on=['日期', '板块名称'])
            print("x"*20)
            print(hot_ice_df[(hot_ice_df['板块名称'] == "游戏") &
                  (hot_ice_df['日期'] == "2023-03-24")])
            print("-"*20)
            ice_hot = self.calcu_ice(hot_ice_df, ice_date)
            finished = pd.merge(hot_ice_df, ice_hot, on=['日期', '板块名称'])
            print("x"*50)
            print(finished[(finished['板块名称'] == "游戏") &
                  (finished['日期'] == "2023-03-24")])
            print("-"*50)
            result = pd.merge(result, finished, on=['日期', '板块名称'])
            print("x"*70)
            print(result[(result['板块名称'] == "游戏") &
                  (result['日期'] == "2023-03-24")])
            print("-"*70)

            self.to_csv(result, info+(key,))

    def create_another_hot(self, data):
        hot = data.groupby(["日期", "板块名称"]).apply(lambda x: all(x['涨跌幅'] > 0))

        # 重置索引
        hot = hot.reset_index()
        ice = data.groupby(["日期", "板块名称"]).apply(lambda x: all(x['涨跌幅'] < 0))
        ice = ice.reset_index()
        ice.columns = ["日期", "板块名称", '冰点']
        # 重命名列名
        hot.columns = ["日期", "板块名称", '沸点']
        result = pd.merge(ice, hot, on=["日期", "板块名称"])
        return result

    def create_hot_ice(self, data):

        daily_data = pd.DataFrame(columns=["日期", "板块名称", "沸点", '冰点'])
        grouped_data = data.groupby("板块名称")

        # 遍历每个板块
        # 按照 date 和 sector 两个字段进行分组
        grouped_data = data.groupby(["日期", "板块名称"])

        # 遍历每个分组
        for (date, sector), group_data in grouped_data:
            # 获取当日所有股票的涨跌幅数据
            # 获取该分组中股票的涨跌幅情况
            day_data = group_data["涨跌幅"]
            # day_data = sector_data.loc[sector_data["日期"] == date, "涨跌幅"]

            # 判断当日的涨跌幅情况是否全为正数，全为负数，还是既有正数又有负数
            if all(day_data > 0):
                hot = 1
                cold = 0
            elif all(day_data < 0):
                hot = 0
                cold = 1
            else:
                hot = 0
                cold = 0

            # 将结果添加到 daily_data 中
            # daily_data = daily_data.append(
            #     {"日期": date, "板块名称": sector, "沸点": hot, "冰点": cold}, ignore_index=True)
            daily_data = pd.concat([daily_data, pd.DataFrame(
                {"日期": date, "板块名称": sector, "沸点": hot, "冰点": cold}, index=[0])], ignore_index=True)
        # 将 daily_data 合并回原始 DataFrame 中
        # data = pd.merge(data, daily_data, on=["日期", "板块名称"])
        return daily_data

    def get_hot_date(self, df):
        mydf = df.copy()
        # 找到冰点为true的日期
        hot_dates = mydf.groupby("板块名称").apply(
            lambda x: x[x['沸点'] == True])[["日期", "沸点"]]
        # true_ice_dates.columns=["日期"]
        # true_ice_dates = true_ice_dates.reset_index(drop=True).loc["日期", "板块名称"]
        hot_dates.reset_index(inplace=True)

        hot_dates = hot_dates[["日期", "板块名称"]]
        return hot_dates

    def get_ice_date(self, df):

        # 找到冰点为true的日期
        mydf = df.copy()
        ice_dates = mydf.groupby("板块名称").apply(
            lambda x: x[x['冰点'] == True])[["日期", "冰点"]]
        # true_ice_dates.columns=["日期"]
        # true_ice_dates = true_ice_dates.reset_index(drop=True).loc["日期", "板块名称"]
        ice_dates.reset_index(inplace=True)

        ice_dates = ice_dates[["日期", "板块名称"]]
        return ice_dates

    # 计算最近的冰点为true的天数

    def caculate_hot_date(self, specified_date, sect, hot_dates):

        dt_series = hot_dates[hot_dates['板块名称'] ==
                              sect]['日期'].apply(lambda x: x.date())
        # print(sect)
        time_list = dt_series.to_list()
        # print(time_list)
        if len(time_list) == 0:
            return 0
        # specified_date = specified_date.date()
        # 判断指定日期是否落在时间list中的区间
        diff_days = 0
        if specified_date in time_list:
            return -1
        if specified_date < time_list[0]:
            nearest_date = time_list[0]
            diff_days = 0

        elif specified_date > time_list[-1]:
            nearest_date = time_list[-1]
            diff_days = (specified_date-nearest_date).days
        else:
            for i in range(len(time_list) - 1):
                if time_list[i] <= specified_date < time_list[i+1]:
                    nearest_date = time_list[i]
                    diff_days = (specified_date-nearest_date).days
                    break
        return diff_days

    # 计算最近的冰点为true的天数

    def caculate_ice_date(self, specified_date, sect, ice_dates):
        dt_series = ice_dates[ice_dates['板块名称'] ==
                              sect]['日期'].apply(lambda x: x.date())
        # print(sect)
        time_list = dt_series.to_list()
        # print(time_list)
        if len(time_list) == 0:
            return 0
        # specified_date = specified_date.date()
        # 判断指定日期是否落在时间list中的区间
        diff_days = 0
        if specified_date in time_list:
            return -1
        if specified_date < time_list[0]:
            nearest_date = time_list[0]
            diff_days = 0

        elif specified_date > time_list[-1]:
            nearest_date = time_list[-1]
            diff_days = (specified_date-nearest_date).days
        else:
            for i in range(len(time_list) - 1):
                if time_list[i] <= specified_date < time_list[i+1]:
                    nearest_date = time_list[i]
                    diff_days = (specified_date-nearest_date).days
                    break
        return diff_days

    def calcu_hot(self, df, hot_date):
        """
        计算沸点天数
        """
        mydata = []
        grouped = df.groupby(["板块名称", "日期"])
        for group_name, group_data in grouped:
            # print(type(group_name[1]))
            re = self.caculate_hot_date(
                group_name[1].date(), group_name[0], hot_date)
            mydata.append([group_name[0], group_name[1], re])
        # data = result.groupby(["板块名称","日期"]).apply(
        #     lambda row: 0 if row["冰点"].any() else mydate(row["日期"], row["板块名称"]))
        # data = result.groupby(["板块名称","日期"]).apply(lambda row: 0 if row["冰点"].any() else 100)
        # data
        final_hot = pd.DataFrame(mydata)
        final_hot.columns = ["板块名称", '日期', "距上次沸点天数"]
        final_hot['日期'] = pd.to_datetime(final_hot['日期'])
        return final_hot

    def calcu_ice(self, df, ice_date):
        """
        计算冰点天数
        """
        mydata = []
        grouped = df.groupby(["板块名称", "日期"])
        for group_name, group_data in grouped:
            # print(type(group_name[1]))
            re = self.caculate_ice_date(
                group_name[1].date(), group_name[0], ice_date)
            mydata.append([group_name[0], group_name[1], re])
        # data = result.groupby(["板块名称","日期"]).apply(
        #     lambda row: 0 if row["冰点"].any() else mydate(row["日期"], row["板块名称"]))
        # data = result.groupby(["板块名称","日期"]).apply(lambda row: 0 if row["冰点"].any() else 100)
        # data
        ice_hot = pd.DataFrame(mydata)
        ice_hot.columns = ["板块名称", '日期', "距上次冰点天数"]
        ice_hot['日期'] = pd.to_datetime(ice_hot['日期'])
        return ice_hot

    def pipeline(self):
        """
        生成最后板块的统计数据
        """
        df_dict = self.create()
        capital_dict = self.get_capital_dict()

        for key, df in tqdm(df_dict.items()):
            df = self.calcu_capital(df, capital_dict)

            self.runit(df, key)

            print(f"finish {key}")


if __name__ == "__main__":
    sector = Sector()
    sector.pipeline()
