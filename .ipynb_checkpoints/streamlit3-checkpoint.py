import pandas as pd
import streamlit as st


st.subheader('Toggleの使い方')
st.markdown
toggle = st.toggle(
    'Turn on the switch!', value=True
)
if toggle:
    st.text('Switch on!')
else:
    st.text('Switch off!')

st.divider()

st.subheader('selectboxの使い方')

