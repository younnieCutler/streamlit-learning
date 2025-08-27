import pandas as pd
import streamlit as st

i = 0

st.header('Session state example1')

plus_one_bad = st.button(
    label='+1',
)

if plus_one_bad:
    i += 1
st.text('i = {}'.format(i))

st.divider()

st.header('Session state example2')

if 'i' not in st.session_state:
    st.session_state['i'] = 0

plus_one_good = st.button(
    label='+1',
    key='btn_plus1'
)

if plus_one_good:
    st.session_state['i'] += 1
st.text('i = {}'.format(st.session_state['i']))

st.divider()

@st.cache_data
def expensive_computation(a, b):
    st.text('Result: {}'.format(a+b))

result = st.button(
    'Caculate', on_click=expensive_computation, args=(3, 4)
)