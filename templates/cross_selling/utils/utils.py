import re
import json
import pandas as pd
import numpy as np

from functools import cached_property
from typing import Iterable

# Global variable for the data folder
data_folder = "data"


def read_csv(name: str, **kwargs) -> pd.DataFrame:
    """
    Reads a CSV file into a pandas DataFrame.

    Parameters:
        name (str): The name of the file to read (without the '.csv' extension).
        **kwargs: Additional keyword arguments to pass to pandas.read_csv().

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return pd.read_csv(f"{data_folder}/{name}.csv", **kwargs)


def to_csv(df: pd.DataFrame, name: str, **kwargs):
    """
    Writes a pandas DataFrame to a CSV file.

    Parameters:
        df (pd.DataFrame): The DataFrame to write.
        name (str): The name of the file to write (without the '.csv' extension).
        **kwargs: Additional keyword arguments to pass to DataFrame.to_csv().
    """
    df.to_csv(f"{data_folder}/{name}.csv", index=False, **kwargs)


def format_number(number) -> str:
    """
    Formats a number with a thousands separator as used in Spain.

    Parameters:
        number: The number to format.

    Returns:
        str: The formatted number as a string.
    """
    return "{0:,}".format(number).replace(",", ".")


def search_string(pattern: str, array: Iterable) -> list:
    """
    Searches for a pattern in an iterable and returns a list of matches.

    Parameters:
        pattern (str): The regex pattern to search for.
        array (Iterable): The iterable to search through.

    Returns:
        list: A list of elements from the iterable that match the pattern.
    """
    prop_regex = re.compile(pattern)
    return list(filter(lambda x: prop_regex.search(x), array))


class DFs:
    """
    A class representing a collection of DataFrames.

    This class uses cached properties to lazily load DataFrames from CSV files.
    """

    @cached_property
    def df_importance(self) -> pd.DataFrame:
        """
        Lazy loading of the 'df_importance' DataFrame.

        Returns:
            pd.DataFrame: The loaded DataFrame.
        """
        return read_csv("df_importance")

    @cached_property
    def df_premodel_predicted(self) -> pd.DataFrame:
        """
        Lazy loading of the 'df_premodel_predicted' DataFrame.

        Returns:
            pd.DataFrame: The loaded DataFrame.
        """
        return read_csv("df_premodel_predicted")

    @cached_property
    def df_recommender_table(self) -> pd.DataFrame:
        """
        Lazy loading and processing of the 'df_recommender_table' DataFrame.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """
        df_recommender_table = read_csv("table_product_recommender")
        df_recommender_table.rename(
            columns={"_base_values": "base_values"}, inplace=True
        )
        return df_recommender_table


# -- Transformations


def map_factor_name(factor_name: str) -> str:
    """
    Maps specific factor names to their desired names.

    Parameters:
        factor_name (str): The original name of the factor.

    Returns:
        str: The mapped name of the factor.
    """
    if factor_name == "ResultHistoricoCampañas":
        return "ResultHistoricoCRM"
    return factor_name


def factors_to_string(row: pd.Series, names_col: str, values_col: str) -> str:
    """
    Converts encoded factor names and values to a readable string format.

    Parameters:
        row (pd.Series): The row of the DataFrame containing the factors.
        names_col (str): The column name containing factor names.
        values_col (str): The column name containing factor values.

    Returns:
        str: A string representation of the top factors and their values.
    """
    factor_list = eval(row[names_col])[:3]
    factor_value_list = eval(row[values_col])[:3]

    filtered_meta_list = []
    for idx, val in enumerate(factor_value_list):
        round_val = round(val * 100)
        if 1 <= round_val or round_val <= -1:
            filtered_meta_list.append({"idx": idx, "val": round_val})

    filtered_factor_values = [f"{meta['val']}%" for meta in filtered_meta_list]
    filtered_factor_list = [factor_list[meta["idx"]] for meta in filtered_meta_list]

    def grab_factor_val(row: pd.Series, factor_list: list) -> list:
        """
        Retrieves the actual values of factors, not their importance.

        Parameters:
            row (pd.Series): The row of the DataFrame containing the factors.
            factor_list (list): A list of factor names.

        Returns:
            list: A list of formatted factor values.
        """
        factors_per_val = []
        for factor in factor_list:
            val = row[factor]
            formatted_val = (
                f"({val})"
                if not (isinstance(val, type(np.nan)) and np.isnan(val))
                else "()"
            )
            factors_per_val.append(formatted_val)

        return factors_per_val

    filtered_factor_per_val = grab_factor_val(row, filtered_factor_list)

    filtered_factor_list = list(map(map_factor_name, filtered_factor_list))

    assert len(filtered_factor_list) == len(filtered_factor_values)

    pre_joined = [
        f"{factor} {filtered_factor_values[idx]} {filtered_factor_per_val[idx]}"
        for idx, factor in enumerate(filtered_factor_list)
    ]

    return ", ".join(pre_joined)


def factors_to_dict(
    row: pd.Series, names_col: str, values_col: str, acronym: str
) -> dict:
    """
    Converts encoded factor names and values to a dictionary format.

    Parameters:
        row (pd.Series): The row of the DataFrame containing the factors.
        names_col (str): The column name containing factor names.
        values_col (str): The column name containing factor values.
        acronym (str): The acronym to use as a prefix in the dictionary keys.

    Returns:
        dict: A dictionary representation of the factors and their values.
    """
    factor_list = eval(row[names_col])[:3]

    factor_weight_list = eval(row[values_col])[:3]

    filtered_meta_list = []

    # Only extract those
    for idx, val in enumerate(factor_weight_list):
        round_val = round(val * 100)
        if round_val >= 1 or round_val <= -1:
            filtered_meta_list.append({"idx": idx, "val": round_val})

    filtered_factor_weights = [meta["val"] for meta in filtered_meta_list]

    filtered_factor_list = [factor_list[meta["idx"]] for meta in filtered_meta_list]

    # Grab actual values
    filtered_factor_values = []
    for factor in filtered_factor_list:
        filtered_factor_values.append(row[factor])

    assert len(filtered_factor_list) == len(filtered_factor_weights)
    assert len(filtered_factor_values) == len(filtered_factor_list)

    factor_dict = {}
    for i in range(len(filtered_factor_weights)):
        factor_dict[f"{acronym}_{i}_name"] = filtered_factor_list[i]
        factor_dict[f"{acronym}_{i}_weight_pct"] = filtered_factor_weights[i]
        factor_dict[f"{acronym}_{i}_value"] = filtered_factor_values[i]

    return factor_dict
