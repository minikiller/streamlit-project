# -*- coding: utf-8 -*-

import requests
import xlwt
import pandas as pd
import time
import json

data = ""
"""
获得股票是否为国企
"""
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'device_id=83b3933a34e5f5f67e0e5d929d72864c;s=cz11extizr;xq_a_token=51d351b43f9ca116112b30f56fbed181c7acbbf4;xqat=51d351b43f9ca116112b30f56fbed181c7acbbf4;xq_r_token=d5c015e44d4eb51cf9fee6298d2cace7b94ba8c8;xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTY4MTI1OTA1MywiY3RtIjoxNjc4ODYzMjMzNDk3LCJjaWQiOiJkOWQwbjRBWnVwIn0.qIuFhFg3Mixj4lv5cr38Nqt7cEZv0SsfZVle2vn5YzWFznATi0VCp_34ZN4KzJfNCiUmLM0OZPAx3MC6Unm0g32Mz1LTnfwZ6M4j3tWj1gVkvn1OQBTFfOthLPiaHMXnDGzC_XwSKe_Aiwg2_jtI4UFuKREZ_a-Y0G6Btxtu3YpYDcd3WAXo7NnLWodDG7MXU6Usl3wAbDVa8w6uFBK35nme1cDOqnxQ33z5ZK0_2j9_0MJ1s0frGuv96SHlrOXlP8lNbNY1b0q9qWhP1QGqqodcmj8cz9WKyxMELfCGX18BSGaJO3F3fLwiTu0tqNbJCUODI84TzMJNRjUgqT416A; u=531678863252671;Hm_lvt_1db88642e346389874251b5a1eded6e3=1677289885,1679042716;Hm_lpvt_1db88642e346389874251b5a1eded6e3=1679042737',
    'Host': 'stock.xueqiu.com',
    # 'Origin': '雪球 - 聪明的投资者都在这里',
    # 'Referer': '雪球-聪明的投资者都在这里',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

# 从baostock获取的all_stock.csv上市公司列表，通过pandas解析，获得公司总数量
# 我这里把csv文件另存成了excel
df = pd.read_csv('all_stock.csv', encoding="utf-8")
height, width = df.shape

# 初始化创建一个上市公司类别的excel文件，用于存储结果
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('company_SHA')

# 遍历深交所A股所有公司列表，使用公司股票代码爬取公司基本信息
# 如果遇到连接问题，记录并重复get4次，如果仍然无法连接，则跳过抓取下一个公司
#
# url = "https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol="+"SH600371"
# res = requests.get(url, headers=headers)
# print(res.json())
# res_dict = json.loads(res.text)
# print(res_dict)
y = height
for x in range(0, height):
    if ("sh" in df.loc[x, "code"]):
        company_id = "SH"+df.loc[x, "code"][3:]
        url = "https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol="+company_id
        print(url)
    elif ("sz" in df.loc[x, "code"]):
        company_id = "SZ"+df.loc[x, "code"][3:]
        url = "https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol="+company_id
    i = 1
    while i <= 4:
        try:
            res = requests.get(url, headers=headers)
            try:
                res_dict = json.loads(res.text)
                break
            except:
                print("Json 解析异常")
        except requests.exceptions.ConnectionError:
            print('ConnectionError -- please wait 3 seconds')
            time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError -- please wait 3 seconds')
            time.sleep(3)
        except Exception as e:
            print(f'未知错误 重新连接 {e}')
            time.sleep(3)
        i += 1

    if (i == 4):
        print(company_id+":该公司无法获取")
        company_type = "无此公司"
        controler = "无实际控制人"
    else:
        if (res_dict['data']['company'] is None or res_dict['data']['company']['classi_name'] is None or res_dict['data']['company']['actual_controller'] is None):
            company_type = "公司无类型"
            controler = "无实际控制人"
        else:
            company_type = res_dict['data']['company']['classi_name']
            controler = res_dict['data']['company']['actual_controller']
    print("剩余:"+str(y)+"个: "+df.loc[x, "code"]+":" +
          df.loc[x, "code_name"]+":"+company_type+" "+controler)

    # 将结果写入excel
    worksheet.write(x, 0, df.loc[x, "code"])
    worksheet.write(x, 1, df.loc[x, "code_name"])
    worksheet.write(x, 2, company_type)
    worksheet.write(x, 3, controler)
    workbook.save('xueqiu2.xls')
    time.sleep(1)
    y -= 1
