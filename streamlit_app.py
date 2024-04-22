import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
# Page title
st.set_page_config(page_title='Dexter data processing', page_icon='📊')
st.title('📊 Dexter data processing')

#with st.expander('About this app'):
#  st.markdown('**What can this app do?**')
#  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
#  st.markdown('**How to use the app?**')
#  st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
  

if st.button("Temperature"):
    st.switch_page("pages/temperature.py")
