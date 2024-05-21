import pandas as pd


def clean_up_csv(file):
    df = pd.read_csv(file)  # Load data
    df = df.drop(["date_end"], axis=1)
    df.rename(columns={"date_start": "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["date"] = pd.to_datetime(df["date"])
    df["temperature"] = df["temperature"].round().astype("Int32")
    nan_temperature: int = df["temperature"].isna().sum()
    return df.groupby(pd.PeriodIndex(df["date"], freq="Y")), nan_temperature


def get_top_ten(df, ascending=True):
    df_sorted = df.sort_values(by="temperature", ascending=ascending)
    top_ten = df_sorted.iloc[:10]
    year = top_ten["date"].iloc[0].year
    top_ten["date"] = top_ten["date"].dt.strftime("%m-%d")
    top_ten["temperature"] = top_ten["temperature"].astype("str")
    top_ten.columns = pd.MultiIndex.from_product([[str(year)], top_ten.columns])
    top_ten = top_ten.reset_index(drop=True)
    return top_ten


def get_cold_dates(df):
    first_soft_negative_index = df.temperature.lt(0).idxmax()
    first_soft_negative = df.loc[first_soft_negative_index]

    first_hard_negative_index = df.temperature.lt(-2).idxmax()
    first_hard_negative = df.loc[first_hard_negative_index]

    df_reverse = df.iloc[::-1]

    last_soft_negative_index = df_reverse.temperature.lt(0).idxmax()
    last_soft_negative = df_reverse.loc[last_soft_negative_index]

    last_hard_negative_index = df_reverse.temperature.lt(-2).idxmax()
    last_hard_negative = df_reverse.loc[last_hard_negative_index]

    return (
        first_soft_negative,
        last_soft_negative,
        first_hard_negative,
        last_hard_negative,
    )
