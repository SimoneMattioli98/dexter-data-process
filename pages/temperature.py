import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(page_title='Temperature', page_icon='📊')
st.title('📊 Temperature')

st.subheader('Select a csv file with minimum temperatures...')
min_temp_file = st.file_uploader("Choose a file", key=1)
st.subheader('Select a csv file with maximum temperatures...')
max_temp_file = st.file_uploader("Choose a file", key=2)
st.subheader('Select a csv file with  medium temperatures...')
mean_temp_file = st.file_uploader("Choose a file", key=3)


if min_temp_file is not None:
    min_df = pd.read_csv(min_temp_file) # Load data
    min_df = min_df.drop(["date_end"], axis=1)
    min_df.rename(columns={'date_start': "date"}, inplace=True)
    min_df["date"] = pd.to_datetime(min_df["date"]).dt.date
    min_df["date"] = pd.to_datetime(min_df["date"])
    min_nan_temperature: int = min_df["temperature"].isna().sum()
    min_df_gb_year = min_df.groupby(pd.PeriodIndex(min_df["date"], freq="Y"))
    
    df_empty = pd.DataFrame()

    for _, group in min_df_gb_year:
        print("WEEEEEEEEEE")
        group["temp"] = group["temperature"].round().astype('Int64')
        group_sorted = group.sort_values(by='temp')
        top_ten = group_sorted.iloc[:10]
        year = top_ten['date'].iloc[0].year
        top_ten["date"] = top_ten["date"].dt.strftime('%m-%d')
        top_ten.columns = pd.MultiIndex.from_product([[str(year)], top_ten.columns])
        top_ten = top_ten.reset_index(drop=True)
        df_empty = pd.concat([top_ten, df_empty], axis=1)
        df_string = df_empty.to_string(header=True, index=False)

    
    print(df_string)
    
    st.table(df_empty)




# if uploaded_file is not None:
#   df = pd.read_csv(uploaded_file)# Load data
#   df = df.drop(["date_end"], axis=1)
#   df.rename(columns={'date_start': "date"}, inplace=True)
#   df["date"] = pd.to_datetime(df["date"]).dt.date
#   nan_temperature: int = df["temperature"].isna().sum()

#   st.subheader(f'Missing data: {nan_temperature}')

#   graph_type = st.radio(
#     "Select graph type",
#     ["***Line***", "***Bars***"],
#   )

#   df = df.groupby(pd.PeriodIndex(df["date"], freq="M"))
#   df = df['temperature'].mean().reset_index()
#   df["temperature"] = df["temperature"].round()
#   df["date"] = df["date"].dt.to_timestamp('M')
#   df["date"] = pd.to_datetime(df["date"]).dt.date
#   df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))

#   year_list = pd.to_datetime(df["date"]).dt.year.unique()
#   year_selection = st.slider('Select year duration', year_list.min(), year_list.max(), (year_list.min(), year_list.max()))
#   year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))
#   df_selection = df[pd.to_datetime(df["date"]).dt.year.isin(year_selection_list)]
#   reshaped_df = df_selection.pivot_table(index='date', dropna=False)

#   df_editor = st.data_editor(reshaped_df, height=400, use_container_width=True,
#                             num_rows="dynamic")
#   df_chart = df_editor.reset_index()

#   if graph_type == "***Line***":
  
#     chart = alt.Chart(df_chart).mark_line().encode(
#               x=alt.X('date:T', title='Date', axis=alt.Axis(format="%Y %B", labelAngle=-45)),  #O N Q T G
#               y=alt.Y('temperature', title='Temperature (C°)'),
#               )
    
#     st.altair_chart(chart, use_container_width=True)

#     chart = alt.Chart(df_chart).mark_line().encode(
#               x=alt.X('date:T', title='Date', axis=alt.Axis(format="%Y %B", labelAngle=-45)),  #O N Q T G
#               y=alt.Y('temperature', title='Temperature (C°)'),
#               ).properties(
#         width=1920,
#         height=1080
#       )
    
#   if graph_type == "***Bars***":
#     chart = alt.Chart(df_chart).mark_bar().encode(
#               x=alt.X('date:T', title='Date', axis=alt.Axis(format="%Y %B", labelAngle=-45)),  #O N Q T G
#               y=alt.Y('temperature', title='Temperature (C°)'),
#               )
  
#     st.altair_chart(chart, use_container_width=True)

#     print(df_chart)

#     chart = alt.Chart(df_chart).mark_bar().encode(
#               x=alt.X('date', title='Date', axis=alt.Axis(labelAngle=-45)),  #O N Q T G
#               y=alt.Y('temperature', title='Temperature (C°)'),
#               ).properties(
#         width=1920,
#         height=1080
#       ).configure_axis(
#       labelFontSize=20,
#       titleFontSize=20
#     )


#   file_name = "chart.png"

#   chart.save(file_name)

  
#   with open(file_name, "rb") as file:
#     btn = st.download_button(
#             label="Download image",
#             data=file,
#             file_name=f"graph-{year_selection_list[0]}-{year_selection_list[-1]}.png",
#             mime="image/png"
#           )
    
  
    