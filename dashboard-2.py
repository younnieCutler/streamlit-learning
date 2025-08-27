import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# MAIN PAGE
st.title(':cloud: Data Analytics - CO2 Emission')

st.write(
    '''
    こんにちは。このページはシンプルなデータ分析ウェブダッシュボードを
    Python Streamlitライブラリで実装したものです。
    '''
)
st.divider()


@st.cache_data
def load_data():
    return pd.read_csv("datasets/CO2_emissions/CO2_emissions.csv")

df = load_data()

st.subheader(
'Analysis of Engine Sizes'
)
col1, col2 = st.columns(2)
with col1:
    st.write(
    '''
    The box plot of engine sizes by automotive manufacturer. What
    types of engine sizes do manufacturers produce the most for each brand?
    '''
    )
with col2:
    fig1 = px.box(
    data_frame=df.sort_values('Engine Size(L)', ascending=False),
    x='Make', y='Engine Size(L)', width=800, height=600, points='all'
    )
st.plotly_chart(fig1)
st.divider()

st.subheader('Analysis of Fuel consumption')

col3, col4 = st.columns(2)
with col3:
    st.write(
    '''
    The scatter plot graph illustrating fuel efficiency based on engine sizes.
    Which manufacturer might have lower fuel efficiency within the same engine size?
    Which manufacturer might have higher fuel efficiency within the same engine size?
    '''
    )
    st.selectbox(
        'Select Y-axis: ',
        [
            'Fuel Consumption City (L/100 km)',
            'Fuel Consumption Hwy (L/100 km)',
            'Fuel Consumption Comb (L/100 km)'
        ],
        key='fig2_yaxis'
    )
with col4 :
    fig2 = px.scatter(
        data_frame=df, x='Engine Size(L)', y=st.session_state['fig2_yaxis'],
        width=500, color='Make', trendline='ols', trendline_scope='overall'
    )
    st.plotly_chart(fig2)

st.divider()

st.subheader('Analysis of Carbon Emissions')

col5, col6 = st.columns(2)
with col5 :
    st.write(
        '''
        The scatter plot graph depicting the correlation between fuel efficiency and
        carbon emissions, with color differentiation for each manufacturer.
        Which manufacturer might have higher carbon emissions within the same fuel
        efficiency range?
        '''
    )
    st.selectbox(
        'Slect X-axis:',
        [
            'Fuel Consumption City (L/100 km)',
            'Fuel Consumption Hwy (L/100 km)',
            'Fuel Consumption Comb (L/100 km)'
            ],
        key='fig3_xaxis'
    )
with col6 :
    fig3 = px.scatter(
        data_frame=df, x=st.session_state['fig3_xaxis'], y='CO2 Emissions(g/km)',
        width=500, color='Make', trendline='ols', trendline_scope='overall'
    )
    st.plotly_chart(fig3)