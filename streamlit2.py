import pandas as pd
import streamlit as st

st.title('ボタン')

# def button_write():
#     st.write('button activated')
# st.button('Reset', type = 'primary')
# st.button('activated', on_click=button_write)


st.button('Reset', type='primary')
if st.button('activated'):
    st.write('button activated')


active = st.checkbox('I agree')
if active:
    st.text('Great!')

# def checkbox_write():
#     st.write('Great')
    
# st.checkbox('I agree', on_change=checkbox_write)








