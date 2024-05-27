import emoji
import pandas as pd
import streamlit as st

from utils import clean_up_wind_csv, order_cardinal_points, build_wind_graph, get_top_ten

wind_emoji = emoji.emojize(":wind_face:")
st.set_page_config(layout="wide", page_title="Wind", page_icon=wind_emoji)
st.title(wind_emoji + " Wind")

st.subheader("Select a csv file with wind SPEED data...")
wind_speed_file = st.file_uploader("Choose a file", key=1)
st.subheader("Select a csv file with wind DIRECTION data...")
wind_direction_file = st.file_uploader("Choose a file", key=2)


if wind_direction_file is not None and wind_speed_file is not None:
    wind_df, nan_wind_info = clean_up_wind_csv(wind_speed_file, wind_direction_file)

    st.text("NUMBER OF WINDY DAYS DIVIDED BY DIRECTION AND SPEED IN M/S")
    beaufort_table = pd.crosstab(wind_df['direction'], wind_df['beaufort'])

    sums_speed = beaufort_table.sum().rename('Total_speed')
    sums_direction = beaufort_table.sum(axis=1).rename('Total_direction')


    def highlight_max(s):
        is_max = s == s.max()
        return ['background-color: yellow' if v else '' for v in is_max]

    beaufort_table = beaufort_table.style.apply(highlight_max, axis=0)

    st.dataframe(beaufort_table)
    sums_speed_df = pd.DataFrame(sums_speed)
    sums_speed_df = sums_speed_df.reset_index()

    sums_direction_df = pd.DataFrame(sums_direction)
    sums_direction_df = sums_direction_df.reset_index()

    sums_direction_df = order_cardinal_points(sums_direction_df)
    total = sums_direction_df['Total_direction'].sum()
    sums_direction_df['percentage'] = (sums_direction_df['Total_direction'] / total) * 100

    graph = build_wind_graph(sums_direction_df)

    del sums_direction_df["percentage"]

    col1, col2, col3 = st.columns(3)

    sums_speed_df.set_index('beaufort', inplace=True)

    sums_speed_df = sums_speed_df.style.apply(highlight_max, axis=0, subset=["Total_speed"])
    sums_direction_df = sums_direction_df.style.apply(highlight_max, axis=0, subset=["Total_direction"])

    with col1:
        st.text("Most popular wind speed")
        st.dataframe(sums_speed_df)

    with col2:
        st.text("Most popular wind direction")
        st.dataframe(sums_direction_df)

    with col3:
        st.text("Top ten wind strength")
        column_names = ['date', 'speed']

        df_no_columns = get_top_ten(wind_df.loc[:, ["date", "speed"]],
                                    "speed", ascending=False).values

        df_no_columns_with_names = pd.DataFrame(df_no_columns, columns=column_names)

        st.dataframe(df_no_columns_with_names)

    st.text('Wind percentage')
    st.plotly_chart(graph)






