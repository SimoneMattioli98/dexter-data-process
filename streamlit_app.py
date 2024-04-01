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
  
st.subheader('Select a csv file with the data to process...')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)# Load data
  df = df.drop(["date_end"], axis=1)
  df.rename(columns={'date_start': "date"}, inplace=True)
  df["date"] = pd.to_datetime(df["date"]).dt.date
  nan_temperature: int = df["temperature"].isna().sum()

  df = df.groupby(pd.PeriodIndex(df["date"], freq="M"))
  df = df['temperature'].mean().reset_index()
  df["temperature"] = df["temperature"].round()
  df["date"] = df["date"].dt.to_timestamp('M')
  df["date"] = pd.to_datetime(df["date"]).dt.date

  year_list = pd.to_datetime(df["date"]).dt.year.unique()
  year_selection = st.slider('Select year duration', year_list.min(), year_list.max(), (year_list.min(), year_list.max()))
  year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))
  df_selection = df[pd.to_datetime(df["date"]).dt.year.isin(year_selection_list)]
  reshaped_df = df_selection.pivot_table(index='date', dropna=False)

  df_editor = st.data_editor(reshaped_df, height=400, use_container_width=True,
                            num_rows="dynamic")
  df_chart = df_editor.reset_index()
  df_chart["date"] = pd.to_datetime(df_chart["date"])

  st.subheader(f'Missing data: {nan_temperature}')


  chart = alt.Chart(df_chart).mark_line().encode(
              x=alt.X('date:T', title='Date'),  #O N Q T G
              y=alt.Y('temperature', title='Temperature (C°)'),
              )
  
  st.altair_chart(chart, use_container_width=True)

  chart = alt.Chart(df_chart).mark_line().encode(
                x=alt.X('date:T', title='Date'),  #O N Q T G
                y=alt.Y('temperature', title='Temperature (C°)'),
                ).properties(
      width=1920,
      height=1080
    )


  
  file_name = "chart.png"

  chart.save(file_name)

  
  with open(file_name, "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name=f"graph-{year_selection_list[0]}-{year_selection_list[-1]}.png",
            mime="image/png"
          )
    