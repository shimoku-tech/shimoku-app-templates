import os
from typing import List, Dict, Union, Any, Optional
from datetime import datetime
import pandas as pd
from pandas import DataFrame


def format_store_id(number: int) -> str:
    """
    Formats a store identifier.

    Args:
        number (int): Store number.

    Returns:
        str: Formatted store identifier.
    """
    return f"Store {number}"


def prepare_pivot(
    df: DataFrame, index: str, columns: str, values: str, unique_stores: List[str]
) -> DataFrame:
    """
    Prepares a pivoted DataFrame with cumulative sales.

    Args:
        df (DataFrame): DataFrame with grouped and summed data.
        index (str): Name of the column to be used as an index in the pivot.
        columns (str): Name of the column to be used as columns in the pivot.
        values (str): Name of the column to be used for values in the pivot.
        unique_stores (list): List of unique store_ids to reindex the DataFrame.

    Returns:
        DataFrame: Pivoted DataFrame with cumulative sales and columns for all store_ids.
    """
    # Group the data and calculate cumulative sales.
    df_grouped = df.groupby([f"{columns}", f"{index}"]).agg({f"{values}": "sum"})
    df_cumulative = df_grouped.groupby(level=0).cumsum().reset_index()

    # Pivot the data.
    df_pivot = df_cumulative.pivot(index=index, columns=columns, values=values)

    # Step 1: Fill NaN values in the first row with zeros.
    df_pivot.iloc[0] = df_pivot.iloc[0].fillna(0)

    # Fill NaNs using the 'forward fill' method.
    df_pivot.ffill(axis=0, inplace=True)

    # Add columns with zeros for any missing store_id.
    for store_id in unique_stores:
        if store_id not in df_pivot.columns:
            df_pivot[store_id] = 0

    # Reorder columns if needed.
    df_pivot = df_pivot.reindex(sorted(df_pivot.columns), axis=1)
    df_pivot = df_pivot.reset_index()

    return df_pivot


def get_data(file_names: List[str]) -> Dict[str, DataFrame]:
    """
    Loads multiple CSV files into a dictionary of pandas DataFrames.

    Args:
        file_names (list of str): List of paths to CSV files.

    Returns:
        dict: A dictionary mapping file base names (without extension) to their corresponding DataFrames.
    """
    dict_dfs = dict()
    for file_name in file_names:
        df = pd.read_csv(file_name)
        dict_dfs[os.path.splitext(os.path.basename(file_name))[0]] = df

    return dict_dfs


