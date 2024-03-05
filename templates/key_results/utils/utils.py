import pandas as pd
import os
from numpy import inf


def get_data(file_names: list) -> dict:
    """Returns a dictionary of dataframes, one item for each file of file_names array parameter.
    Example:
    file_names = ['data/active_users.csv', 'data/shop_events.csv', ...]
    dict_dfs ['active_users'] = A dataframe with 'data/active_users.csv' CSV file
    dict_dfs ['shop_events'] = A dataframe with 'data/shop_events.csv' CSV file

    Args:
        dict_dfs (dict): A dictionary of dataframes.
    """

    dict_dfs = dict()
    for file_name in file_names:
        df = pd.read_csv(file_name)

        # Finds the columns containing "_date" in their name
        columnas_fecha = [col for col in df.columns if "date" in col or "time" in col]

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
    """Return a HTML structure to plot the header on the menu path

    Args:
        title (str): title of the header in the menu path

    Returns:
        str: HTML structure to plot the header
    """
    return (
        "<head>"
            "<style>"
                # Styles title
                ".component-title{height:auto; width:100%; "
                "border-radius:16px; padding:16px;"
                "display:flex; align-items:center;"
                "background-color:var(--chart-C1); color:var(--color-white);}"
                # Start icons style
                ".big-icon-banner"
                "{width:48px; height: 48px; display: flex;"
                "margin-right: 16px;"
                "justify-content: center;"
                "align-items: center;"
                "background-size: contain;"
                "background-position: center;"
                "background-repeat: no-repeat;"
                "background-image: url('https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63594ccf3f311a98d72faff7_suite-customer-b.svg');}"
                # End icons style
                ".base-white{color:var(--color-white);}"
            "</style>"
        "</head>"  # Styles subtitle
        "<div class='component-title'>"
        "<div class='big-icon-banner'></div>"
        "<div class='text-block'>"
        "<h1>" + title + "</h1>"
        "</div>"
    )


def get_indicator_color(value: float) -> str:
    if value < 50:
        return "error"
    elif value < 80:
        return "warning"
    else:
        return "success"
def get_gauge_color(value: float) -> str:
    if value < 50:
        return "status-error"
    elif value < 80:
        return 4
    else:
        return 2

def get_table_color_range_numerical(df: pd.DataFrame) -> dict:
    value = df.head().min().values[1]
    value = 1 if value < 2 else value
    return {
        (-inf, 0) : "error",
        (1, 1) : "warning",
        (value, inf) : "active"
    }
def get_table_color_range_categorical(df: pd.DataFrame) -> dict:
    df_zero = df[df["frequency"] == 0]
    df_one = df[df["frequency"] == 1]
    return {
        row["chart_name"] : "error"
    for _, row in df_zero.iterrows()} | {
        row["chart_name"] : "warning"
    for _, row in df_one.iterrows()}

def add_new_charts(charts, charts_str):
    old_charts = charts.copy()
    new_charts = charts_str.split()[::2]
    for chart in new_charts:
        if not chart in old_charts:
            old_charts.append(chart)
    return old_charts

def compute_percentage(total, value):
    return round(100.0 * value / total if total != 0 else 0, 2)

def get_columns_options(dataframe):
    # Calcular la longitud máxima por columna
    columns_lengths = [len(str(column)) for column in dataframe.columns]
    max_values_lengths = dataframe.map(lambda value: len(str(value))).max()

    # Ajustar el ancho máximo permitido para las columnas
    max_width = 12  # Puedes ajustar este valor según tus necesidades

    # Calcular los anchos ajustados
    widths_ajustados = [max_width*max(column, value) for column, value in zip(columns_lengths, max_values_lengths)]

    # Crear el diccionario columns_options
    columns_options = {col: {'width': width} for col, width in zip(dataframe.columns, widths_ajustados)}

    return columns_options