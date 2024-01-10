import pandas as pd
import os
from typing import List


def get_data(file_names: List[str]):
    """
    Parameters:
    file_names (List[str]): List of paths for .csv files
    
    Returns:
    Dictionary of dataframes, one item for each file of file_names array parameter.
    
    Example:
    file_names = ['data/active_users.csv', 'data/shop_events.csv', ...]
    dict_dfs ['active_users'] = A dataframe with 'data/active_users.csv' CSV file
    dict_dfs ['shop_events'] = A dataframe with 'data/shop_events.csv' CSV file
    """

    dict_dfs = dict()
    for file_name in file_names:
        df = pd.read_csv(file_name)

        # Find columns that contain "_date" in their name
        columnas_fecha = [col for col in df.columns if "_date" in col]

        # Converts columns identified with "_date" to datetime
        df[columnas_fecha] = df[columnas_fecha].apply(pd.to_datetime)

        dict_dfs[os.path.splitext(os.path.basename(file_name))[0]] = df

    return dict_dfs

def beautiful_indicator(title: str):
    """
    Create a header with HTML

    Parameters:
    title (str): Title of the dashboard

    Returns:
    Literal string with the HTML to plot the header section.
    """

    return (
        "<head>"
        "<style>"  # Styles title
        ".component-title{height:auto; width:100%; "
        "border-radius:16px; padding:16px;"
        "display:flex; align-items:center;"
        "background-color:var(--chart-C1); color:var(--color-white);}"
        "</style>"
        # Start icons style
        "<style>.big-icon-banner"
        "{width:48px; height: 48px; display: flex;"
        "margin-right: 16px;"
        "justify-content: center;"
        "align-items: center;"
        "background-size: contain;"
        "background-position: center;"
        "background-repeat: no-repeat;"
        "background-image: url('https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63594ccf3f311a98d72faff7_suite-customer-b.svg');}"
        "</style>"
        # End icons style
        "<style>.base-white{color:var(--color-white);}</style>"
        "</head>"  # Styles subtitle
        "<div class='component-title'>"
        "<div class='big-icon-banner'></div>"
        "<div class='text-block'>"
        "<h1>" + title + "</h1>"
        "</div>"
    )


def groupby_sum(df: pd.DataFrame, groupby_col: str, sum_col: str):
    """
    Group a DataFrame and sum a specific column.

    Parameters:
    df (DataFrame): The DataFrame to group and summarize.
    groupby_col (str): The column name to groupby.
    sum_col (str): The column name to sum.

    Returns:
    DataFrame: Groupby DataFrame with summarized column.
    """

    return df.groupby(groupby_col)[sum_col].sum().reset_index()