def process_retail_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Processes retail sales data.

    Args:
        df (DataFrame): DataFrame with the following columns:
            - 'sale_id' (str): Unique sale identifier.
            - 'store_id' (str): Unique store identifier.
            - 'user_id' (str): Unique user identifier.
            - 'sale_date' (datetime): Sale date.
            - 'sales_amount' (float): Sale amount.

    Returns:
        Dict[str, Any]: A dictionary containing KPIs and DataFrames for charts.
    """
    # Convert 'sale_date' to datetime and set as index
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["store_id"] = df["store_id"].apply(format_store_id)
    df.set_index("sale_date", inplace=True)

    # Calculate KPIs
    total_stores = df["store_id"].nunique()
    total_sales = df["sales_amount"].sum()
    average_sales_per_store = total_sales / total_stores
    total_users = df["user_id"].nunique()
    average_sales_per_user = total_sales / total_users

    # Get unique store_ids from the original DataFrame
    unique_stores = df["store_id"].unique()
    current_year = datetime.now().year

    # Filter for current time periods
    current_week = df[
        (df.index.isocalendar().week == datetime.now().isocalendar().week)
        & (df.index.isocalendar().year == current_year)
    ].reset_index()
    current_month = df[
        (df.index.month == datetime.now().month) & (df.index.year == current_year)
    ].reset_index()
    current_year = df[df.index.year == current_year].reset_index()

    # Sales and users by store for the current period
    sales_users_by_store = {
        "Current Week": current_week.groupby("store_id")
        .agg({"sales_amount": "sum", "user_id": "nunique"})
        .reset_index(),
        "Current Month": current_month.groupby("store_id")
        .agg({"sales_amount": "sum", "user_id": "nunique"})
        .reset_index(),
        "Current Year": current_year.groupby("store_id")
        .agg({"sales_amount": "sum", "user_id": "nunique"})
        .reset_index(),
    }
    for key, df in sales_users_by_store.items():
        df.rename(
            columns={"sales_amount": "Sales Amount", "user_id": "Number of Users"},
            inplace=True,
        )

    current_week_sales = current_week["sales_amount"].sum()
    current_month_sales = current_month["sales_amount"].sum()
    current_year_sales = current_year["sales_amount"].sum()

    # Sales percentage by store
    sales_percentage_by_store = {
        "Current Week": (
            round(
                current_week.groupby("store_id")["sales_amount"].sum()
                * 100
                / current_week_sales,
                2,
            )
        ).reset_index(),
        "Current Month": (
            round(
                current_month.groupby("store_id")["sales_amount"].sum()
                * 100
                / current_month_sales,
                2,
            )
        ).reset_index(),
        "Current Year": (
            round(
                current_year.groupby("store_id")["sales_amount"].sum()
                * 100
                / current_year_sales,
                2,
            )
        ).reset_index(),
    }

    # Group data by 'store_id' and 'sale_date', and calculate cumulative sales.
    df_weekly_sorted = current_week.sort_values(by="sale_date")
    df_weekly_pivot = prepare_pivot(
        df_weekly_sorted, "sale_date", "store_id", "sales_amount", unique_stores
    )
    new_values_weekly = [f"Day {day}" for day in df_weekly_pivot["sale_date"].dt.day]
    df_weekly_pivot[
        "sale_date"
    ] = new_values_weekly  # Group by 'store_id' and weeks for the current month.
    df_weekly_pivot = df_weekly_pivot.rename(columns={"sale_date": "Current Week"})

    df_monthly_sorted = current_month.sort_values(by="sale_date").set_index("sale_date")
    df_monthly_sorted["week"] = df_monthly_sorted.index.isocalendar().week
    df_monthly_pivot = prepare_pivot(
        df_monthly_sorted, "week", "store_id", "sales_amount", unique_stores
    )
    new_values_monthly = [f"Week {week}" for week in df_monthly_pivot["week"]]
    df_monthly_pivot["week"] = new_values_monthly
    df_monthly_pivot = df_monthly_pivot.rename(columns={"week": "Current Month"})

    df_yearly_sorted = current_year.sort_values(by="sale_date").set_index("sale_date")
    df_yearly_sorted["month"] = df_yearly_sorted.index.month
    df_yearly_pivot = prepare_pivot(
        df_yearly_sorted, "month", "store_id", "sales_amount", unique_stores
    )
    new_values_yearly = [f"Month {month}" for month in df_yearly_pivot["month"]]
    df_yearly_pivot["month"] = new_values_yearly
    df_yearly_pivot = df_yearly_pivot.rename(columns={"month": "Current Year"})

    # Create the results dictionary
    results = {
        "Stores": {"Value": total_stores, "Description": ""},
        "Total Sales": {"Value": total_sales, "Description": ""},
        "Average Sales": {
            "Value": average_sales_per_store,
            "Description": "per store",
        },
        "Users": {"Value": total_users, "Description": ""},
        "Average Sales ": {
            "Value": average_sales_per_user,
            "Description": "per user",
        },
        "Sales Users by Store": sales_users_by_store,
        "Sales Percentage by Store": sales_percentage_by_store,
        "Sales Accumulated by Store": {
            "Current Week": df_weekly_pivot,
            "Current Month": df_monthly_pivot,
            "Current Year": df_yearly_pivot,
        },
    }

    return results


def get_column_name_by_value(
    data_dict: dict[str, Any], value_to_find: Any
) -> Optional[str]:
    """
    Find the key (column name) in a dictionary of data based on its value.

    Args:
        data_dict (dict[str, Any]): A dictionary where values are to be searched.
        value_to_find (Any): The value to search for in the dictionary.

    Returns:
        Optional[str]: The column name (key) if found, or None if not found.
    """
    for column_name, column_data in data_dict.items():
        if column_data is value_to_find:
            return column_name

    for column_name, column_data in data_dict.items():
        if isinstance(column_data, pd.DataFrame) and column_data.equals(value_to_find):
            return column_name

    return None
