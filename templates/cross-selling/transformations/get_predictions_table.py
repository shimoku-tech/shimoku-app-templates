# Core python libraries
import re
import json
import os
from pathlib import Path

# Local
from utils.utils import (
    get_prod_category, read_csv, to_csv,
    search_string
)

# Third party
import pandas as pd
import numpy as np

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

    print(row)
    print(row[names_col])
    print(row[values_col])

    factor_list = eval(
        row[names_col]
    )[:3]

    factor_value_list = eval(
        row[values_col]
    )[:3]

    filtered_meta_list = []


    for idx, val in enumerate(factor_value_list):
        round_val = round(val*100)
        if round_val >= 1 or round_val <= -1:
            filtered_meta_list.append({"idx": idx, "val": round_val})


    filtered_factor_values = [
        f"{meta['val']}%" for meta in filtered_meta_list
    ]

    filtered_factor_list = [
        factor_list[meta['idx']] for meta in filtered_meta_list
    ]

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

    assert(len(filtered_factor_list) == len(filtered_factor_values))

    pre_joined = [
        f"{factor} {filtered_factor_values[idx]} {filtered_factor_per_val[idx]}" for idx, factor in enumerate(filtered_factor_list)
    ]

    return ", ".join(pre_joined)

def factors_to_dict(row: pd.Series, names_col: str, values_col: str, acronym: str):
    """
    Convert the encoded string list to
    actual readable values
    """
    # DONE: multiplicar por 100, sin decimales
    # DONE: Quitar los dos puntos
    factor_list = eval(
        row[names_col]
    )[:3]

    factor_weight_list = eval(
        row[values_col]
    )[:3]

    filtered_meta_list = []


    # Only extract those
    for idx, val in enumerate(factor_weight_list):
        round_val = round(val*100)
        if round_val >= 1 or round_val <= -1:
            filtered_meta_list.append({"idx": idx, "val": round_val})


    filtered_factor_weights = [
        meta['val'] for meta in filtered_meta_list
    ]

    filtered_factor_list = [
        factor_list[meta['idx']] for meta in filtered_meta_list
    ]

    # Grab actual values
    filtered_factor_values = []
    for factor in filtered_factor_list:
        filtered_factor_values.append(row[factor])

    assert(len(filtered_factor_list) == len(filtered_factor_weights))
    assert(len(filtered_factor_values) == len(filtered_factor_list))

    factor_dict = { }
    for i in range(len(filtered_factor_weights)):
        factor_dict[f"{acronym}_{i}_name"] = filtered_factor_list[i]
        factor_dict[f"{acronym}_{i}_weight_pct"] = filtered_factor_weights[i]
        factor_dict[f"{acronym}_{i}_value"] = filtered_factor_values[i]



    return factor_dict

def factors_to_col(df_factors):
    """
    Make a dataframe with barriers and drivers in columns
    """

    df_dict = []

    # df_test = df_factors.head(50)

    # RAM Expensive
    for idx, row in df_factors.iterrows():
        factors_row = {
            "sPerson": row["sPerson"],
            "product_name": row["product_name"],
        }

        factors_dict_pos = factors_to_dict(
            row,
            names_col='list_driver_names',
            values_col='list_driver_values',
            acronym="driver",
        )
        factors_dict_neg = factors_to_dict(
            row,
            names_col='list_barrier_names',
            values_col='list_barrier_values',
            acronym="barrier"
        )

        # Add the 12 factors column
        factors_row.update(factors_dict_pos)
        factors_row.update(factors_dict_neg)


        df_dict.append(factors_row)

    # Build dataframe
    df_factors_split = pd.DataFrame(data=df_dict)

    return df_factors_split

