import streamlit as st

# Page title
st.set_page_config(page_title="Dexter data processing", page_icon="📊")
st.title("📊 Dexter data processing")

with st.expander("About this app"):
    # Load Markdown content from file
    with open("markdown/about_app.md") as file:
        markdown_about_app = file.read()
        st.markdown(markdown_about_app)
    with open("markdown/app_usage.md") as file:
        markdown_app_usage = file.read()
        st.markdown(markdown_app_usage)

if st.button("Temperature"):
    st.switch_page("pages/temperature.py")

if st.button("Wind"):
    st.switch_page("pages/wind.py")


if st.button("Rain"):
    st.switch_page("pages/rain.py")
