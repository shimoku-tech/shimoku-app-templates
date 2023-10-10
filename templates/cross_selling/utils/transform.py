import pandas as pd


def count_column_values(df, column):
    """
    Count occurrences of values in a specified column of a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to analyze.
        column (str): The name of the column to count values in.

    Raises:
        ValueError: If the specified 'column' is not found in the DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame containing counts of unique values in 'column'.
    """
    if column not in df.columns:
        raise ValueError(f"Column {column} not in dataframe")
    return df.groupby(by=column).agg({column: "count"})


def count_column_values_with_filter(df, column, filter_column, filter_value):
    """
    Count occurrences of values in 'column' when 'filter_column' matches 'filter_value'.

    Args:
        df (pandas.DataFrame): The DataFrame to analyze.
        column (str): The name of the column to count values in.
        filter_column (str): The name of the column to use for filtering.
        filter_value (str): The value to filter 'filter_column' by.

    Raises:
        ValueError: If 'column' or 'filter_column' is not found in the DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame containing counts of unique 'column' values
                         when 'filter_column' matches 'filter_value'.
    """
    if column not in df.columns:
        raise ValueError(f"Column {column} not in dataframe")
    if filter_column not in df.columns:
        raise ValueError(f"Column {filter_column} not in dataframe")
    return (
        df[df[filter_column] == filter_value].groupby(by=column).agg({column: "count"})
    )


def df_to_indicator_product_data(df, column_name):
    """
    Convert a DataFrame to a dictionary of indicator product data.

    Args:
        df (pandas.DataFrame): The DataFrame to convert.
        column_name (str): The name of the column to use as indicator titles.

    Returns:
        dict: A dictionary where keys are unique values from 'df' and values are
              dictionaries with 'value', 'title', and 'color' keys.
    """
    unique_values = df.index.tolist()
    indicator_product_data = {}

    for value in unique_values:
        data = {
            "value": df.loc[value, column_name],
            "title": value,
            "color": "success",
        }
        indicator_product_data[value] = data

    return {"Productos": indicator_product_data}