def get_usable_premodel_predicted() -> pd.DataFrame:
    """
    Transform df_premodel_predicted from high column number
    to low column number
    """
    # La predicción de compra/no compra y probabilidad de compra/no compra
    df_premodel_predicted = read_csv('df_premodel_predicted')


    # Obtener el nombre de todas las columnas de predicción de probabilidad de compra
    regex_probability_Product = r"^(probability_Product_)(.*)(_1\.0)$"
    col_pred_prob = search_string(
        regex_probability_Product,
        df_premodel_predicted.columns
    )

    # Product_{NombredelProducto}
    regex_product = r'^Product_(.*)'
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
    df_premodel_usable_raw_product = df_premodel_predicted[["sPerson"] + cold_pred_product_buy]

    print(df_premodel_usable_raw_proba.head())


    # Ahora tratamos de pivotar la tabla
    df_premodel_usable_proba = df_premodel_usable_raw_proba.melt(
        id_vars=["sPerson"], value_name="probabilidad_compra",
        var_name="product",
    )

    print(df_premodel_usable_proba.head())


    # Se descarta el prefijo probability_ y sufijo 1.0
    df_premodel_usable_proba['product'] = df_premodel_usable_proba['product'].apply(
        lambda x: re.match(regex_probability_Product, x).group(2)
    )

    # Convertir probabilidades a porcentajes redondeado a 1 decimal
    df_premodel_usable_proba['probabilidad_compra'] = df_premodel_usable_proba['probabilidad_compra'].apply(lambda x: x*100)

    # Se crea la columna calculada lead_scoring
    # High (+70%), Medium (+50%), Low (-50%)
    def get_lead_scoring(probability_percentage):
        if probability_percentage < 50:
            return "Low"
        if probability_percentage >= 50 and probability_percentage < 75:
            return 'Medium'
        if probability_percentage >= 75:
            return "High"

    df_premodel_usable_proba['lead_scoring'] = df_premodel_usable_proba['probabilidad_compra'].apply(get_lead_scoring)

    # Pivotar tabla para que solo tenga tres columnas
    df_premodel_usable_product = df_premodel_usable_raw_product.melt(
        id_vars=["sPerson"], value_name="tiene_producto",
        var_name="product",
    )

    # Se descarta el prefijo Product_
    df_premodel_usable_product['product'] = df_premodel_usable_product['product'].apply(
        lambda x: re.match(regex_product, x).group(1)
    )

    # Se unen las tablas de probabilidades mas compra de producto
    df_premodel_usable = df_premodel_usable_proba.merge(
        right=df_premodel_usable_product,
        right_on=['sPerson','product'], left_on=['sPerson','product'],
        how='inner',
    )

    # Lista de nombres exactos de productos mutuamente excluyentes
    exclude_prod = {'Adeslas Vital', 'Adeslas Complerta','Mèdica ASC','Accidents Vida ASC', 'Accidents Invalidesa permanent i absoluta ASC', 'Hospital Barcelona', 'Accidents Vida ASC Circulació', 'CorreduriaSalud'}

    for product in exclude_prod:
        # Obtener todos los sPerson en donde product_name este en la lista y tiene_producto=1
        df_step1 = df_premodel_usable.query(f"product == '{product}' & tiene_producto==1")

        # Products to search for
        prod_search = exclude_prod - {product}

        df_step2 = df_premodel_usable[
            (df_premodel_usable["product"].isin(prod_search)) &
            (df_premodel_usable["tiene_producto"] == 0)
        ]

        # Obtener aquellos sPerson que tienen productos mutuamente excluyentes
        df_step3 = df_step2[df_step2["sPerson"].isin(df_step1["sPerson"].unique())]

        # Si sPerson aparece en df_step1 y df_step2 filter out of df_premodel_usable
        df_premodel_usable = df_premodel_usable[~df_premodel_usable["sPerson"].isin(df_step3["sPerson"].unique())]


    # Excluir las polizas que ya ha comprado la persona
    df_premodel_usable = df_premodel_usable.query(
        "tiene_producto == 0"
    )

    # This should be empty dataframe
    # assert(
    #     df_premodel_usable[df_premodel_usable["sPerson"].isin([11741, 16118, 16359, 17626, 17720, 18160, 18265, 18855, 18898,])].empty
    # )

    # Categorizar productos por Muta o correduria
    df_premodel_usable['product_category'] = df_premodel_usable['product'].apply(get_prod_category)

    return df_premodel_usable

