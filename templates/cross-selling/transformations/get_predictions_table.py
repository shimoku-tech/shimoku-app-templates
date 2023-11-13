import re
import json
import os
from pathlib import Path
import pandas as pd
import numpy as np

from utils.utils import read_csv, to_csv, search_string, factors_to_string


import pandas as pd
import re

def get_lead_scoring(probability_percentage):
    """
    Determine the lead scoring category based on the probability percentage.

    Args:
        probability_percentage (float): The probability percentage.

    Returns:
        str: The lead scoring category ('Low', 'Medium', or 'High').
    """
    if probability_percentage < 50:
        return "Low"
    elif probability_percentage < 75:
        return "Medium"
    else:
        return "High"

def get_usable_premodel_predicted() -> pd.DataFrame:
    """
    Transforms a DataFrame with a high number of columns (df_premodel_predicted)
    to a DataFrame with a lower number of columns.

    The function performs the following steps:
    1. Reads the premodel predicted data.
    2. Extracts columns related to probability of purchase predictions.
    3. Extracts columns related to actual product purchase.
    4. Pivots the tables for probability and actual purchase.
    5. Merges these tables.
    6. Filters out already purchased policies.

    Returns:
        pd.DataFrame: The transformed DataFrame with usable premodel predictions.
    """
    # Read premodel predicted data
    df_premodel_predicted = read_csv("df_premodel_predicted")

    # Regex patterns for probability and product columns
    regex_probability_product = r"^(probability_Product_)(.*)(_1\.0)$"
    regex_product = r"^Product_(.*)"

    # Extract probability and product columns
    col_pred_prob = search_string(regex_probability_product, df_premodel_predicted.columns)
    col_pred_product_buy = search_string(regex_product, df_premodel_predicted.columns)

    # Create DataFrame for probability of purchase
    df_premodel_usable_raw_proba = df_premodel_predicted[["sPerson"] + col_pred_prob]

    # Create DataFrame for actual product purchase
    df_premodel_usable_raw_product = df_premodel_predicted[["sPerson"] + col_pred_product_buy]

    # Pivot probability table
    df_premodel_usable_proba = df_premodel_usable_raw_proba.melt(
        id_vars=["sPerson"], value_name="purchase_probability", var_name="product"
    )

    # Clean up 'product' column by removing prefix and suffix
    df_premodel_usable_proba["product"] = df_premodel_usable_proba["product"].apply(
        lambda x: re.match(regex_probability_product, x).group(2)
    )


    # Convert probabilities to percentages
    df_premodel_usable_proba["purchase_probability"] *= 100

    # Apply lead scoring
    df_premodel_usable_proba["lead_scoring"] = df_premodel_usable_proba["purchase_probability"].apply(get_lead_scoring)

    # Pivot product table
    df_premodel_usable_product = df_premodel_usable_raw_product.melt(
        id_vars=["sPerson"], value_name="has_product", var_name="product"
    )

    # Clean up 'product' column by removing prefix
    df_premodel_usable_product["product"] = df_premodel_usable_product["product"].apply(
        lambda x: re.match(regex_product, x).group(1)
    )

    # Merge probability and product tables
    df_premodel_usable = df_premodel_usable_proba.merge(
        df_premodel_usable_product, on=["sPerson", "product"], how="inner"
    )

    # Filter out policies already purchased
    df_premodel_usable = df_premodel_usable.query("has_product == 0")

    return df_premodel_usable


def get_positive_neg_factors():
    """
    Obtener una sola tabla, a partir de muchas, que contenga los fac pos y nega
    """
    enriched_regex = re.compile(r"df_enriched_db_Product_(.*)_1\.0")
    df_to_concat = []

    enriched_dir = Path("./data/df_enriched_db_{ProductName}_10")

    # Make sure that this is a folder
    assert enriched_dir.is_dir()

    for file in enriched_dir.iterdir():
        with file.open() as f:
            # Get the file name
            file_name = os.path.basename(file)
            # Extract product from file name

            product_name = enriched_regex.match(file_name).group(1)

            # Load the dataframe
            df_product_factors = pd.read_csv(
                f,
                # Only keep needed columns
                usecols=[
                    "sPerson",
                    "list_driver_names",
                    "list_driver_values",
                    "list_barrier_names",
                    "list_barrier_values",
                    "_base_values",
                ],
            )
            df_product_factors["product_name"] = product_name
            df_to_concat.append(df_product_factors)

    # Append to main dataframe
    df_factors = pd.concat(df_to_concat)

    return df_factors


