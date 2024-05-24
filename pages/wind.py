import emoji
import streamlit as st

from utils import clean_up_wind_csv

wind_emoji = emoji.emojize(":wind_face:")
st.set_page_config(page_title="Wind", page_icon=wind_emoji)
st.title(wind_emoji + " Wind")

st.subheader("Select a csv file with wind SPEED data...")
wind_speed_file = st.file_uploader("Choose a file", key=1)
st.subheader("Select a csv file with wind DIRECTION data...")
wind_direction_file = st.file_uploader("Choose a file", key=1)


if wind_direction_file is not None and wind_speed_file is not None:
    wind_df, nan_wind_info = clean_up_wind_csv(wind_speed_file, wind_direction_file)
