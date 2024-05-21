import pandas as pd
import streamlit as st

from utils import clean_up_csv, get_cold_dates, get_top_ten

st.set_page_config(page_title="Temperature", page_icon="📊")
st.title("📊 Temperature")

st.subheader("Select a csv file with minimum temperatures...")
min_temp_file = st.file_uploader("Choose a file", key=1)
st.subheader("Select a csv file with maximum temperatures...")
max_temp_file = st.file_uploader("Choose a file", key=2)
st.subheader("Select a csv file with  medium temperatures...")
mean_temp_file = st.file_uploader("Choose a file", key=3)

if min_temp_file is not None:
    min_df_gb_year, min_nan_temperature = clean_up_csv(min_temp_file)

    min_df_empty = pd.DataFrame()

    current_soft = [-1, -1]
    current_hard = [-1, -1]
    prev_soft = [-1, -1]
    prev_hard = [-1, -1]
    first_soft_negative_second_half = 1
    first_hard_negative_second_half = 1
    last_soft_negative_second_half = 1
    last_hard_negative_second_half = 1
    first_soft_negative_first_half = 1
    first_hard_negative_first_half = 1
    last_soft_negative_first_half = 1
    last_hard_negative_first_half = 1

    last_year_last_soft_cold = 1
    last_year_last_hard_cold = 1

    for i, (_, group) in enumerate(min_df_gb_year):
        first_half = group.iloc[:180].dropna()
        second_half = group.iloc[180:].dropna()

        if second_half.size > 0:
            (
                first_soft_negative_second_half,
                last_soft_negative_second_half,
                first_hard_negative_second_half,
                last_hard_negative_second_half,
            ) = get_cold_dates(second_half)

        if first_half.size > 0:
            (
                first_soft_negative_first_half,
                last_soft_negative_first_half,
                first_hard_negative_first_half,
                last_hard_negative_first_half,
            ) = get_cold_dates(first_half)

        current_soft[0] = first_soft_negative_second_half
        current_hard[0] = first_hard_negative_second_half
        if i != 0:
            prev_soft[1] = last_soft_negative_first_half
            prev_hard[1] = last_hard_negative_first_half

        prev_hard = current_hard
        prev_soft = current_soft
        current_soft = [-1, -1]
        current_hard = [-1, -1]

    exit(1)

    # |-x---X--------X---x-----|------------y-----|

    # giro 1
    # prev_soft = [y1, x2]
    # curr_soft = [y2, -1]

    # giro 1
    # prev_soft = [y0, x1]          [y0, x1]
    # curr_soft = [y1, -1]
    # next_soft = [-1, -1]

    # giro 2
    # prev_soft = [y1, x2]          [y0, x1]
    # curr_soft = [y2, -1]
    # next_soft = [-1, -1]

    #     top_ten = get_top_ten(group.copy())
    #     min_df_empty = pd.concat([top_ten, min_df_empty], axis=1)

    #     st.dataframe(min_df_empty, hide_index=True)
    # st.dataframe(min_df_empty, hide_index=True)

if max_temp_file is not None:

    max_df_gb_year, max_nan_temperature = clean_up_csv(max_temp_file)

    max_df_empty = pd.DataFrame()

    for _, group in min_df_gb_year:
        top_ten = get_top_ten(group.copy(), ascending=False)
        max_df_empty = pd.concat([top_ten, max_df_empty], axis=1)

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
