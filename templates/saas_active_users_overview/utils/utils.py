import pandas as pd
import os
from re import sub


def get_data(file_names):
    #  Returns a dictionary of dataframes, one item for each file of file_names array parameter.
    #  Example:
    #  file_names = ['data/active_users.csv', 'data/shop_events.csv', ...]
    #  dict_dfs ['active_users'] = A dataframe with 'data/active_users.csv' CSV file
    #  dict_dfs ['shop_events'] = A dataframe with 'data/shop_events.csv' CSV file

    dict_dfs = dict()
    for file_name in file_names:
        df = pd.read_csv(file_name)

        # Encuentra las columnas que contienen "_date" en su nombre
        columnas_fecha = [col for col in df.columns if "_date" in col]

        # Convierte las columnas identificadas con "_date" a datetime
        df[columnas_fecha] = df[columnas_fecha].apply(pd.to_datetime)

        dict_dfs[os.path.splitext(os.path.basename(file_name))[0]] = df

    return dict_dfs


def convert_dataframe_to_array(
    df,
):  ## -> hace lo mismo que df.to_dict(orient="records")
    columns_to_include = df.columns.tolist()  # Obtener la lista de nombres de columnas
    new_data = []

    for index, row in df.iterrows():
        new_dict = {column: row[column] for column in columns_to_include}
        new_data.append(new_dict)

    return new_data


def plot_beautiful_title(self, order, title, href, background_url):
    # HTML - Beatiful indicator
    indicator = beautiful_indicator(
        title=title, href=href, background_url=background_url
    )
    self.shimoku.plt.html(
        indicator,
        # menu_path=self.menu_path,
        order=order,
        rows_size=1,
        cols_size=12,
    )

    return order + 1


def beautiful_indicator(title, background_url, href):
    if not background_url:
        background_url: str = "https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a07a6d9e984908a5aca6a1_shim-anomaly-bg-s.jpg"

    title_style: str = sub(r"\s+", "", title)
    return (
        f"<head>"
        f"<style>.{title_style}{{height:121px; width:100%; border-radius:8px; padding:45px; background-position: center; background-size: cover; background-image: url('{background_url}'); color:#FFFFFF;}}</style>"
        f"</head>"
        f"<a href='{href}'>"
        f"<div class='{title_style}'>"
        f"<h3>"
        f"{title}"
        f"</h3>"
        f"</div>"
        f"</a>"
    )
