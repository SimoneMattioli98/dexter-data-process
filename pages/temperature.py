import emoji
import pandas as pd
import streamlit as st

from utils import (
    clean_up_temperature_csv,
    get_frosts,
    get_top_ten,
    spring_autumn_critical_temperature,
)

# Definisci le traduzioni disponibili
translations = {
    'en': {
        'about_app': "About this app",
        'about_app_content': "Load Markdown content from file",
        'select_min_temp_file': "Select a csv file with minimum temperatures...",
        'select_max_temp_file': "Select a csv file with maximum temperatures...",
        'select_years_display': "Select years to display",
        'soft_frost': "Soft frost",
        'hard_frost': "Hard frost",
        'temp_spring_autumn': "15° temperature in spring/autumn",
        'top_10_coldest': "Top 10 coldest temperatures per year",
        'top_10_hottest': "Top 10 hottest temperatures per year"
    },
    'it': {
        'about_app': "Informazioni sull'applicazione",
        'about_app_content': "Carica contenuto Markdown da file",
        'select_min_temp_file': "Seleziona un file CSV con le temperature minime...",
        'select_max_temp_file': "Seleziona un file CSV con le temperature massime...",
        'select_years_display': "Seleziona gli anni da visualizzare",
        'soft_frost': "Gelata leggera",
        'hard_frost': "Gelata forte",
        'temp_spring_autumn': "Temperatura 15° in primavera/autunno",
        'top_10_coldest': "Top 10 temperature più fredde per anno",
        'top_10_hottest': "Top 10 temperature più calde per anno"
    }
}


# Funzione per tradurre una stringa
def translate(key, lang):
    return translations[lang].get(key, key)


# Funzione principale dell'applicazione
def main():
    thermometer_emoji = emoji.emojize(":thermometer:")
    st.set_page_config(layout="wide", page_title="Temperature", page_icon=thermometer_emoji)
    st.title(thermometer_emoji + " Temperature")

    # Selettore di lingua
    selected_language = st.sidebar.selectbox('Language / Lingua', ('English', 'Italiano'))
    language_code = 'en' if selected_language == 'English' else 'it'

    st.session_state.language = language_code


    with st.expander(translate('about_app', st.session_state.language)):
        # Carica il contenuto Markdown dal file
        with open(f"markdown/{st.session_state.language}/about_temperature.md") as file:
            markdown_about_app = file.read()
            st.markdown(markdown_about_app)

    st.subheader(translate('select_min_temp_file', st.session_state.language))
    min_temp_file = st.file_uploader(translate('select_min_temp_file', st.session_state.language), key=1)

    if min_temp_file is not None:
        min_df, min_nan_temperature = clean_up_temperature_csv(min_temp_file)

        min_df["year"] = pd.to_datetime(min_df["date"], format="%d/%m/%Y").dt.year

        min_available_years = sorted(min_df["year"].unique())

        min_selected_years = st.slider(
            translate('select_years_display', st.session_state.language),
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

        soft_frost, hard_frost = get_frosts(min_df)
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
            st.subheader(translate('soft_frost', st.session_state.language))
            st.dataframe(soft_frost)

        with col2:
            st.subheader(translate('hard_frost', st.session_state.language))
            st.dataframe(hard_frost)

        with col3:
            st.subheader(translate('temp_spring_autumn', st.session_state.language))
            st.dataframe(first_15_temps_df)

        st.divider()
        st.subheader(translate('top_10_coldest', st.session_state.language))
        st.dataframe(min_df_empty, hide_index=True)

    st.subheader(translate('select_max_temp_file', st.session_state.language))
    max_temp_file = st.file_uploader(translate('select_max_temp_file', st.session_state.language), key=2)

    if max_temp_file is not None:
        max_df, max_nan_temperature = clean_up_temperature_csv(max_temp_file)

        max_df["year"] = pd.to_datetime(max_df["date"], format="%d/%m/%Y").dt.year

        max_available_years = sorted(max_df["year"].unique())

        max_selected_years = st.slider(
            translate('select_years_display', st.session_state.language),
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

        st.subheader(translate('top_10_hottest', st.session_state.language))
        st.dataframe(max_df_empty, hide_index=True)

if __name__ == "__main__":
    st.session_state.language = 'en'
    main()
