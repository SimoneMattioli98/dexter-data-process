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

# Definisci le traduzioni disponibili
translations = {
    'en': {
        'page_title': "Rain",
        'about_app': "About this app",
        'select_csv': "Select a csv file with rain data...",
        'monthly_means': "Monthly means",
        'monthly_accumulations': "Monthly accumulations",
        'annual_means': "Annual means",
        'annual_accumulations': "Annual accumulations",
        'download_monthly_means': "Download monthly means graph",
        'download_monthly_accumulations': "Download monthly accumulations graph",
        'download_annual_means': "Download annual means graph",
        'download_annual_accumulations': "Download annual accumulations graph"
    },
    'it': {
        'page_title': "Pioggia",
        'about_app': "Informazioni sull'applicazione",
        'select_csv': "Seleziona un file csv con i dati sulla pioggia...",
        'monthly_means': "Medie mensili",
        'monthly_accumulations': "Accumuli mensili",
        'annual_means': "Medie annuali",
        'annual_accumulations': "Accumuli annuali",
        'download_monthly_means': "Scarica il grafico delle medie mensili",
        'download_monthly_accumulations': "Scarica il grafico degli accumuli mensili",
        'download_annual_means': "Scarica il grafico delle medie annuali",
        'download_annual_accumulations': "Scarica il grafico degli accumuli annuali"
    }
}

# Funzione per tradurre una stringa
def translate(key, lang):
    return translations[lang].get(key, key)

# Funzione principale dell'applicazione
def main():
    rain_emoji = emoji.emojize(":cloud_with_rain:")
    st.set_page_config(layout="wide", page_title="Rain", page_icon=rain_emoji)
    selected_language = st.sidebar.selectbox('Language / Lingua', ('English', 'Italiano'))
    language_code = 'en' if selected_language == 'English' else 'it'

    st.session_state.language = language_code
    st.title(rain_emoji + " " + translate('page_title', language_code))

    with st.expander(translate('about_app', language_code)):
        # Load Markdown content from file
        with open(f"markdown/{st.session_state.language}/about_rain.md") as file:
            markdown_about_app = file.read()
            st.markdown(markdown_about_app)

    st.subheader(translate('select_csv', language_code))
    rain_file = st.file_uploader(translate('select_csv', language_code), key=1)

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
            translate('select_years_display', language_code),
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
        st.subheader(translate('monthly_means', language_code))
        mean_monthly_fig = plot_monthly_rain(
            mean_monthly_rain,
            range(selected_years[0], selected_years[1] + 1),
            translate('monthly_means', language_code),
        )
        st.pyplot(mean_monthly_fig)

        # Crea il buffer per il grafico mensile e aggiungi il pulsante di download
        mean_monthly_buf = create_download_link(mean_monthly_fig)
        st.download_button(
            label=translate('download_monthly_means', language_code),
            data=mean_monthly_buf,
            file_name="monthly_means.png",
            mime="image/png",
        )

        st.subheader(translate('monthly_accumulations', language_code))
        monthly_fig = plot_monthly_rain(
            montly_accumulations,
            range(selected_years[0], selected_years[1] + 1),
            translate('monthly_accumulations', language_code),
        )
        st.pyplot(monthly_fig)

        mensili_buf = create_download_link(monthly_fig)
        st.download_button(
            label=translate('download_monthly_accumulations', language_code),
            data=mensili_buf,
            file_name="monthly_accumulations.png",
            mime="image/png",
        )

        st.subheader(translate('annual_means', language_code))
        mean_annual_fig = plot_annual_rain(
            mean_yearly_rain,
            range(selected_years[0], selected_years[1] + 1),
            translate('annual_means', language_code),
        )
        st.pyplot(mean_annual_fig)

        mean_annual_buf = create_download_link(mean_annual_fig)
        st.download_button(
            label=translate('download_annual_means', language_code),
            data=mean_annual_buf,
            file_name="annual_means.png",
            mime="image/png",
        )

        st.subheader(translate('annual_accumulations', language_code))
        annual_fig = plot_annual_rain(
            annual_accumulations,
            range(selected_years[0], selected_years[1] + 1),
            translate('annual_accumulations', language_code),
        )
        st.pyplot(annual_fig)

        annual_buf = create_download_link(annual_fig)
        st.download_button(
            label=translate('download_annual_accumulations', language_code),
            data=annual_buf,
            file_name="annual_accumulations.png",
            mime="image/png",
        )

# Esegui l'applicazione
if __name__ == '__main__':
    # Imposta la lingua predefinita
    st.session_state.language = 'en'
    main()
