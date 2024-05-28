import emoji
import pandas as pd
import streamlit as st

from utils import (
    clean_up_rain_csv,
    create_download_link,
    order_months,
    plot_annual_rain,
    plot_monthly_rain,
)

rain_emoji = emoji.emojize(":cloud_with_rain:")

st.set_page_config(layout="wide", page_title="Rain", page_icon=rain_emoji)
st.title(rain_emoji + " Rain")

with st.expander("About this app"):
    # Load Markdown content from file
    with open("markdown/about_rain.md") as file:
        markdown_about_app = file.read()
        st.markdown(markdown_about_app)

st.subheader("Select a csv file with rain data...")
rain_file = st.file_uploader("Choose a file", key=1)


if rain_file is not None:
    rain_df, nan_temperature = clean_up_rain_csv(rain_file)

    rain_df["date"] = pd.to_datetime(rain_df["date"], format="%d/%m/%Y")

    # Estrai l'year e il month dalla colonna 'data'
    rain_df["year"] = rain_df["date"].dt.year
    rain_df["month"] = rain_df["date"].dt.strftime("%b")

    # Ottieni l'elenco degli anni disponibili nel dataset
    available_years = sorted(rain_df["year"].unique())

    # Seleziona gli anni da visualizzare con uno slider
    selected_years = st.slider(
        "Select years to display",
        min_value=min(available_years),
        max_value=max(available_years),
        value=(min(available_years), max(available_years)),
    )

    # Raggruppa per year e month e calcola la somma delle rain
    montly_accumulations = (
        rain_df.groupby(["year", "month"])["rain"].sum().reset_index()
    )
    montly_accumulations = order_months(montly_accumulations)

    # Raggruppa per year e calcola la somma delle rain
    annual_accumulations = rain_df.groupby(["year"])["rain"].sum().reset_index()

    mean_monthly_rain = rain_df.groupby(["year", "month"])["rain"].mean().reset_index()
    mean_monthly_rain = order_months(mean_monthly_rain)

    mean_yearly_rain = rain_df.groupby(["year"])["rain"].mean().reset_index()

    # Mostra le medie mensili
    st.subheader("Monthly means")
    mean_monthly_fig = plot_monthly_rain(
        mean_monthly_rain,
        range(selected_years[0], selected_years[1] + 1),
        "Rain Monthly Means",
    )
    st.pyplot(mean_monthly_fig)

    # Crea il buffer per il grafico mensile e aggiungi il pulsante di download
    mean_monthly_buf = create_download_link(mean_monthly_fig)
    st.download_button(
        label="Download monthly means graph",
        data=mean_monthly_buf,
        file_name="monthly_means.png",
        mime="image/png",
    )

    # Mostra gli accumuli mensili
    st.subheader("Monthly accumulations")
    monthly_fig = plot_monthly_rain(
        montly_accumulations,
        range(selected_years[0], selected_years[1] + 1),
        "Rain Monthly Accumulations",
    )
    st.pyplot(monthly_fig)

    # Crea il buffer per il grafico mensile e aggiungi il pulsante di download
    mensili_buf = create_download_link(monthly_fig)
    st.download_button(
        label="Download monthly accumulations graph",
        data=mensili_buf,
        file_name="monthly_accumulations.png",
        mime="image/png",
    )

    # Mostra le medie annuali
    st.subheader("Annual Means")
    mean_annual_fig = plot_annual_rain(
        mean_yearly_rain,
        range(selected_years[0], selected_years[1] + 1),
        "Rain Annual Means",
    )
    st.pyplot(mean_annual_fig)

    mean_annual_buf = create_download_link(mean_annual_fig)
    st.download_button(
        label="Download annual means graph",
        data=mean_annual_buf,
        file_name="annual_means.png",
        mime="image/png",
    )

    # Mostra gli accumuli annuali
    st.subheader("Annual Accumulations")
    annual_fig = plot_annual_rain(
        annual_accumulations,
        range(selected_years[0], selected_years[1] + 1),
        "Rain Annual Accumulations",
    )
    st.pyplot(annual_fig)

    # Crea il buffer per il grafico annuale e aggiungi il pulsante di download
    annual_buf = create_download_link(annual_fig)
    st.download_button(
        label="Download annual accumulations graph",
        data=annual_buf,
        file_name="annual_accumulations.png",
        mime="image/png",
    )
