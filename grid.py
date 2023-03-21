import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd

# 安装 streamlit-aggrid 库
# !pip install streamlit-aggrid

# 导入 streamlit-aggrid 库
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# 创建示例数据集
data = {
    'Name': ['Tom', 'Jack', 'Steve', 'Ricky'],
    'Age': [28, 34, 29, 42],
    'Salary': [35000, 45000, 30000, 50000]
}
df = pd.DataFrame(data)

# 创建 GridOptionsBuilder 对象
gb = GridOptionsBuilder.from_dataframe(df)

# 设置一些自定义属性
gb.configure_default_column(
    groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

# 创建 GridOptions 对象
go = gb.build()

# 在 Streamlit 中显示数据网格
grid_result = AgGrid(
    df,
    gridOptions=go,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    width='100%',
    height='600px',
    theme='streamlit'
)

# 显示修改后的数据
if grid_result['data']:
    st.write('修改后的数据：')
    st.write(pd.DataFrame(grid_result['data']))
