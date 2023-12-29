import pandas as pd
import calendar
import os


def get_data(file_names):
    """
    Loads multiple CSV files into a dictionary of pandas DataFrames.

    Parameters:
    file_names (list of str): List of paths to CSV files.

    Returns:
    dict: A dictionary mapping file base names (without extension) to their corresponding DataFrames.
    """
    dict_dfs = dict()
    for file_name in file_names:
        df = pd.read_csv(file_name)
        dict_dfs[os.path.splitext(os.path.basename(file_name))[0]] = df

    return dict_dfs


def process_sales_data(df):
    """
    Process sales orders performance data from a CSV file.

    Returns:
    Tuple: A tuple containing Income Total, Spend Total, Net Profit, Average Profit Per Order, and Net Profit by Month.
    """

    # Convert 'order_date' column to datetime format
    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d")

    # Extract month and year for monthly analysis
    df["month"] = df["order_date"].dt.month
    df["year"] = df["order_date"].dt.year

    # Calculate income total, spend total, and net profit
    income_total = df["order_spend"].sum()
    spend_total = df["order_cost"].sum()
    net_profit = income_total - spend_total

    # Calculate average profit per order
    average_profit_per_order = df.groupby("order_id")["order_cost"].sum().mean()

    # Calculate net profit by month
    net_profit_by_month = df.groupby(["year", "month"])[
        ["order_cost", "order_spend"]
    ].sum()
    net_profit_by_month["net_profit"] = (
        net_profit_by_month["order_spend"] - net_profit_by_month["order_cost"]
    )
    net_profit_by_month.rename(
        columns={
            "order_cost": "Expenses",
            "order_spend": "Income",
            "net_profit": "Net Profit",
        },
        inplace=True,
    )
    net_profit_by_month.index = pd.to_datetime(
        net_profit_by_month.index.map(lambda x: f"{x[0]}-{x[1]}"), format="%Y-%m"
    )
    net_profit_by_month["Month"] = net_profit_by_month.index.month
    net_profit_by_month["Month"] = net_profit_by_month["Month"].apply(
        lambda x: calendar.month_abbr[x]
    )

    return (
        income_total,
        spend_total,
        net_profit,
        average_profit_per_order,
        net_profit_by_month,
    )
