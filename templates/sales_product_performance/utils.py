import pandas as pd
import os


def get_data(file_names):
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

        # Encuentra las columnas que contienen "_date" en su nombre
        columnas_fecha = [col for col in df.columns if "_date" in col]

        # Convierte las columnas identificadas con "_date" a datetime
        df[columnas_fecha] = df[columnas_fecha].apply(pd.to_datetime)

        dict_dfs[os.path.splitext(os.path.basename(file_name))[0]] = df

    return dict_dfs
