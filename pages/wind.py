import streamlit as st
import emoji

wind_emoji = emoji.emojize(':wind_face:')
st.set_page_config(page_title="Wind", page_icon=wind_emoji)
st.title(wind_emoji + " Wind")

st.subheader("Select a csv file with wind data...")
wind_file = st.file_uploader("Choose a file", key=1)