def get_positive_neg_factors():
    """
    Obtener una sola tabla, a partir de muchas, que contenga los fac pos y nega
    """
    enriched_regex = re.compile(r"df_enriched_db_Product_(.*)_1\.0")
    df_to_concat = []

    enriched_dir = Path('./data/df_enriched_db_{ProductName}_10')

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
                    'sPerson',
                    'list_driver_names', 'list_driver_values',
                    'list_barrier_names', 'list_barrier_values',
                    '_base_values',
                ]
            )
            df_product_factors['product_name'] = product_name
            df_to_concat.append(df_product_factors)

    # Append to main dataframe
    df_factors=pd.concat(df_to_concat)

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
            'AñosPasivoPlanplanes_1': 'Int8',
            'AñosPasivoPlanplanes_10': 'Int8',
            'AñosPasivoPlanplanes_14': 'Int8',
            'AñosPasivoPlanplanes_15': 'Int8',
            'AñosPasivoPlanplanes_17': 'Int8',
            'AñosPasivoPlanplanes_19': 'Int8',
            'AñosPasivoPlanplanes_2': 'Int8',
            'AñosPasivoPlanplanes_22': 'Int8',
            'AñosPasivoPlanplanes_28': 'Int8',
            'AñosPasivoPlanplanes_29': 'Int8',
            'AñosPasivoPlanplanes_3': 'Int8',
            'AñosPasivoPlanplanes_30': 'Int8',
            'AñosPasivoPlanplanes_31': 'Int8',
            'AñosPasivoPlanplanes_4': 'Int8',
            'AñosPasivoPlanplanes_6': 'Int8',
            'AñosPasivoPlanplanes_7': 'Int8',
            'AñosPasivoPlanplanes_9': 'Int8',
            'ClientPreferent': 'Int8',
            'DretsMutualistaSuspesos': 'Int8',
            'Edad': 'Int8',
            'HasBusinessAdvisor': 'Int8',
            'HasInvestmentAdvisor': 'Int8',
            'IdSex': 'Int8',
            'ProvinceId_ESP08': 'Int8',
            'ProvinceId_ESP17': 'Int8',
            'ProvinceId_ESP25': 'Int8',
            'ProvinceId_ESP28': 'Int8',
            'ProvinceId_ESP43': 'Int8',
            'ProvinceId_ESP46': 'Int8',
            'ProvinceId_Otra': 'Int8',
            'ResidenciaFiscalEsp': 'Int8',
            'RiesgoPBC': 'Int8',
            'SociMutualista': 'Int8',
            'YearsSinceCampaign': 'Int8',
            'YearsSinceMutuaRegisterDate': 'Int8',
            'numeroAseguradosCorreduriaSalud': 'Int8',
            'numeroModalidadesCorreduriaRC': 'Int8',
            'numeroModalidadesCorreduriaSalud': 'Int8'
        }
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
    assert(df_factors.shape[0] == df_factors_with_vals.shape[0])

    return df_factors_with_vals

def get_person_data():
    """
    Add person
    """
    check_null_cols = [
        'Edad', 'Ingresos', 'IdSex', 'HasInvestmentAdvisor',
        'HasBusinessAdvisor', 'SociMutualista', 'DretsMutualistaSuspesos',
        'RiesgoPBC',
        'ClientPreferent',
        'Tom. Plans', 'Tom. UL', 'Tom. Corr. Ind', 'Tom. Mutua',
        'Tom. Col. RC', 'Tom. Col. Salud',
    ]


    check_null_cols = [
        'Edad', 'Ingresos', 'IdSex', 'HasInvestmentAdvisor',
        'HasBusinessAdvisor', 'SociMutualista', 'DretsMutualistaSuspesos',
        'RiesgoPBC',
        'ClientPreferent',
        'Tom. Plans', 'Tom. UL', 'Tom. Corr. Ind', 'Tom. Mutua',
        'Tom. Col. RC', 'Tom. Col. Salud',
    ]
    check_null_cols = [
    "Ingresos", "ComercialAsignado","IdSex","YearsSinceCampaign","Edad","UltimoContacto"
    ]

    
    # We need just a single CSV
    df_enriched_sample = read_csv(
        "df_enriched_db_{ProductName}_10/df_enriched_db_Product_Vida_1.0",
        # Todos los CSVs df_enriched_db_{ProductName}_10, tienen los mismos valores en estas columnas
        # por lo tanto basta con leer una y duplicar esta info en df_factors
        usecols=['sPerson',] + check_null_cols,
        dtype={"ResultHistoricoCampañas": "str"}
    )

    # Dropear filas que tienen la Edad, ..., Tom. Col. Salud como NaN
    df_enriched_sample_final = df_enriched_sample[~df_enriched_sample[check_null_cols].isnull().all(axis=1)]

    # Quitar la unica persona que tiene la Edad en null
    df_enriched_sample_final = df_enriched_sample_final[~df_enriched_sample_final["Edad"].isna()]

    # # Add metadata
    # # Crear columna 'etapa_vida'
    # def get_etapa_vida(age):
    #     if age >= 0 and age < 35:
    #         return "Joves"
    #     if age >= 35 and age < 45:
    #         return "Maduros I"
    #     if age >= 45 and age < 55:
    #         return "Maduros II"
    #     if age >= 55 and age < 65:
    #         return "Maduros III y Mayores"
    #     if age >= 65 and age < 130:
    #         return "Edat de Jubilación"

    # df_enriched_sample_final["etapa_vida"] = df_enriched_sample_final["Edad"].apply(get_etapa_vida)

    return df_enriched_sample_final

