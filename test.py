import plotly.graph_objects as go
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
select = result["selected_rows"]
if len(select) > 0:
    st.write(select)
    st.write(select[0]['板块名称'])
    # "板块名称"
# st.write(result.get_selected_df())
# st.warning(type(result))

# create some sample data
data = pd.DataFrame({'x': np.arange(10),
                     'y': np.random.randn(10)})

# create the line plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['x'], y=data['y'], mode='lines'))

# set the title and axis labels
fig.update_layout(title='Line Plot', xaxis_title='X', yaxis_title='Y')

# customize the y-axis tick marks
fig.update_layout(yaxis=dict(
    tickvals=[-20, 0, 20], ticktext=['Low', 'Medium', 'High'], dtick=5))

# display the plot
# fig.show()
st.plotly_chart(fig, use_container_width=True)
