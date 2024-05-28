import streamlit as st

# Definisci le traduzioni disponibili
translations = {
    'en': {
        'page_title': "Dexter data processing",
        'about_app': "About this app",
        'about_app_content': "Load Markdown content from file",
        'app_usage': "App Usage",
        'temperature_btn': "Temperature",
        'wind_btn': "Wind",
        'rain_btn': "Rain"
    },
    'it': {
        'page_title': "Elaborazione dati di Dexter",
        'about_app': "Informazioni sull'applicazione",
        'about_app_content': "Carica contenuto Markdown da file",
        'app_usage': "Utilizzo dell'applicazione",
        'temperature_btn': "Temperatura",
        'wind_btn': "Vento",
        'rain_btn': "Pioggia"
    }
}

def translate(key, lang):
    return translations[lang].get(key, key)

# Funzione principale dell'applicazione
def main():
    st.set_page_config(page_title=translate('page_title', st.session_state.language), page_icon="📊")
    st.sidebar.header('Language / Lingua')
    # Aggiungi un selettore di lingua nella barra laterale
    selected_language = st.sidebar.selectbox('', ('English', 'Italiano'))

    # Mappa la selezione dell'utente al codice della lingua
    language_code = 'en' if selected_language == 'English' else 'it'

    # Imposta la lingua corrente
    st.session_state.language = language_code
    st.title("📊 " + translate('page_title', st.session_state.language))

    with st.expander(translate('about_app', st.session_state.language)):
        # Load Markdown content from file
        with open(f"markdown/{st.session_state.language}/about_app.md") as file:
            markdown_about_app = file.read()
            st.markdown(markdown_about_app)

        with open(f"markdown/{st.session_state.language}/app_usage.md") as file:
            markdown_app_usage = file.read()
            st.markdown(markdown_app_usage)

    if st.button(translate('temperature_btn', st.session_state.language)):
        st.switch_page("pages/temperature.py")

    if st.button(translate('wind_btn', st.session_state.language)):
        st.switch_page("pages/wind.py")

    if st.button(translate('rain_btn', st.session_state.language)):
        st.switch_page("pages/rain.py")


# Esegui l'applicazione
if __name__ == '__main__':
    # Imposta la lingua predefinita
    st.session_state.language = 'en'
    main()