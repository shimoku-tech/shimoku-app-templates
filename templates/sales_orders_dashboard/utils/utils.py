import pandas as pd
import os
from typing import List


def get_data(file_names: List[str]):
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


def process_sales_data(df: pd.DataFrame):
    """
    Process sales orders performance data.

    Args:
        df (DataFrame): DataFrame with the following columns:
            - 'order_date' (datetime): Date of the order.
            - 'order_id' (str): Unique identifier for each order.
            - 'customer_id' (str): Unique identifier for each customer.
            - 'order_spend' (float): Amount spent in the order.
            - 'market_segment' (str): Segment to which the market belongs.
            - 'geo_segment' (str): Segment indicating geographical location.

    Returns:
        dict: A dictionary containing the following metrics:
            - 'Total Customers': Total unique customers.
            - 'Orders per Month': Rounded count of orders in the last month.
            - 'Average spend per order': Rounded average spend per order.
            - 'Growth Rate': Month-over-month growth rate.
            - 'Sales by Market Segment': Sales data by market segment.
            - 'Sales National vs International': Sales data by geographical segment.
    """
    # Calculate Total Customers
    total_accounts = df["customer_id"].nunique()

    # Ensure 'order_date' column is in ascending chronological order
    df["order_date"] = pd.to_datetime(df["order_date"])
    df.sort_values(by="order_date", inplace=True)

    # Create 'month' column in 'yyyy-mm' format
    df["month"] = df["order_date"].dt.strftime("%Y-%m")

    # Filter DataFrame to include only the last month and calculate rounded unique order count
    last_month_orders = df[df["month"] == df["month"].iloc[-1]]
    orders_last_month = round(last_month_orders["order_id"].nunique())

    # Calculate Average Spend per Order
    average_spend_per_order = round(df.groupby("order_id")["order_spend"].sum().mean())

    # Calculate Month-over-Month Growth Rate
    df["order_month"] = pd.to_datetime(df["order_date"]).dt.month
    previous_month = df[df["order_month"] == df["order_month"].max() - 1]
    current_month = df[df["order_month"] == df["order_month"].max()]
    growth_rate = round(
        (current_month["order_spend"].sum() - previous_month["order_spend"].sum())
        / previous_month["order_spend"].sum(),
        2,
    )

    # Calculate Sales by Market Segment
    sales_by_market_segment_month = (
        df.groupby(["month", "market_segment"])["order_spend"].sum().reset_index()
    )

    # Calculate Sales National vs. International
    sales_national_vs_international_month = (
        df.groupby(["month", "geo_segment"])["order_spend"].sum().reset_index()
    )

    # Create the 'results' dictionary with all calculated variables
    results = {
        "Total Accounts": total_accounts,
        "Orders per Month": orders_last_month,
        "Average spend per order": average_spend_per_order,
        "Growth Rate": growth_rate,
        "Sales Growth by Market Segment": sales_by_market_segment_month,
        "Sales National vs International": sales_national_vs_international_month,
    }

    return results


def get_column_name_by_value(data_dict: dict, value_to_find):
    """
    Find the key (column name) in a dictionary of data based on its value.

    Args:
        data_dict (dict): A dictionary where values are to be searched.
        value_to_find: The value to search for in the dictionary.

    Returns:
        str or None: The column name (key) if found, or None if not found.
    """
    for column_name, column_data in data_dict.items():
        if column_data is value_to_find:
            return column_name

    for column_name, column_data in data_dict.items():
        if isinstance(column_data, pd.DataFrame) and column_data.equals(value_to_find):
            return column_name

    return None