def get_premodel_factors() -> pd.DataFrame:
    """
    This is a common step between the
    get_predictions_table_{complex, simple} tables
    """

    df_premodel_usable = get_usable_premodel_predicted()
    df_person_data = get_person_data()
    df_factors = get_positive_neg_factors() # RAM EXPENSIVE 1.2 GB
    df_factors_with_vals = add_actual_values_to_factors(df_factors) # RAM EXPENSIVE 1.2 GB


    # Añadir info de personas a la tabla de factores
    df_factors_person = df_factors_with_vals.merge(
        on="sPerson",
        #right=df_person_data[["sPerson", "etapa_vida"]],
        right=df_person_data[["sPerson"]],
        how="inner",
    )

    # Unir info de factores, personas, con las predicciones de compra
    df_premodel_factors = df_premodel_usable.merge(
        left_on=["sPerson","product"],
        right=df_factors_person,
        right_on=["sPerson", "product_name"],
        how="inner",
    )
    return df_premodel_factors

def drop_original_factors(df_premodel_factors):

    # Drop original factors Since the drivers are transformed,
    # to be displayed in the dashboard.
    print(df_premodel_factors.columns)
    df_premodel_factors.drop(
        columns=["list_driver_names_y", "list_driver_values_y", "list_barrier_names_y", "list_barrier_values_y"],# + ['ResultHistoricoCampañas', 'Tom. Plans', 'Tom. UL', 'ActividadEconomica', 'Tom. Corr. Ind', 'Tom. Mutua', 'Tom. Col. RC', 'Ingresos', 'Tom. Col. Salud', 'HasInvestmentAdvisor', 'ProvinceId_ESP28', 'ProvinceId_ESP08', 'SociMutualista', 'ProvinceId_ESP43', 'HasBusinessAdvisor', 'AñosPasivoPlanplanes_22', 'ResidenciaFiscalEsp', 'ProvinceId_ESP46', 'ProvinceId_Otra', 'DretsMutualistaSuspesos', 'RiesgoPBC', 'ProvinceId_ESP17', 'IdSex', 'ClientPreferent', 'ProvinceId_ESP25', 'numeroModalidadesCorreduriaRC', 'numeroAseguradosCorreduriaSalud', 'YearsSinceCampaign', 'AñosPasivoPlanplanes_6', 'AñosPasivoPlanplanes_10', 'YearsSinceMutuaRegisterDate', 'numeroModalidadesCorreduriaSalud', 'AñosPasivoPlanplanes_4', 'AñosPasivoPlanplanes_3', 'AñosPasivoPlanplanes_14', 'AñosPasivoPlanplanes_19', 'AñosPasivoPlanplanes_1', 'AñosPasivoPlanplanes_30', 'AñosPasivoPlanplanes_9', 'AñosPasivoPlanplanes_15', 'AñosPasivoPlanplanes_29', 'AñosPasivoPlanplanes_28', 'AñosPasivoPlanplanes_7', 'AñosPasivoPlanplanes_2', 'AñosPasivoPlanplanes_31', 'AñosPasivoPlanplanes_17',],
        inplace=True,
    )

def get_predictions_table_simple():
    """
    Get the predictions table that it's going to be displayed
    in shimoku.io
    """

    df_premodel_factors = get_premodel_factors()

    # Format factors (RAM EXPENSIVE 3GB)

    print(df_premodel_factors.head())
    
    
    df_premodel_factors['positive_impact_factors'] = df_premodel_factors.apply(factors_to_string, axis=1, names_col='list_driver_names_y', values_col='list_driver_values_y')

    df_premodel_factors['negative_impact_factors'] = df_premodel_factors.apply(factors_to_string, axis=1, names_col='list_barrier_names_y', values_col='list_barrier_values_y')


    # Drop original factors Since the drivers are transformed,
    # to be displayed in the dashboard.

    drop_original_factors(df_premodel_factors)

    df_premodel_factors.rename(columns={'product': 'product_name'}, inplace=True)

    to_csv(
        df_premodel_factors,
        "table_product_recommender"
    )

def get_predictions_table_complex():

    df_premodel_factors = get_premodel_factors()

    # This operation is very expensive in RAM and SLOW
    df_factors_split = factors_to_col(df_premodel_factors)

    table_product_recommender = df_premodel_factors.merge(
        right=df_factors_split,
        left_on=["sPerson","product"],
        right_on=["sPerson", "product_name"],
        how="inner",
    )

    # Drop not needed columns for the final result
    drop_original_factors(table_product_recommender)
    table_product_recommender.drop(columns=["product_name_x", "product_name_y"], inplace=True)

    # Rename cols
    table_product_recommender.rename(
        columns={'product': 'product_name'},
        inplace=True
    )

    to_csv(
        table_product_recommender,
        "table_product_recommender_split"
    )
if __name__ == "__main__":
    # Never run the two functions below at the same time
    # You might run out of RAM

    get_predictions_table_simple()
    # get_predictions_table_complex()
