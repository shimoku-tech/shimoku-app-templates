# Core python libraries
import re
import json
from functools import cached_property
from typing import Iterable


# Third party
import pandas as pd

# -- I/O
data_folder = "data"


def read_csv(name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(f"data/{name}.csv", **kwargs)


def to_csv(df: pd.DataFrame, name: str, **kwargs):
    df.to_csv(f"{data_folder}/{name}.csv", index=False, **kwargs)


def read_json(name: str):
    with open(f"data/{name}.json", "r") as f:
        return json.load(f)


def write_json(filename: str, dictionary: dict):
    with open(f"data/{filename}.json", "w") as f:
        f.write(json.dumps(dictionary, indent=4))


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


def pretty_print_dict(_dict: dict):
    print(json.dumps(_dict, indent=4))


# --- Data transformation
prod_cat_regex = re.compile("Correduria(.*)")


def get_prod_category(product_name: str):
    """
    Determinar categoría de productos por Muta o correduria
    """

    if prod_cat_regex.match(product_name):
        return "Correduria"
    return "Mutua"


# --- Read processed data lazily
class DFs:
    """
    Collection of DataFrames
    """

    @cached_property
    def df_pdp(self) -> pd.DataFrame:
        return read_csv("df_pdp")

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

    @cached_property
    def df_recommender_table_split(self) -> pd.DataFrame:
        df_recommender_split = read_csv(
            "table_product_recommender_split",
            dtype={
                "barrier_0_value": "str",
                "barrier_1_value": "str",
                "barrier_2_value": "str",
                "driver_0_value": "str",
                "driver_1_name": "str",
                "driver_1_value": "str",
                "driver_2_name": "str",
                "driver_2_value": "str",
            },
        )
        df_recommender_split.rename(
            columns={
                "_base_values": "base_values",
            },
            inplace=True,
        )
        return df_recommender_split

    @cached_property
    def df_importance_pdb(self) -> pd.DataFrame:
        """
        Merged df_importance and df_pdb by product
        """
        # Set appropiate columns names
        df_importance_pdp = (
            read_csv(
                "df_importance_pdp",
                dtype={
                    "class": "category",
                    "column_target": "str",
                    "feature": "str",
                    "interval": "category",
                },
            )
            .rename(
                columns={
                    "column_target": "product",
                    "pd": "Probability",
                }
            )
            .query(
                #  si quieres trabajar con la decisión de compra, coger 1
                f"`class` == '1.0'"
            )
        )

        print(df_importance_pdp)

        return df_importance_pdp
