import emoji
import pandas as pd
import streamlit as st

from utils import (
    clean_up_temperature_csv,
    get_colds,
    get_top_ten,
    spring_autumn_critical_temperature,
)

thermometer_emoji = emoji.emojize(":thermometer:")

st.set_page_config(layout="wide", page_title="Temperature", page_icon=thermometer_emoji)
st.title(thermometer_emoji + " Temperature")

st.subheader("Select a csv file with minimum temperatures...")
min_temp_file = st.file_uploader("Choose a file", key=1)

if min_temp_file is not None:
    min_df, min_df_gb_year, min_nan_temperature = clean_up_temperature_csv(
        min_temp_file
    )
    soft_cold, hard_cold = get_colds(min_df)
    del min_df["year_index"]
    min_df_empty = pd.DataFrame()

    first_15_temps_df = pd.DataFrame(
        index=min_df_gb_year.groups.keys(),
        columns=["Spring Date 15", "Autumn Date <15"],
    )

    for i, (year, group) in enumerate(min_df_gb_year):
        first_spring_temp_15, first_autumn_temp_below_15 = (
            spring_autumn_critical_temperature(first_15_temps_df, year, group)
        )

        top_ten = get_top_ten(group.copy(), "temperature")
        min_df_empty = pd.concat([top_ten, min_df_empty], axis=1)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.text("SOFT COLD")
        st.dataframe(soft_cold)

    with col2:
        st.text("HARD COLD")
        st.dataframe(hard_cold)

    with col3:
        st.text("15° TEMPERATURES IN SPRING/AUTUMN ")
        st.dataframe(first_15_temps_df)

    st.divider()
    st.text("TOP TEN COLDEST TEMPERATURE PER YEAR")
    st.dataframe(min_df_empty, hide_index=True)


st.subheader("Select a csv file with maximum temperatures...")
max_temp_file = st.file_uploader("Choose a file", key=2)

if max_temp_file is not None:

    max_df, max_df_gb_year, max_nan_temperature = clean_up_temperature_csv(
        max_temp_file
    )

    max_df_empty = pd.DataFrame()

    for _, group in max_df_gb_year:
        top_ten = get_top_ten(group.copy(), "temperature", ascending=False)
        max_df_empty = pd.concat([top_ten, max_df_empty], axis=1)

    st.text("TOP TEN HOTTEST TEMPERATURE PER YEAR")
    st.dataframe(max_df_empty, hide_index=True)
