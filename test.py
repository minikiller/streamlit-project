import pandas as pd
import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode


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
    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        height=400
    )

    return selection


@st.cache_data
def get_code_data():
    df = pd.read_csv(
        "data/板块名称_股票对应.csv", index_col=0, dtype={"代码": object})
    return df


df = get_code_data()
result = aggrid_interactive_table(df)
# if not result:
select =result["selected_rows"]
if len(select)>0:
    st.write(select)
    st.write(select[0]['板块名称'])
    # "板块名称"
# st.write(result.get_selected_df())
# st.warning(type(result))
