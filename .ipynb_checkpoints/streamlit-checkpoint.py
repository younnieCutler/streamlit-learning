import pandas as pd
import streamlit as st

#タイトルを作成する関数
st.title('This is title')
st.header('This is header')
st.subheader('This is subheader')


st.markdown(
    '''
    -This is Markdown.
    This is how to change the color oftext **:red[Red,]** :blue[Blue,] :green[Green.]
    This is **Bold** amd *Italic* text
    '''
)

st.text(
    '''
    This is plain text.
    '''
)

code = '''
This is code
'''
st.code(code, language='python')

#ページを分けるdivide関数
st.divider() 
