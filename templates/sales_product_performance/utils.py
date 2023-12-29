import pandas as pd
import os
from typing import List


def get_data(file_names: List[str]):
    """
    Returns a dictionary of dataframes, one item for each file of file_names array parameter.
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