def add_actual_values_to_factors(df_factors: pd.DataFrame):
    """
    Add columns that have the actual values of the factors
    (not the importance)
    """
    # Only one csv is needed because all of the rest have the same columns and vals
    df_factors_sample = read_csv(
        "df_enriched_db_{ProductName}_10/df_enriched_db_Product_Vida_1.0"
    )

    df_factors_sample = df_factors_sample.iloc[:, 0:48]

    # Merge with df_factors
    df_factors_with_vals = df_factors.merge(
        left_on="sPerson",
        right=df_factors_sample,
        right_on="sPerson",
        how="inner",
    )

    return df_factors_with_vals


def get_person_data():
    """
    Get the person data to add to the factors table
    """

    check_null_cols = [
        "Ingresos",
        "ComercialAsignado",
        "Sexo",
        "YearsSinceCampaign",
        "Edad",
        "UltimoContacto",
    ]

    # We need just a single CSV
    df_enriched_sample = read_csv(
        "df_enriched_db_{ProductName}_10/df_enriched_db_Product_Vida_1.0",
        # Todos los CSVs df_enriched_db_{ProductName}_10, tienen los mismos valores en estas columnas
        # por lo tanto basta con leer una y duplicar esta info en df_factors
        usecols=[
            "sPerson",
        ]
        + check_null_cols,
        dtype={"ResultHistoricoCampañas": "str"},
    )

    # Dropear filas que tienen la Edad, ..., Tom. Col. Salud como NaN
    df_enriched_sample_final = df_enriched_sample[
        ~df_enriched_sample[check_null_cols].isnull().all(axis=1)
    ]

    # Quitar la unica persona que tiene la Edad en null
    df_enriched_sample_final = df_enriched_sample_final[
        ~df_enriched_sample_final["Edad"].isna()
    ]

    return df_enriched_sample_final


def drop_original_factors(df_premodel_factors):
    # Drop original factors Since the drivers are transformed,
    # to be displayed in the dashboard.
    df_premodel_factors.drop(
        columns=[
            "list_driver_names_y",
            "list_driver_values_y",
            "list_barrier_names_y",
            "list_barrier_values_y",
        ],
        inplace=True,
    )


def get_predicted_opportunities():
    """
    Retrieve a table of predicted opportunities for display on shimoku.io.

    This function performs several steps to prepare the data:
    1. Fetches pre-model usable predicted data.
    2. Retrieves personal data of individuals.
    3. Obtains factors with positive and negative impacts.
    4. Merges actual values into these factors.
    5. Combines this information with personal data.
    6. Merges the above with pre-model predictions.
    7. Processes and formats the impact factors.
    8. Drops original factor columns.
    9. Renames columns for consistency.
    10. Exports the final dataframe to a CSV file.

    Returns:
        None: The function outputs a CSV file and does not return any value.
    """
    # Fetch pre-model usable predicted data
    df_premodel_usable = get_usable_premodel_predicted()

    # Retrieve personal data
    df_person_data = get_person_data()

    # Obtain factors with positive and negative impacts
    df_factors = get_positive_neg_factors()
    df_factors_with_vals = add_actual_values_to_factors(df_factors)

    # Merge personal information with factor data
    df_factors_person = df_factors_with_vals.merge(
        df_person_data[["sPerson"]],
        on="sPerson",
        how="inner"
    )

    # Combine factor and personal information with pre-model predictions
    df_premodel_factors = df_premodel_usable.merge(
        df_factors_person,
        left_on=["sPerson", "product"],
        right_on=["sPerson", "product_name"],
        how="inner"
    )

    # Process and format positive impact factors
    df_premodel_factors["positive_impact_factors"] = df_premodel_factors.apply(
        factors_to_string,
        axis=1,
        names_col="list_driver_names_y",
        values_col="list_driver_values_y"
    )

    # Process and format negative impact factors
    df_premodel_factors["negative_impact_factors"] = df_premodel_factors.apply(
        factors_to_string,
        axis=1,
        names_col="list_barrier_names_y",
        values_col="list_barrier_values_y"
    )

    # Drop original factor columns
    drop_original_factors(df_premodel_factors)

    # Rename columns for consistency
    df_premodel_factors.rename(columns={"product": "product_name"}, inplace=True)

    # Export the final dataframe to a CSV file
    to_csv(df_premodel_factors, "table_product_recommender")
