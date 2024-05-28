import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns


def clean_up_temperature_csv(file):
    df = pd.read_csv(file)
    df = df.drop(columns=["date_end"]).rename(columns={"date_start": "date"})

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d/%m/%Y")

    nan_temperature = df["temperature"].isna().sum()

    df = df.dropna(subset=["temperature"])

    df["temperature"] = np.round(df["temperature"], 1)

    return df, nan_temperature


def clean_up_rain_csv(file):
    df = pd.read_csv(file)
    df = df.drop(columns=["date_end"]).rename(columns={"date_start": "date"})

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d/%m/%Y")

    nan_temperature = df["rain"].isna().sum()

    df = df.dropna(subset=["rain"])

    return df, nan_temperature


def create_download_link(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf


# Funzione per aggiungere annotazioni sulle barre con rotazione
def add_annotations(ax, rotation, offset):
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.1f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="bottom",
            rotation=rotation,
            xytext=(0, offset),
            textcoords="offset points",
            fontsize=10,
            color="black",
            weight="bold",
        )


def plot_monthly_rain(accumuli_mensili, selected_years, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    accumuli_mensili_selected = accumuli_mensili[
        accumuli_mensili["year"].isin(selected_years)
    ]
    accumuli_mensili_pivot = accumuli_mensili_selected.pivot(
        index="month", columns="year", values="rain"
    )
    accumuli_mensili_pivot.plot(kind="bar", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Rain (mm)")
    ax.set_title(title, fontsize=16, y=1.10)
    ax.legend(title="Year")
    sns.despine()
    add_annotations(ax, rotation=90, offset=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=12)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
    return fig


def plot_annual_rain(accumuli_annuali, selected_years, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    accumuli_annuali_selected = accumuli_annuali[
        accumuli_annuali["year"].isin(selected_years)
    ]
    sns.barplot(
        x="year", y="rain", data=accumuli_annuali_selected, ax=ax, palette="viridis"
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Rain (mm)")
    ax.set_title(title, fontsize=16, y=1.10)
    sns.despine()
    add_annotations(ax, rotation=90, offset=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=12)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
    return fig


def order_months(df):
    # Ordina i dati per numero del mese
    df["month"] = pd.Categorical(
        df["month"],
        categories=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        ordered=True,
    )
    return df.sort_values(by=["month"])

def build_wind_graph(sums_direction_df):
    graph = go.Figure()

    colors = [
        "rgba(255, 0, 0, 0.7)",
        "rgba(0, 255, 0, 0.7)",
        "rgba(0, 0, 255, 0.7)",
        "rgba(255, 255, 0, 0.7)",
        "rgba(255, 165, 0, 0.7)",
        "rgba(128, 0, 128, 0.7)",
        "rgba(0, 255, 255, 0.7)",
        "rgba(255, 192, 203, 0.7)",
    ]

    graph.add_trace(
        go.Barpolar(
            r=sums_direction_df["percentage"],
            theta=sums_direction_df["direction"],
            marker_color=colors,
        )
    )

    graph.update_layout(
        template="plotly_white",
        polar=dict(
            radialaxis=dict(
                ticks="",
                showticklabels=True,
                tickfont=dict(
                    size=15,  # Adjust the font size of the tick labels
                    color="black",  # Adjust the color of the tick labels
                ),
                gridcolor="rgba(0, 0, 0, 0.5)",  # Darker grid color
                linewidth=2,
                linecolor="black",
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=15,  # Adjust the font size of the cardinal directions
                    color="black",  # Adjust the color of the cardinal directions
                ),
                linecolor="black",  # Set line color for angular axis
                linewidth=2,
            ),
        ),
        width=800,  # Adjust the width of the plot
        height=800,
    )
    return graph


def clean_up_wind_csv(wind_speed_file, wind_direction_file):
    wind_speed_df = pd.read_csv(wind_speed_file)
    wind_direction_df = pd.read_csv(wind_direction_file)
    del wind_speed_df["date_end"]
    del wind_direction_df["date_end"]
    wind_speed_df.rename(columns={"date_start": "date"}, inplace=True)
    wind_direction_df.rename(columns={"date_start": "date"}, inplace=True)
    wind_speed_df["date"] = pd.to_datetime(wind_speed_df["date"]).dt.date
    wind_direction_df["date"] = pd.to_datetime(wind_direction_df["date"]).dt.date
    merged_df = pd.merge(wind_speed_df, wind_direction_df, on="date")
    nan_wind_info: int = merged_df.isna().sum()
    merged_df.dropna()
    merged_df["direction"] = merged_df["direction"].apply(wind_rose)
    merged_df["beaufort"] = merged_df["speed"].apply(beaufort_value)

    return merged_df, nan_wind_info


def wind_rose(degree):
    if (degree >= 0 and degree < 22.5) or (degree >= 337.5 and degree <= 359):
        return "N"
    elif degree >= 22.5 and degree < 67.5:
        return "NE"
    elif degree >= 67.5 and degree < 112.5:
        return "E"
    elif degree >= 112.5 and degree < 157.5:
        return "SE"
    elif degree >= 157.5 and degree < 202.5:
        return "S"
    elif degree >= 202.5 and degree < 247.5:
        return "SW"
    elif degree >= 247.5 and degree < 292.5:
        return "W"
    elif degree >= 292.5 and degree < 337.5:
        return "NW"


def order_cardinal_points(df):
    ordered_cardinals = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
    df["direction"] = pd.Categorical(
        df["direction"], categories=ordered_cardinals, ordered=True
    )
    return df.sort_values("direction")


def beaufort_value(speed_meter_per_second):
    if speed_meter_per_second >= 0 and speed_meter_per_second <= 1.5:
        return 1
    elif speed_meter_per_second >= 1.6 and speed_meter_per_second <= 3.4:
        return 2
    elif speed_meter_per_second >= 3.5 and speed_meter_per_second <= 5.4:
        return 3
    elif speed_meter_per_second >= 5.5 and speed_meter_per_second <= 7.9:
        return 4
    elif speed_meter_per_second >= 8 and speed_meter_per_second <= 10.7:
        return 5
    elif speed_meter_per_second >= 10.8 and speed_meter_per_second <= 13.8:
        return 6
    elif speed_meter_per_second >= 13.9 and speed_meter_per_second <= 17.1:
        return 7
    elif speed_meter_per_second >= 17.2 and speed_meter_per_second <= 20.7:
        return 8
    elif speed_meter_per_second >= 20.8 and speed_meter_per_second <= 24.4:
        return 9
    elif speed_meter_per_second >= 24.5 and speed_meter_per_second <= 28.4:
        return 10


def rename_index(val):
    return f"{val}-{val+1}"


def get_current_year(date):
    return date.year


def get_frosts(df):
    # Converti la colonna 'date' in Timestamp solo una volta
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df["year_index"] = df["date"].apply(get_current_year)

    # Crea maschere per soft frost e hard frost
    soft_frost_mask = (df["temperature"] >= -2) & (df["temperature"] < 0)
    hard_frost_mask = df["temperature"] < -2

    soft_frost = df[soft_frost_mask].groupby("year_index")["date"].agg(["min", "max"])
    soft_frost.columns = ["first_soft_frost", "last_soft_frost"]
    soft_frost["first_soft_frost"] = soft_frost["first_soft_frost"].dt.strftime("%d/%m/%Y")
    soft_frost["last_soft_frost"] = soft_frost["last_soft_frost"].dt.strftime("%d/%m/%Y")

    hard_frost = df[hard_frost_mask].groupby("year_index")["date"].agg(["min", "max"])
    hard_frost.columns = ["first_hard_frost", "last_hard_frost"]
    hard_frost["first_hard_frost"] = hard_frost["first_hard_frost"].dt.strftime("%d/%m/%Y")
    hard_frost["last_hard_frost"] = hard_frost["last_hard_frost"].dt.strftime("%d/%m/%Y")

    # Rinomina gli indici
    soft_frost = soft_frost.rename(index=rename_index)
    hard_frost = hard_frost.rename(index=rename_index)

    return soft_frost, hard_frost


def get_top_ten(df, key, ascending=True):
    top_ten = df.sort_values(by=key, ascending=ascending).head(10)

    # Ottieni l'anno dalla prima data
    year = pd.to_datetime(top_ten["date"], format="%d/%m/%Y").iloc[0].year

    # Converti le date nel formato italiano 'gg/mm'
    top_ten["date"] = pd.to_datetime(top_ten["date"], format="%d/%m/%Y").dt.strftime(
        "%d/%m/%Y"
    )

    # Converti il valore chiave in stringa, se necessario
    top_ten[key] = top_ten[key].astype(str)

    # Assegna il MultiIndex alle colonne
    top_ten.columns = pd.MultiIndex.from_product([[str(year)], top_ten.columns])

    # Reset dell'indice
    top_ten = top_ten.reset_index(drop=True)

    return top_ten


def spring_autumn_critical_temperature(first_15_temps_df, year, df):
    df["month_day"] = pd.to_datetime(df["date"], format="%d/%m/%Y").dt.strftime(
        "%d/%m/%Y"
    )

    # Definisci i periodi di primavera e autunno
    spring_start = "01/01"
    spring_end = "30/06"
    autumn_start = "01/07"
    autumn_end = "31/12"

    # Filtra una sola volta per primavera e autunno
    spring_df = df[(df["month_day"] >= spring_start) & (df["month_day"] <= spring_end)]
    autumn_df = df[(df["month_day"] >= autumn_start) & (df["month_day"] <= autumn_end)]

    # Trova la prima temperatura che raggiunge 15°C in primavera
    first_spring_temp_15 = spring_df[spring_df["temperature"] >= 15].head(1)

    # Trova la prima temperatura che scende sotto 15°C in autunno
    first_autumn_temp_below_15 = autumn_df[autumn_df["temperature"] < 15].head(1)

    # Aggiorna il DataFrame first_15_temps_df
    first_15_temps_df.loc[year, "Spring Date 15"] = (
        (first_spring_temp_15["date"].iloc)[0]
        if not first_spring_temp_15.empty
        else None
    )
    first_15_temps_df.loc[year, "Autumn Date <15"] = (
        (first_autumn_temp_below_15["date"].iloc)[0]
        if not first_autumn_temp_below_15.empty
        else None
    )

    return first_spring_temp_15, first_autumn_temp_below_15
