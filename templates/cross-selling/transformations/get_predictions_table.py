import re
import json
import os
from pathlib import Path
import pandas as pd
import numpy as np

from utils.utils import (read_csv, 
                         to_csv, 
                         search_string,
                         factors_to_string)


def get_usable_premodel_predicted() -> pd.DataFrame:
    """
    Transform df_premodel_predicted from high column number
    to low column number
    """
    # La predicción de compra/no compra y probabilidad de compra/no compra
    df_premodel_predicted = read_csv("df_premodel_predicted")

    # Obtener el nombre de todas las columnas de predicción de probabilidad de compra
    regex_probability_Product = r"^(probability_Product_)(.*)(_1\.0)$"
    col_pred_prob = search_string(
        regex_probability_Product, df_premodel_predicted.columns
    )

    # Product_{NombredelProducto}
    regex_product = r"^Product_(.*)"
    cold_pred_product_buy = search_string(
        regex_product,
        df_premodel_predicted.columns,
    )
    # Obtener un dataframe con el id de las personas más todas las columnas de predicción
    # de probabilidad de compra
    df_premodel_usable_raw_proba = df_premodel_predicted[["sPerson"] + col_pred_prob]

    # Obtener un dataframe con el id de las personas más todas las columnas
    # del valor real de si ha comprado un producto.
    # Esta tabla se necesita ya que el melt no permite tener varias columnas con valores.
    df_premodel_usable_raw_product = df_premodel_predicted[
        ["sPerson"] + cold_pred_product_buy
    ]

    # Ahora tratamos de pivotar la tabla
    df_premodel_usable_proba = df_premodel_usable_raw_proba.melt(
        id_vars=["sPerson"],
        value_name="probabilidad_compra",
        var_name="product",
    )

    # Se descarta el prefijo probability_ y sufijo 1.0
    df_premodel_usable_proba["product"] = df_premodel_usable_proba["product"].apply(
        lambda x: re.match(regex_probability_Product, x).group(2)
    )

    # Convertir probabilidades a porcentajes redondeado a 1 decimal
    df_premodel_usable_proba["probabilidad_compra"] = df_premodel_usable_proba[
        "probabilidad_compra"
    ].apply(lambda x: x * 100)

    # Se crea la columna calculada lead_scoring
    # High (+70%), Medium (+50%), Low (-50%)
    def get_lead_scoring(probability_percentage):
        if probability_percentage < 50:
            return "Low"
        if probability_percentage >= 50 and probability_percentage < 75:
            return "Medium"
        if probability_percentage >= 75:
            return "High"

    df_premodel_usable_proba["lead_scoring"] = df_premodel_usable_proba[
        "probabilidad_compra"
    ].apply(get_lead_scoring)

    # Pivotar tabla para que solo tenga tres columnas
    df_premodel_usable_product = df_premodel_usable_raw_product.melt(
        id_vars=["sPerson"],
        value_name="tiene_producto",
        var_name="product",
    )

    # Se descarta el prefijo Product_
    df_premodel_usable_product["product"] = df_premodel_usable_product["product"].apply(
        lambda x: re.match(regex_product, x).group(1)
    )

    # Se unen las tablas de probabilidades mas compra de producto
    df_premodel_usable = df_premodel_usable_proba.merge(
        right=df_premodel_usable_product,
        right_on=["sPerson", "product"],
        left_on=["sPerson", "product"],
        how="inner",
    )

    # Lista de nombres exactos de productos mutuamente excluyentes
    exclude_prod = {
        "Adeslas Vital",
        "Adeslas Complerta",
        "Mèdica ASC",
        "Accidents Vida ASC",
        "Accidents Invalidesa permanent i absoluta ASC",
        "Hospital Barcelona",
        "Accidents Vida ASC Circulació",
        "CorreduriaSalud",
    }

    for product in exclude_prod:
        # Obtener todos los sPerson en donde product_name este en la lista y tiene_producto=1
        df_step1 = df_premodel_usable.query(
            f"product == '{product}' & tiene_producto==1"
        )

        # Products to search for
        prod_search = exclude_prod - {product}

        df_step2 = df_premodel_usable[
            (df_premodel_usable["product"].isin(prod_search))
            & (df_premodel_usable["tiene_producto"] == 0)
        ]

        # Obtener aquellos sPerson que tienen productos mutuamente excluyentes
        df_step3 = df_step2[df_step2["sPerson"].isin(df_step1["sPerson"].unique())]

        # Si sPerson aparece en df_step1 y df_step2 filter out of df_premodel_usable
        df_premodel_usable = df_premodel_usable[
            ~df_premodel_usable["sPerson"].isin(df_step3["sPerson"].unique())
        ]

    # Excluir las polizas que ya ha comprado la persona
    df_premodel_usable = df_premodel_usable.query("tiene_producto == 0")

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
        "df_enriched_db_{ProductName}_10/df_enriched_db_Product_Vida_1.0",
        dtype={
            "ResultHistoricoCampañas": "object",
            "AñosPasivoPlanplanes_1": "Int8",
            "AñosPasivoPlanplanes_10": "Int8",
            "AñosPasivoPlanplanes_14": "Int8",
            "AñosPasivoPlanplanes_15": "Int8",
            "AñosPasivoPlanplanes_17": "Int8",
            "AñosPasivoPlanplanes_19": "Int8",
            "AñosPasivoPlanplanes_2": "Int8",
            "AñosPasivoPlanplanes_22": "Int8",
            "AñosPasivoPlanplanes_28": "Int8",
            "AñosPasivoPlanplanes_29": "Int8",
            "AñosPasivoPlanplanes_3": "Int8",
            "AñosPasivoPlanplanes_30": "Int8",
            "AñosPasivoPlanplanes_31": "Int8",
            "AñosPasivoPlanplanes_4": "Int8",
            "AñosPasivoPlanplanes_6": "Int8",
            "AñosPasivoPlanplanes_7": "Int8",
            "AñosPasivoPlanplanes_9": "Int8",
            "ClientPreferent": "Int8",
            "DretsMutualistaSuspesos": "Int8",
            "Edad": "Int8",
            "HasBusinessAdvisor": "Int8",
            "HasInvestmentAdvisor": "Int8",
            "IdSex": "Int8",
            "ProvinceId_ESP08": "Int8",
            "ProvinceId_ESP17": "Int8",
            "ProvinceId_ESP25": "Int8",
            "ProvinceId_ESP28": "Int8",
            "ProvinceId_ESP43": "Int8",
            "ProvinceId_ESP46": "Int8",
            "ProvinceId_Otra": "Int8",
            "ResidenciaFiscalEsp": "Int8",
            "RiesgoPBC": "Int8",
            "SociMutualista": "Int8",
            "YearsSinceCampaign": "Int8",
            "YearsSinceMutuaRegisterDate": "Int8",
            "numeroAseguradosCorreduriaSalud": "Int8",
            "numeroModalidadesCorreduriaRC": "Int8",
            "numeroModalidadesCorreduriaSalud": "Int8",
        },
    )
    df_factors_sample = df_factors_sample.iloc[:, 0:48]

    # Merge with df_factors
    df_factors_with_vals = df_factors.merge(
        left_on="sPerson",
        right=df_factors_sample,
        right_on="sPerson",
        how="inner",
    )

    # No rows should have been lost
    assert df_factors.shape[0] == df_factors_with_vals.shape[0]

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


