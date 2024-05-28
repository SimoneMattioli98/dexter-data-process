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
    min_df, min_nan_temperature = clean_up_temperature_csv(min_temp_file)

    min_df["year"] = pd.to_datetime(min_df["date"], format="%d/%m/%Y").dt.year

    # Ottieni l'elenco degli anni disponibili nel dataset
    min_available_years = sorted(min_df["year"].unique())

    # Seleziona gli anni da visualizzare con uno slider
    min_selected_years = st.slider(
        "Select years to display",
        min_value=min(min_available_years),
        max_value=max(min_available_years),
        value=(min(min_available_years), max(min_available_years)),
    )

    min_df = min_df[
        min_df["year"].isin(range(min_selected_years[0], min_selected_years[1] + 1))
    ]

    del min_df["year"]

    min_df["date_year"] = pd.to_datetime(
        min_df["date"], format="%d/%m/%Y"
    ).dt.to_period("Y")
    min_df_gb_year = min_df.groupby("date_year")

    del min_df["date_year"]

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
        st.subheader("Soft cold")
        st.dataframe(soft_cold)

    with col2:
        st.subheader("Hard cold")
        st.dataframe(hard_cold)

    with col3:
        st.subheader("15° temperature in spring/autumn")
        st.dataframe(first_15_temps_df)

    st.divider()
    st.subheader("Top 10 coldest temperatures per year")
    st.dataframe(min_df_empty, hide_index=True)


st.subheader("Select a csv file with maximum temperatures...")
max_temp_file = st.file_uploader("Choose a file", key=2)

if max_temp_file is not None:

    max_df, max_nan_temperature = clean_up_temperature_csv(max_temp_file)

    max_df["year"] = pd.to_datetime(max_df["date"], format="%d/%m/%Y").dt.year

    # Ottieni l'elenco degli anni disponibili nel dataset
    max_available_years = sorted(max_df["year"].unique())

    # Seleziona gli anni da visualizzare con uno slider
    max_selected_years = st.slider(
        "Select years to display",
        min_value=min(max_available_years),
        max_value=max(max_available_years),
        value=(min(max_available_years), max(max_available_years)),
    )

    max_df = max_df[
        max_df["year"].isin(range(max_selected_years[0], max_selected_years[1] + 1))
    ]

    del max_df["year"]

    max_df["date_year"] = pd.to_datetime(
        max_df["date"], format="%d/%m/%Y"
    ).dt.to_period("Y")
    max_df_gb_year = max_df.groupby("date_year")

    del max_df["date_year"]

    max_df_empty = pd.DataFrame()

    for _, group in max_df_gb_year:
        top_ten = get_top_ten(group.copy(), "temperature", ascending=False)
        max_df_empty = pd.concat([top_ten, max_df_empty], axis=1)

    st.subheader("Top 10 hottest temperatures per year")
    st.dataframe(max_df_empty, hide_index=True)
