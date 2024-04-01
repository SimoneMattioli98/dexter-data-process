import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
# Page title
st.set_page_config(page_title='Interactive Data Explorer', page_icon='📊')
st.title('📊 Interactive Data Explorer')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
  
st.subheader('Which Movie Genre performs ($) best at the box office?')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)# Load data
  df = df.drop(["date_end"], axis=1)
  df.rename(columns={'date_start': "date"}, inplace=True)
  df["date"] = pd.to_datetime(df["date"]).dt.date
  nan_temperature: int = df["temperature"].isna().sum()
  df["temperature"] = df["temperature"].round()

  year_list = pd.to_datetime(df["date"]).dt.year.unique()
  year_selection = st.slider('Select year duration', year_list.min(), year_list.max(), (year_list.min(), year_list.max()))
  year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))
  df_selection = df[pd.to_datetime(df["date"]).dt.year.isin(year_selection_list)]
  reshaped_df = df_selection.pivot_table(index='date', dropna=False)

  df_editor = st.data_editor(reshaped_df, height=400, use_container_width=True,
                            num_rows="dynamic")
  df_chart = df_editor.reset_index()
  chart = alt.Chart(df_chart).mark_line().encode(
              x=alt.X('date:T', title='Date'),  #O N Q T G
              y=alt.Y('temperature', title='Temperature (C°)'),
              ).properties(height=700)
  st.altair_chart(chart, use_container_width=True)

  fn = 'scatter.png'
  plt.savefig(chart)
  with open(fn, "rb") as img:
    btn = st.download_button(
        label="Download image",
        data=img,
        file_name=fn,
        mime="image/png"
    )


df = pd.read_csv('data/movies_genres_summary.csv')
df.year = df.year.astype('int')

# Input widgets
## Genres selection
genres_list = df.genre.unique()
genres_selection = st.multiselect('Select genres', genres_list, ['Action', 'Adventure', 'Biography', 'Comedy', 'Drama', 'Horror'])

## Year selection
year_list = df.year.unique()
year_selection = st.slider('Select year duration', 1986, 2006, (2000, 2016))
year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

df_selection = df[df.genre.isin(genres_selection) & df['year'].isin(year_selection_list)]
reshaped_df = df_selection.pivot_table(index='year', columns='genre', values='gross', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='year', ascending=False)


# Display DataFrame

df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
                            column_config={"year": st.column_config.TextColumn("Year")},
                            num_rows="dynamic")
df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='genre', value_name='gross')

# Display chart
chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('year:N', title='Year'),
            y=alt.Y('gross:Q', title='Gross earnings ($)'),
            color='genre:N'
            ).properties(height=320)
st.altair_chart(chart, use_container_width=True)
