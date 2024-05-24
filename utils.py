import numpy as np
import pandas as pd


def clean_up_csv(file):
    df = pd.read_csv(file)  # Load data
    del df["date_end"]
    df.rename(columns={"date_start": "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    nan_temperature: int = df["temperature"].isna().sum()
    df.dropna()
    df.loc[:, "temperature"] = np.round(df["temperature"].values, 1)
    return df, df.groupby(pd.PeriodIndex(df["date"], freq="Y")), nan_temperature


def rename_index(val):
    return f"{val}-{val+1}"


def get_colds(df):
    df["date"] = df["date"].apply(pd.Timestamp)
    df["year_index"] = df["date"].apply(get_current_year)

    soft_cold = np.logical_and(df["temperature"] >= -2, df["temperature"] < 0)
    hard_cold = df["temperature"] < -2

    soft_groupby = df[soft_cold].groupby("year_index")["date"]
    first_soft_cold = soft_groupby.min()
    first_soft_cold = first_soft_cold.to_frame(name="first_soft_cold")
    first_soft_cold["first_soft_cold"] = pd.to_datetime(
        first_soft_cold["first_soft_cold"]
    ).dt.date
    last_soft_cold = soft_groupby.max()
    last_soft_cold = last_soft_cold.to_frame(name="last_soft_cold")
    last_soft_cold["last_soft_cold"] = pd.to_datetime(
        last_soft_cold["last_soft_cold"]
    ).dt.date
    soft_cold = pd.merge(first_soft_cold, last_soft_cold, on="year_index")
    hard_groupby = df[hard_cold].groupby("year_index")["date"]
    first_hard_cold = hard_groupby.min()
    first_hard_cold = first_hard_cold.to_frame(name="first_hard_cold")
    first_hard_cold["first_hard_cold"] = pd.to_datetime(
        first_hard_cold["first_hard_cold"]
    ).dt.date
    last_hard_cold = hard_groupby.max()
    last_hard_cold = last_hard_cold.to_frame(name="last_hard_cold")
    last_hard_cold["last_hard_cold"] = pd.to_datetime(
        last_hard_cold["last_hard_cold"]
    ).dt.date
    hard_cold = pd.merge(first_hard_cold, last_hard_cold, on="year_index")

    soft_cold = soft_cold.rename(index=rename_index)
    hard_cold = hard_cold.rename(index=rename_index)

    return soft_cold, hard_cold


def get_current_year(date):
    year = date.year
    start_date = pd.Timestamp(year=year, month=6, day=15)
    if date >= start_date:
        return year
    else:
        return year - 1


def get_top_ten(df, ascending=True):
    df_sorted = df.sort_values(by="temperature", ascending=ascending)
    top_ten = df_sorted.iloc[:10]
    year = top_ten["date"].iloc[0].year
    top_ten.loc[:, "date"] = (
        pd.to_datetime(top_ten["date"]).dt.strftime("%m-%d").astype(str)
    )
    top_ten["temperature"] = top_ten["temperature"].astype("str")
    top_ten.columns = pd.MultiIndex.from_product([[str(year)], top_ten.columns])
    top_ten = top_ten.reset_index(drop=True)
    return top_ten


def spring_autumn_critical_temperature(df):
    # Define the spring and autumn periods
    spring_start = "01-01"
    spring_end = "06-30"
    autumn_start = "07-01"
    autumn_end = "12-31"

    spring_df = df[
        (df["date"].dt.strftime("%m-%d") >= spring_start)
        & (df["date"].dt.strftime("%m-%d") <= spring_end)
    ]
    autumn_df = df[
        (df["date"].dt.strftime("%m-%d") >= autumn_start)
        & (df["date"].dt.strftime("%m-%d") <= autumn_end)
    ]

    # Find the first temperature reaching 15°C in spring for the current year
    first_spring_temp_15 = spring_df[spring_df["temperature"] >= 15].head(1)

    # Find the first temperature falling below 15°C in autumn for the current year
    first_autumn_temp_below_15 = autumn_df[autumn_df["temperature"] < 15].head(1)

    return first_spring_temp_15, first_autumn_temp_below_15
