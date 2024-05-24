import pandas as pd
import streamlit as st

from utils import (
    clean_up_csv,
    get_colds,
    get_top_ten,
    spring_autumn_critical_temperature,
)

st.set_page_config(page_title="Temperature", page_icon="📊")
st.title("📊 Temperature")

st.subheader("Select a csv file with minimum temperatures...")
min_temp_file = st.file_uploader("Choose a file", key=1)

if min_temp_file is not None:
    min_df, min_df_gb_year, min_nan_temperature = clean_up_csv(min_temp_file)
    soft_cold, hard_cold = get_colds(min_df)
    del min_df["year_index"]
    min_df_empty = pd.DataFrame()

    first_15_temps_df = pd.DataFrame(
        index=min_df_gb_year.groups.keys(),
        columns=["Spring Date 15", "Autumn Date <15"],
    )

    for i, (year, group) in enumerate(min_df_gb_year):
        first_spring_temp_15, first_autumn_temp_below_15 = (
            spring_autumn_critical_temperature(group)
        )

        first_15_temps_df.loc[year, "Spring Date 15"] = (
            (pd.to_datetime(first_spring_temp_15["date"]).dt.date.iloc)[0]
            if not first_spring_temp_15.empty
            else None
        )
        first_15_temps_df.loc[year, "Autumn Date <15"] = (
            (pd.to_datetime(first_autumn_temp_below_15["date"]).dt.date.iloc)[0]
            if not first_autumn_temp_below_15.empty
            else None
        )

        top_ten = get_top_ten(group.copy())
        min_df_empty = pd.concat([top_ten, min_df_empty], axis=1)

    col1, col2 = st.columns(2)

    with col1:
        st.text("SOFT COLD")
        st.dataframe(soft_cold)

    with col2:
        st.text("HARD COLD")
        st.dataframe(hard_cold)

    st.divider()

    st.text("15° TEMPERATURES IN SPRING/AUTUMN ")
    st.dataframe(first_15_temps_df)

    st.divider()
    st.text("TOP TEN COLDEST TEMPERATURE PER YEAR")
    st.dataframe(min_df_empty, hide_index=True)


st.subheader("Select a csv file with maximum temperatures...")
max_temp_file = st.file_uploader("Choose a file", key=2)

if max_temp_file is not None:

    max_df, max_df_gb_year, max_nan_temperature = clean_up_csv(max_temp_file)

    max_df_empty = pd.DataFrame()

    for _, group in max_df_gb_year:
        top_ten = get_top_ten(group.copy(), ascending=False)
        max_df_empty = pd.concat([top_ten, max_df_empty], axis=1)

    st.text("TOP TEN HOTTEST TEMPERATURE PER YEAR")
    st.dataframe(max_df_empty, hide_index=True)


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
#   year_selection = st.slider('Select year duration',
#   year_list.min(), year_list.max(), (year_list.min(), year_list.max()))
#   year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))
#   df_selection = df[pd.to_datetime(df["date"]).dt.year.isin(year_selection_list)]
#   reshaped_df = df_selection.pivot_table(index='date', dropna=False)

#   df_editor = st.data_editor(reshaped_df, height=400, use_container_width=True,
#                             num_rows="dynamic")
#   df_chart = df_editor.reset_index()

#   if graph_type == "***Line***":

#     chart = alt.Chart(df_chart).mark_line().encode(
#               x=alt.X('date:T', title='Date',
#               axis=alt.Axis(format="%Y %B", labelAngle=-45)),  #O N Q T G
#               y=alt.Y('temperature', title='Temperature (C°)'),
#               )

#     st.altair_chart(chart, use_container_width=True)

#     chart = alt.Chart(df_chart).mark_line().encode(
#               x=alt.X('date:T', title='Date',
#               axis=alt.Axis(format="%Y %B", labelAngle=-45)),  #O N Q T G
#               y=alt.Y('temperature', title='Temperature (C°)'),
#               ).properties(
#         width=1920,
#         height=1080
#       )

#   if graph_type == "***Bars***":
#     chart = alt.Chart(df_chart).mark_bar().encode(
#               x=alt.X('date:T', title='Date', axis=alt.Axis
#               (format="%Y %B", labelAngle=-45)),  #O N Q T G
#               y=alt.Y('temperature', title='Temperature (C°)'),
#               )

#     st.altair_chart(chart, use_container_width=True)

#     print(df_chart)

#     chart = alt.Chart(df_chart).mark_bar().encode(
#               x=alt.X('date', title='Date',
#               axis=alt.Axis(labelAngle=-45)),  #O N Q T G
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
