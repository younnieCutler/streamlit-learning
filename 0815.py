import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image

st.title('this is page')

x_options = ['day', 'size']
y_options = ['total_bill', 'tip']
hue_options = ['smoker', 'sex']
df = sns.load_dataset('tips')
x_options = st.selectbox(
    'Select X-axis',
    index=None,
    options=x_options
)
y_options = st.selectbox(
    'Select Y-axis',
    index=None,
    options=y_options
)
hue_options = st.selectbox(
    'Select Hue',
    index=None,
    options=hue_options
)

if(x_options != None) & (y_options != None):
    if hue_options != None:
        fig3 = px.box(
            data_frame=df, x=x_options, y=y_options,
            color=hue_options, width=500
        )
    else:
        fig3 = px.box(
            data_frame=df, x=x_options, y=y_options,
            width=500
        )
    st.plotly_chart(fig3)
img1 = Image.open('datasets/images/image1.jpg')
img2 = Image.open('datasets/images/image2.jpg')
img3 = Image.open('datasets/images/image3.jpg')

with st.sidebar:
    st.title('This is sidebar')
    side_option = st.multiselect(
        label='好scきなモータースポーツを選んでください。',
        options=['Monster Truck', 'Fomuler', '24h-lemans', 
                 '24h-daytona'],
        placeholder='select transportation'
    )
st.write(f"選択したモータースポーツは：{side_option}")

col0, col1, col2 = st.columns(3)
with col0:
    st.header('Landscape')
    st.image(img1, width=300, caption='Image Source : Unsplash')

with col1:
    st.header('Lemonade')
    st.image(img2, width=300, caption='Image Source : Unsplash')

with col2:
    st.header('Cocktail')
    st.image(img3, width=300, caption='Image Source : Unsplash')
    
tab1, tab2= st.tabs(['Table', 'Graph'])

df = pd.read_csv('datasets/medical_cost/medical_cost.csv')
df = df.query('region == "northwest"')

with tab1:
    st.table(df.head(5))
with tab2:
    fig = px.scatter(
        data_frame=df, x='bmi', y='charges'
    )
    st.plotly_chart(fig)
with st.expander("See datatable"):
    st.table(df.head(5))
