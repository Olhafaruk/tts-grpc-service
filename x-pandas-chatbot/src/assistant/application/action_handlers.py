#src/assistant/application/action_handlers.py
import pandas as pd

def merge_tables(df1: pd.DataFrame, df2: pd.DataFrame, on: list[str], how: str = "inner") -> pd.DataFrame:
    return df1.merge(df2, on=on, how=how)


def convert_currency(df, currency: str, amount: float, date: str) -> dict:
    row = df[(df["Currency"] == currency) & (df["Date"] == date)]
    if row.empty:
        return {"text": f"No rate found for {currency} on {date}"}
    rate = row.iloc[0]["Rate to USD"]
    converted = round(amount * rate, 2)
    return {
        "converted_amount": converted,
        "rate": rate,
        "currency": currency,
        "date": date,
        "original_amount": amount,
        "text": f"{amount} {currency} on {date} = {converted} USD (rate: {rate})"
    }

def aggregate_column(df, column: str, agg: str = "mean", group_by: str = None) -> dict:
    if group_by:
        grouped = df.groupby(group_by)[column].agg(agg).reset_index()
        return {"aggregated": grouped.to_dict(orient="records")}
    else:
        value = getattr(df[column], agg)()
        return {"aggregated": value, "text": f"{agg} of {column} = {value}"}

def compare_rows(df, currency1: str, currency2: str, date: str) -> dict:
    row1 = df[(df["Currency"] == currency1) & (df["Date"] == date)]
    row2 = df[(df["Currency"] == currency2) & (df["Date"] == date)]
    if row1.empty or row2.empty:
        return {"text": f"Rates not found for {currency1} or {currency2} on {date}"}
    rate1 = row1.iloc[0]["Rate to USD"]
    rate2 = row2.iloc[0]["Rate to USD"]
    return {
        "currency1": currency1,
        "rate1": rate1,
        "currency2": currency2,
        "rate2": rate2,
        "date": date,
        "text": f"On {date}, {currency1} = {rate1}, {currency2} = {rate2}"
    }

def get_column_stats(df, column: str) -> dict:
    if column not in df.columns:
        return {"text": f"Column '{column}' not found."}

    stats = {
        "mean": df[column].mean(),
        "min": df[column].min(),
        "max": df[column].max(),
        "std": df[column].std(),
        "count": df[column].count(),
        "median": df[column].median()
    }

    return {
        "stats": stats,
        "text": f"Stats for '{column}': {stats}"
    }

def list_columns(df) -> dict:
    columns = list(df.columns)
    return {
        "columns": columns,
        "text": f"Available columns: {', '.join(columns)}"
    }
