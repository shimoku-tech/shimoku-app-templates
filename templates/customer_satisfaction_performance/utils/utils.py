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
        df (DataFrame): DataFrame with columns 'customer_id', 'order_returned',
            'order_id', 'order_spend', 'order_rate', and 'order_date'.

    Returns:
        dict: A dictionary containing the following metrics:
            - 'Total Customers'
            - 'Customers with Returns'
            - 'Total Orders'
            - 'Orders with Returns'
            - 'Total Revenue'
            - 'Revenue Lost'
            - 'Real Revenue'
            - 'Customer Satisfaction'
            - 'Order Satisfaction'
            - 'Monthly Metrics'
    """

    # Total customers
    total_customers = df["customer_id"].nunique()

    # Customers with returns
    customers_with_returns = round(
        (df[df["order_returned"] == 1]["customer_id"].nunique() / total_customers) * 100
    )

    # Total orders
    total_orders = df["order_id"].nunique()

    # Orders with returns
    orders_with_returns = round(
        (df[df["order_returned"] == 1]["order_id"].nunique() / total_orders) * 100
    )

    # Customer Satisfaction
    customer_satisfaction = df.groupby("customer_id")["order_rate"].mean()

    # Define satisfaction categories
    satisfaction_categories = pd.cut(
        customer_satisfaction,
        bins=[0, 1, 2, 3, 4, 5],
        labels=[
            "Very Unsatisfied",
            "Unsatisfied",
            "Neutral",
            "Satisfied",
            "Very Satisfied",
        ],
    )

    # Count satisfaction categories
    customer_satisfaction_counts = satisfaction_categories.value_counts().to_dict()

    # Order Satisfaction
    df["order_date"] = pd.to_datetime(df["order_date"])
    daily_order_satisfaction = df.groupby(df["order_date"].dt.date)["order_rate"].mean()

    # Total Revenue
    total_revenue = df["order_spend"].sum()

    # Revenue Lost
    revenue_lost = df[df["order_returned"] == 1]["order_spend"].sum()

    # Real Revenue
    real_revenue = total_revenue - revenue_lost

    # Monthly Revenue Lost
    monthly_revenue_lost = (
        df[df["order_returned"] == 1]
        .groupby(df["order_date"].dt.strftime("%b"))["order_spend"]
        .sum()
    )

    # Monthly Total Revenue
    monthly_total_revenue = df.groupby(df["order_date"].dt.strftime("%b"))[
        "order_spend"
    ].sum()

    # Monthly Real Revenue
    monthly_real_revenue = monthly_total_revenue - monthly_revenue_lost

    # Monthly Orders
    monthly_orders = df.groupby(df["order_date"].dt.strftime("%b"))[
        "order_id"
    ].nunique()

    # Monthly Orders with Returns
    monthly_orders_with_returns = (
        df[df["order_returned"] == 1]
        .groupby(df["order_date"].dt.strftime("%b"))["order_id"]
        .nunique()
    )

    # Create a dictionary with the metrics
    results = {
        "Total Customers": total_customers,
        "Customers with Returns": customers_with_returns,
        "Total Orders": total_orders,
        "Orders with Returns": orders_with_returns,
        "Total Revenue": total_revenue,
        "Revenue Lost": revenue_lost,
        "Real Revenue": real_revenue,
        "Customer Satisfaction": customer_satisfaction_counts,
        "Order Satisfaction": daily_order_satisfaction.to_dict(),
        "Monthly Metrics": {
            "Monthly Orders": monthly_orders.to_dict(),
            "Monthly Orders with Returns": monthly_orders_with_returns.to_dict(),
            "Monthly Revenue Lost": monthly_revenue_lost.to_dict(),
            "Monthly Real Revenue": monthly_real_revenue.to_dict(),
        },
    }

    return results


def get_status(value: float):
    """
    Determine the status based on a given value.

    Args:
        value (float): A numeric value.

    Returns:
        str: A status string, either "success," "warning," or "error."
    """
    if value < 33:
        return "success"
    elif 33 <= value <= 66:
        return "warning"
    else:
        return "error"


def get_column_name_by_value(data_dict: dict, value_to_find: str):
    """
    Find the column name in a dictionary of data based on its value.

    Args:
        data_dict (dict): A dictionary where values are to be searched.
        value_to_find: The value to search for in the dictionary.

    Returns:
        str or None: The column name if found, or None if not found.
    """
    for column_name, column_data in data_dict.items():
        if column_data is value_to_find:
            return column_name
    return None