def get_premodel_factors() -> pd.DataFrame:
    """
    This is a common step between the
    get_predictions_table_{complex, simple} tables
    """

    df_premodel_usable = get_usable_premodel_predicted()
    df_person_data = get_person_data()
    df_factors = get_positive_neg_factors() 
    df_factors_with_vals = add_actual_values_to_factors(df_factors) 

    # Añadir info de personas a la tabla de factores
    df_factors_person = df_factors_with_vals.merge(
        on="sPerson",
        # right=df_person_data[["sPerson", "etapa_vida"]],
        right=df_person_data[["sPerson"]],
        how="inner",
    )

    # Unir info de factores, personas, con las predicciones de compra
    df_premodel_factors = df_premodel_usable.merge(
        left_on=["sPerson", "product"],
        right=df_factors_person,
        right_on=["sPerson", "product_name"],
        how="inner",
    )
    return df_premodel_factors


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


def get_predictions_table():
    """
    Get the predictions table that it's going to be displayed
    in shimoku.io
    """

    df_premodel_factors = get_premodel_factors()

    df_premodel_factors["positive_impact_factors"] = df_premodel_factors.apply(
        factors_to_string,
        axis=1,
        names_col="list_driver_names_y",
        values_col="list_driver_values_y",
    )

    df_premodel_factors["negative_impact_factors"] = df_premodel_factors.apply(
        factors_to_string,
        axis=1,
        names_col="list_barrier_names_y",
        values_col="list_barrier_values_y",
    )

    # Drop original factors Since the drivers are transformed,
    # to be displayed in the dashboard.

    drop_original_factors(df_premodel_factors)

    df_premodel_factors.rename(columns={"product": "product_name"}, inplace=True)

    to_csv(df_premodel_factors, "table_product_recommender")