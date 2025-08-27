import pandas as pd
import streamlit as st

st.subheader('Toggle')
toggle = st.toggle(
    'Turn on the switch!', value=True
)
if toggle:
    st.text('Switch on!')
else:
    st.text('Switch off!')

st.divider()

st.subheader('selectbox')

code = '''
option = st.selectbox(
label='Your selection is',
options=['Car', 'Airplane', 'Train', 'Ship'],
index=None,
placeholder='Select transportation'
)
st.text('You Selected: {}'.format(option))
'''
st.code(code, language='python')



option = st.selectbox(
label='Your selection is',
options=['Car', 'Airplane', 'Train', 'Ship'],
index=None,
placeholder='Select transportation'
)
st.text('You Selected: {}'.format(option))

st.divider()

st.subheader('Radio Button')

code = '''
option = st.radio(
'What is your favorite movie genre',
["Comedy", "Drama", "Documentary"],
captions = ['Laugh out loud', 'Get the popcorn', 'Never stop learning']
)
if option:
st.text('You Selected {}'.format(option))
'''
st.code(code, language='python')

option = st.radio(
    'Whais your favorite movie genre',
    ['Comedy','Drama','Documentary'],
    captions=['Laugh out loud', 'Get the popcorn', 'Never stop learning']
)
if option:
    st.text('You Selected {}'.format(option))
    
st.divider()
st.subheader('Multi Select')


option = st.multiselect(
    label='Your Selection is',
    options=['Car', 'Airplane', 'Train', 'Ship'],
    placeholder='Select Transportation'
)
st.text('You Selected {}'.format(option))