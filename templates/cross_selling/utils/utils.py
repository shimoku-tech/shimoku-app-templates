import re
import json
import pandas as pd
import numpy as np

from functools import cached_property
from typing import Iterable

# -- I/O
data_folder = "data"

def read_csv(name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(f"data/{name}.csv", **kwargs)


def to_csv(df: pd.DataFrame, name: str, **kwargs):
    df.to_csv(f"{data_folder}/{name}.csv", index=False, **kwargs)


def format_number(number):
    """
    Set thousands separator as the one used in SPAIN
    """
    return "{0:,}".format(number).replace(",", ".")


def search_string(pattern, array: Iterable) -> list:
    """
    Search values between a list
    """
    prop_regex = re.compile(pattern)

    return list(
        filter(
            lambda x: prop_regex.search(x),
            array,
        )
    )


# --- Read processed data lazily
class DFs:
    """
    Collection of DataFrames
    """

    @cached_property
    def df_importance(self) -> pd.DataFrame:
        return read_csv("df_importance")

    @cached_property
    def df_premodel_predicted(self) -> pd.DataFrame:
        return read_csv("df_premodel_predicted")

    @cached_property
    def df_recommender_table(self) -> pd.DataFrame:
        df_recommender_table = read_csv(
            "table_product_recommender",
        )
        df_recommender_table.rename(
            columns={
                "_base_values": "base_values",
            },
            inplace=True,
        )
        return df_recommender_table


# -- Transformations

def map_factor_name(factor_name):
    """
    Change name of some factors
    """

    if factor_name == "ResultHistoricoCampañas":
        return "ResultHistoricoCRM"
    return factor_name


def factors_to_string(row: pd.Series, names_col: str, values_col: str):
    """
    Convert the encode string list to
    actual readable values
    """
    # DONE: multiplicar por 100, sin decimales
    # DONE: Quitar los dos puntos

    factor_list = eval(row[names_col])[:3]

    factor_value_list = eval(row[values_col])[:3]

    filtered_meta_list = []

    for idx, val in enumerate(factor_value_list):
        round_val = round(val * 100)
        if round_val >= 1 or round_val <= -1:
            filtered_meta_list.append({"idx": idx, "val": round_val})

    filtered_factor_values = [f"{meta['val']}%" for meta in filtered_meta_list]

    filtered_factor_list = [factor_list[meta["idx"]] for meta in filtered_meta_list]

    def grab_factor_val(row: pd.Series, factor_list: list):
        """
        Grab actual value not importance
        """
        factors_per_val = []
        for factor in factor_list:
            val = row[factor]

            formatted_val = f"({val})"
            if isinstance(val, type(np.nan)):
                if np.isnan(val):
                    formatted_val = "()"

            factors_per_val.append(formatted_val)

        return factors_per_val

    # Actual values not importance
    filtered_factor_per_val = grab_factor_val(row, filtered_factor_list)

    # Change names of factors
    filtered_factor_list = list(
        map(
            map_factor_name,
            filtered_factor_list,
        )
    )

    assert len(filtered_factor_list) == len(filtered_factor_values)

    pre_joined = [
        f"{factor} {filtered_factor_values[idx]} {filtered_factor_per_val[idx]}"
        for idx, factor in enumerate(filtered_factor_list)
    ]

    return ", ".join(pre_joined)


def factors_to_dict(row: pd.Series, names_col: str, values_col: str, acronym: str):
    """
    Convert the encoded string list to
    actual readable values
    """
    # DONE: multiplicar por 100, sin decimales
    # DONE: Quitar los dos puntos
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
