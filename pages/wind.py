import emoji
import pandas as pd
import streamlit as st

from utils import (
    build_wind_graph,
    clean_up_wind_csv,
    get_top_ten,
    order_cardinal_points,
)

# Definisci le traduzioni disponibili
translations = {
    'en': {
        'about_app': "About this app",
        'select_speed_file': "Select a csv file with wind SPEED data...",
        'select_direction_file': "Select a csv file with wind DIRECTION data...",
        'select_years_display': "Select years to display",
        'windy_days_table': "Number of windy days divided by direction and speed in m/s",
        'most_popular_speed': "Most popular wind speed",
        'most_popular_direction': "Most popular wind direction",
        'top_ten_strength': "Top ten wind strength",
        'percentage_graph': "Wind percentage graph"
    },
    'it': {
        'about_app': "Informazioni sull'applicazione",
        'select_speed_file': "Seleziona un file CSV con i dati di VELOCITÀ del vento...",
        'select_direction_file': "Seleziona un file CSV con i dati di DIREZIONE del vento...",
        'select_years_display': "Seleziona gli anni da visualizzare",
        'windy_days_table': "Numero di giorni ventosi divisi per direzione e velocità in m/s",
        'most_popular_speed': "Velocità del vento più popolare",
        'most_popular_direction': "Direzione del vento più popolare",
        'top_ten_strength': "Top dieci forza del vento",
        'percentage_graph': "Grafico percentuale del vento"
    }
}

# Funzione per tradurre una stringa
def translate(key, lang):
    return translations[lang].get(key, key)

# Funzione principale dell'applicazione
def main():
    wind_emoji = emoji.emojize(":wind_face:")
    st.set_page_config(layout="wide", page_title="Wind", page_icon=wind_emoji)
    st.title(wind_emoji + " Wind")

    # Selettore di lingua
    selected_language = st.sidebar.selectbox('Language / Lingua', ('English', 'Italiano'))
    language_code = 'en' if selected_language == 'English' else 'it'

    st.session_state.language=language_code

    with st.expander(translate('about_app', st.session_state.language)):
        # Carica il contenuto Markdown dal file
        with open(f"markdown/{st.session_state.language}/about_wind.md") as file:
            markdown_about_app = file.read()
            st.markdown(markdown_about_app)

    st.subheader(translate('select_speed_file', st.session_state.language))
    wind_speed_file = st.file_uploader(translate('select_speed_file', st.session_state.language), key=1)
    st.subheader(translate('select_direction_file', st.session_state.language))
    wind_direction_file = st.file_uploader(translate('select_direction_file', st.session_state.language), key=2)

    if wind_direction_file is not None and wind_speed_file is not None:
        wind_df, nan_wind_info = clean_up_wind_csv(wind_speed_file, wind_direction_file)

        wind_df["year"] = pd.to_datetime(wind_df["date"], format="%d/%m/%Y").dt.year

        available_years = sorted(wind_df["year"].unique())

        selected_years = st.slider(
            translate('select_years_display', st.session_state.language),
            min_value=min(available_years),
            max_value=max(available_years),
            value=(min(available_years), max(available_years)),
        )

        wind_df = wind_df[
            wind_df["year"].isin(range(selected_years[0], selected_years[1] + 1))
        ]

        del wind_df["year"]

        st.subheader(translate('windy_days_table', st.session_state.language))
        beaufort_table = pd.crosstab(wind_df["direction"], wind_df["beaufort"])

        sums_speed = beaufort_table.sum().rename("Total_speed")
        sums_direction = beaufort_table.sum(axis=1).rename("Total_direction")

        def highlight_max(s):
            is_max = s == s.max()
            return ["background-color: yellow" if v else "" for v in is_max]

        beaufort_table = beaufort_table.style.apply(highlight_max, axis=0)

        st.dataframe(beaufort_table)
        sums_speed_df = pd.DataFrame(sums_speed)
        sums_speed_df = sums_speed_df.reset_index()

        sums_direction_df = pd.DataFrame(sums_direction)
        sums_direction_df = sums_direction_df.reset_index()

        sums_direction_df = order_cardinal_points(sums_direction_df)
        total = sums_direction_df["Total_direction"].sum()
        sums_direction_df["percentage"] = (
            sums_direction_df["Total_direction"] / total
        ) * 100

        graph = build_wind_graph(sums_direction_df)

        del sums_direction_df["percentage"]

        col1, col2, col3 = st.columns(3)

        sums_speed_df.set_index("beaufort", inplace=True)

        sums_speed_df = sums_speed_df.style.apply(
            highlight_max, axis=0, subset=["Total_speed"]
        )
        sums_direction_df = sums_direction_df.style.apply(
            highlight_max, axis=0, subset=["Total_direction"]
        )

        with col1:
            st.subheader(translate('most_popular_speed', st.session_state.language))
            st.dataframe(sums_speed_df)

        with col2:
            st.subheader(translate('most_popular_direction', st.session_state.language))
            st.dataframe(sums_direction_df)

        with col3:
            st.subheader(translate('top_ten_strength', st.session_state.language))
            column_names = ["date", "speed"]

            df_no_columns = get_top_ten(
                wind_df.loc[:, ["date", "speed"]], "speed", ascending=False
            ).values

            df_no_columns_with_names = pd.DataFrame(df_no_columns, columns=column_names)

            st.dataframe(df_no_columns_with_names)

        st.subheader(translate('percentage_graph', st.session_state.language))
        st.plotly_chart(graph)

if __name__ == "__main__":
    st.session_state.language = 'en'
    main()
