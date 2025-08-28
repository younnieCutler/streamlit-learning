import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def load_dataset(path):
    return pd.read_csv(path)

path = '..\python_learning\datasets\CO2_emissions\CO2_Emissions.csv'
df = load_dataset(path)
df.head().T
#hello
makers = df['Vehicle Class'].unique().tolist()
with st.sidebar:
    st.markdown('Filter the data you want to analyze: :tulip:')
    
    st.multiselect(
        'Select the vehicle. class you want to analyze: ',
        makers, default=['TWO-SEATER'],
        key='maker_filter'   
    )
    
st.slider(
'Select the engine size (Liter) you want to analyze: ',
min_value = df['Engine Size(L)'].min(),
max_value = df['Engine Size(L)'].max(),
value=(df['Engine Size(L)'].quantile(0.1), df['Engine Size(L)'].quantile(0.95)),
step=.3,
key='engine_filter'
)
df = df.loc[
(df['Vehicle Class'].isin(st.session_state['maker_filter'])) &
(df['Engine Size(L)'] < st.session_state['engine_filter'][1]) &
(df['Engine Size(L)'] > st.session_state['engine_filter'][0])
]

