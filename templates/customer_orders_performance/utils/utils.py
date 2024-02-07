import pandas as pd
import os
from re import sub


def get_data(file_names: list) -> dict:
    """Returns a dictionary of dataframes, one item for each file of file_names array parameter.
    Example:
    file_names = ['data/active_users.csv', 'data/shop_events.csv', ...]
    dict_dfs ['active_users'] = A dataframe with 'data/active_users.csv' CSV file
    dict_dfs ['shop_events'] = A dataframe with 'data/shop_events.csv' CSV file

    Args:
        file_names (list): a list of file names CSV.
    Returns:
        dict_dfs (dict): A dictionary of dataframes.
    """

    dict_dfs = dict()
    for file_name in file_names:
        df = pd.read_csv(file_name)

        # Finds the columns containing "_date" in their name
        columnas_fecha = [col for col in df.columns if "_date" in col]

        # Convert columns identified with "_date" to datetime
        df[columnas_fecha] = df[columnas_fecha].apply(pd.to_datetime)

        dict_dfs[os.path.splitext(os.path.basename(file_name))[0]] = df

    return dict_dfs


def convert_dataframe_to_array(df: pd.DataFrame) -> list:
    """Return a list, convert a dataframe to a list.

    Args:
        df (pd.DataFrame): A dataFrame to convert.

    Returns:
        new_data (List): A List with the dataframe information.
    """
    # Get list of column names
    columns_to_include = df.columns.tolist()
    new_data = []

    for index, row in df.iterrows():
        new_dict = {column: row[column] for column in columns_to_include}
        new_data.append(new_dict)

    return new_data

def beautiful_header(title: str) -> str:
    """Return a HTML structure to plot the header on the menu path.

    Args:
        title (str): title of the header in the menu path.

    Returns:
        str: HTML structure to plot the header.
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