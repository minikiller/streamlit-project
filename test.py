import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.graph_objs as go
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode

# 加载数据
df = pd.read_csv('tools/临时冰点沸点.csv')


def aggrid_interactive_table(df: pd.DataFrame, filtered=False):
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
    if filtered:
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
            # column_state=st.session_state.code
        )
    else:
        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            save_settings=True,
            load_settings=True,
            allow_unsafe_jscode=True,
            height=400,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW
        )

    return selection


# 加载数据
# df = pd.read_csv('data.csv')
my_value = st.sidebar.text_input(
    "请输入过滤的板块名字：")

# 在 Streamlit 中显示表格
if "code" in st.session_state:
    result = aggrid_interactive_table(df, filtered=True)
else:
    result = aggrid_interactive_table(df, filtered=False)
# 获取用户的过滤条件
# filter_models = grid_result['filter_models']

# 创建一个空的 DataFrame 用于存储过滤后的结果

# filtered_df = pd.DataFrame(columns=df.columns)
st.write(my_value)

# for key, value in result.items():
#     print(f"key is {key}")
#     print(f"value is {value}")
column_state = result.get("column_state")
if column_state and len(column_state) > 0:
    # print(grid_result)
    st.session_state.code = column_state["column_state"]
# # 根据用户的过滤条件进行筛选
# for filter_model in filter_models:
#     col_id = filter_model['colId']
#     col_type = filter_model['type']
#     filter_obj = filter_model['filter']

#     if col_type == 'text':
#         filter_str = filter_obj['filter']
#         operator = filter_obj['operator']
#         mask = df[col_id].str.contains(filter_str, case=False, na=False)
#         if operator == 'AND':
#             filtered_df = filtered_df[mask]
#         elif operator == 'OR':
#             filtered_df = pd.concat([filtered_df, df[mask]])
#     elif col_type == 'number':
#         filter_value = filter_obj['filter']
#         filter_operator = filter_obj['type']
#         if filter_operator == 'equals':
#             mask = df[col_id] == filter_value
#         elif filter_operator == 'lessThan':
#             mask = df[col_id] < filter_value
#         elif filter_operator == 'greaterThan':
#             mask = df[col_id] > filter_value
#         elif filter_operator == 'inRange':
#             mask = (df[col_id] >= filter_value[0]) & (
#                 df[col_id] <= filter_value[1])
#         filtered_df = filtered_df[mask]
#     elif col_type == 'date':
#         # 类似于数字过滤，不再赘述
#         pass
#     elif col_type == 'set' or col_type == 'multi':
#         # 类似于文本过滤，不再赘述
#         pass

# 在 Streamlit 中显示结果
# st.write(filtered_df)
