# 发布内容更新

## 2023-03-25 更新

> 完成按照总市值区间过滤数据，形成五个按照板块分组结果的文件
```
   result_0-100_20230325.csv

   result_100-500_20230325.csv

   result_500-1000_20230325.csv

   result_1000-30000_20230325.csv

   result_all_20230325.csv
```

> 修复柱形图的x轴title和x轴过于紧密的问题：

```python
# 增加数值
fig.update_layout(autosize=True, margin=dict(
            l=50, r=50, t=50, b=50),)
```