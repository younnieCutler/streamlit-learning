import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# Text Input , File Uploader, Slider

st.title("📊 Text Input")

st.markdown(
    '''
    - Streamlit上でtextを入力してもらうボックスを生成。
    一つ目のパラメータがウィジェットのLabelに表示。
    - placeholderパラメータの空欄の文字列設定。
    '''
)

string = st.text_input(
    'Movie Title',
    placeholder='好きな映画のタイトルを入力してください。'
)
if string:
    st.text('あなたが好きな映画は'+ string)
    
st.title("File Uploader")

st.markdown(
    '''
    - Streamlit上でファイルアップロードウィジェット生成。
    一つ目のパラメータがウィジェットのLabelに表示。
    - typeパラメータを通じて受け取れる拡張子を入力。
    - access_multipleパラメータで複数のファイルアップロード可能。
    '''
)
file = st.file_uploader(
    'ファイルを選んでここに', type='csv', accept_multiple_files=False
)
if file is not None:
    df = pd.read_csv(file)
    st.write(df)
    
    
st.title("Slider")

st.markdown(
    '''
    - Streamlit上で値 or 範囲を選択するスライダー生成。
    一つ目のパラメータがウィジェットのLabelに表示。
    - main_value, max_valueパラメータで２つの値渡すと区間選択可能。
    - 上と一緒。
    '''
)
score = st.slider('あなたの点数は：', 0, 100, 1)
st.text('点数 : {}'.format(score))

from datetime import time
start_time, end_time = st.slider(
    'Working time is...',
    min_value=time(0), max_value=time(23),
    value=(time(8), time(18)),
    format='HH:mm'
)
st.text('Working time : {}, {}'.format(start_time, end_time))


st.title("Matplotlib & Seaborn Graph")
st.text(
    '''
    Matplotlib subplotsで生成されたfigure変数をStreamlit pyplot関数に渡す。
    '''
)

df = sns.load_dataset('tips')

fig, ax = plt.subplots()
sns.histplot(df, x='total_bill', ax=ax, hue='time')
st.pyplot(fig)

st.divider()
st.title('Plotpy')
fig2 = px.box(
    data_frame=df, x='day', y='tip',
    facet_col= 'smoker', facet_row='sex',
    width=800, height=800
)
st.plotly_chart(fig2)