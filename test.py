import streamlit as st
import plotly.express as px


import streamlit as st
import datetime
import pytz

# 获取当前时区的时间
tz = pytz.timezone('Asia/Shanghai')
current_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

# 显示当前时间
st.write("当前时间是：", current_time)
# 创建两个示例数据集
df1 = px.data.gapminder().query("continent=='Asia'")
df2 = px.data.gapminder().query("continent=='Europe'")

# 使用beta_columns创建两个列
col1, col2 = st.beta_columns(2)

# 在每个列中分别放置一个plotly图形
with col1:
    fig1 = px.scatter(df1, x="gdpPercap", y="lifeExp",
                      color="country", log_x=True, size_max=60)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.scatter(df2, x="gdpPercap", y="lifeExp",
                      color="country", log_x=True, size_max=60)
    st.plotly_chart(fig2, use_container_width=True)
