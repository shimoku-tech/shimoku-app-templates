# Core python libraries
from os import getenv
from typing import Callable, Iterable

# Local modules
from utils.utils import DFs, format_number, read_json
from utils.components import (
    create_title_name_head, info_modal_predicted,
    info_modal_ai_insights,
    modal_partial_dependence,
)

# Third party
from shimoku_api_python import Client
import numpy as np
import pandas as pd

environment = getenv("ENVIROMENT", "develop")
develop = environment == "develop"
develop_mutua = environment == "develop_mutua"

# Used by predictions_page and hidden_indicators_page

def plot_indicator_list(shimoku: Client, order: int, indicator_product_data):
    """
    Plot a list of HIGH indicators
    """

    next_order = order
    for prod_cat in indicator_product_data.keys():
        # Add title
        shimoku.plt.html(
            html=shimoku.html_components.create_h1_title(
                title="",
                subtitle=f"{prod_cat}",
            ),
            order=next_order
        )
        next_order+=1

        # Plot all products in a product category
        for idx, indicator_data in enumerate(indicator_product_data[prod_cat]):
            # Pop not needed key
            indicator_data.pop("percentage")

            # if indicator_data["title"] == "Otros productos":
            #     breakpoint()

            shimoku.plt.indicator(
                data=indicator_data,
                order=next_order,
                cols_size=3,
            )
            next_order+=1

    return next_order

def get_indicators_by_bussniess(dfs: DFs, board: dict):
    """
    Gets the indicators by the Mutua Business or
    Correduria
    """
    def make_indicator(product_name: str, value_lead_scoring, total_high: int, extra_options={}):
        """
        Construct indicator dict for the indicator section
        """
        percentage = (value_lead_scoring / total_high ) * 100
        perc_formatted = round(percentage, ndigits=0)

        return {
            'title': f"{product_name}",
            'value': f"{format_number(value_lead_scoring)} ({'{:.0f}'.format(perc_formatted)} %)",
            'color': 'success',
            # Metadata for sorting
            'percentage': perc_formatted,
            # Common indicator settings
            'align': 'center',
            'variant': 'topColor',
            "align": "left",
            **extra_options,
        }

    # print(lead_scoring_per_cat['lead_scoring'].index.levels)
    # - Product category is the first level of the index
    # - The second level contains the product names

    # Total rows High probability by product category
    high_scoring_per_cat = dfs.df_recommender_table.query(f"lead_scoring=='High'").groupby(by="product_category").agg({'lead_scoring': 'count'})

    # Count number of lead_scoring categories by product and product_name
    lead_scoring_per_cat = dfs.df_recommender_table.query(f"lead_scoring=='High'").groupby(by=["product_category", "product_name"]).agg({'lead_scoring': 'count'})


    # Build indicators per product
    indicators_summary = {}
    hidden_indicators = {}

    # Iterate over unique products, then get the count of the high lead scoring
    for product_category in lead_scoring_per_cat['lead_scoring'].index.levels[0]:

        total_high = high_scoring_per_cat['lead_scoring'][product_category]

        indicators_summary[product_category] = []
        hidden_indicators[product_category] = []

        # Used only after the third product
        scoring_accumulator = 0

        # Sort with in the dataframe
        product_category_group = lead_scoring_per_cat['lead_scoring'][product_category].sort_values(ascending=False)

        high_group_size = len(product_category_group)

        for product_count, product_name in enumerate(product_category_group.index.values):

            value_lead_scoring = product_category_group[product_name]

            extra_options = {}
            # print(product_count, product_name)

            # Only The first three products are allowed to be displayed,
            # the rest are grouped into one product called 'Other products'
            # And saved to another list to be plotted in a hidden path
            if product_count > 2:
                scoring_accumulator += value_lead_scoring
                hidden_indicators[product_category].append(
                    make_indicator(
                        product_name,
                        value_lead_scoring,
                        total_high,
                    )
                )

                # If it is the last product
                if product_count == high_group_size - 1:

                    # Override the product_name
                    product_name = "Otros productos"

                    # Override the scoring_accumulator
                    value_lead_scoring = scoring_accumulator

                    # Add a link to the indicator
                    extra_options={
                        "targetPath": f"{board['id']}/hidden-indicators",
                    }

                else:
                    # Skip the iteration so we don't create a new entry in the
                    # indicators_summary[product_category] array
                    continue

            # Make indicator data
            indicators_summary[product_category].append(
                make_indicator(
                    product_name,
                    value_lead_scoring,
                    total_high,
                    extra_options=extra_options,
                )
            )

    return {
        "indicators_summary": indicators_summary,
        "hidden_indicators": hidden_indicators,
    }

def hidden_indicators_page(shimoku: Client, indicator_product_data):
    """
    Detailed page of all the product indicators
    that fall into the 'Other products' category
    """
    order=0
    menu_path="Hidden indicators"
    shimoku.set_menu_path(name=menu_path)

    shimoku.plt.html(
        html=shimoku.html_components.create_h1_title(
            title="Otros productos",
            subtitle="Indicadores Lead Scoring HIGH, de 'otros productos'",
        ),
        order=order,
    )
    order+=1

    order+=plot_indicator_list(shimoku, order, indicator_product_data=indicator_product_data)

    # Hide the menu path
    shimoku.menu_paths.update_menu_path(
        name=menu_path,
        hide_path=True,
    )

    shimoku.pop_out_of_menu_path()

def info_btn(shimoku: Client, order: int, modal_html_fn: Callable[[], str], modal_name="info_modal"):

    next_order=order
    shimoku.plt.modal_button(
        label="Info",
        order=next_order,
        modal=modal_name,
        cols_size=1,
        # push to the right
        padding="0, 0, 0, 11",
    )
    next_order+=1

    # Begin modal content
    shimoku.plt.set_modal(modal_name=modal_name)
    modal_order = 0
    shimoku.plt.html(
        order=modal_order,
        html=modal_html_fn(),
    )

    # End Modal content
    shimoku.plt.pop_out_of_modal()
    return next_order

path_name_predicted_page = "Predicted opportunities"
def predictions_page(shimoku: Client, dfs: DFs, indicators_summary):
    shimoku.set_menu_path(name=path_name_predicted_page)

    order=0

    def headings(order: int):
        next_order=order

        shimoku.plt.html(
            html=create_title_name_head(
                title="Predictions",
                subtitle="Cross Selling",
            ),
            order=next_order,
        )

        next_order+=1
        return next_order

    def indicators(order: int):
        """
        Indicators section
        """
        next_order=order

        common_indicator_settings = {
            'align': 'center',
            'variant': 'topColor',
        }

        # Total rows High, Medium and LOW probability
        lead_scoring_agg = dfs.df_recommender_table.groupby(by="lead_scoring").agg({'lead_scoring': 'count'})

        # General indicators
        shimoku.plt.html(
            html=shimoku.html_components.create_h1_title(
                title="Total opportunities",
                subtitle="",
            ),
            order=next_order,
        )
        next_order+=1

        # description prefix
        desc_prefix="Oportunidades"
        next_order+=shimoku.plt.indicator(
            data=[
                {
                    'title': 'HIGH',
                    'value': format_number(lead_scoring_agg['lead_scoring']['High']),
                    'color': 'success',
                    'description': f"{desc_prefix} con una probabilidad de éxito mayor del 75%",
                    **common_indicator_settings,
                },
                {
                    'title': 'MEDIUM',
                    'value': format_number(lead_scoring_agg['lead_scoring']['Medium']),
                    'color': 'warning',
                    'description': f"{desc_prefix} con una probabilidad de éxito de entre el 50% y el 75%",
                    **common_indicator_settings,
                },
                {
                    'title': 'LOW',
                    'value': format_number(lead_scoring_agg['lead_scoring']['Low']),
                    'color': 'error',
                    'description': f"{desc_prefix} con una probabilidad de éxito menor del 50%",
                    # 'info': 'abc',
                    **common_indicator_settings,
                },
            ],
            order=next_order,
        )

        shimoku.plt.html(
            html=shimoku.html_components.create_h1_title(
                title="Product opportunities",
                subtitle="Basado en Lead Scoring High",
            ),
            order=next_order
        )
        next_order+=1

        # Indicators per product category

        next_order+=plot_indicator_list(
            shimoku,
            order=next_order,
            indicator_product_data=indicators_summary
        )

        return next_order

    def table_header(order: int):
        """
        Title and a Download button for the table
        """

        next_order = order

        # This title wasn't plotted in the previous
        # version of this dashboard but it would be nice
        # to add.

        # shimoku.plt.html(
        #     html=shimoku.html_components.create_h1_title(
        #         title="Product Recommender & Factors",
        #         subtitle="Recommendation per user",
        #     ),
        #     order=next_order,
        # )
        # next_order+=1

        next_order+=1
        return next_order

    def table_complex(order: int):
        """
        table with drivers and barriers in columns
        """
        shimoku.plt.change_current_tab("Compleja")
        next_order=order

        # String(2): sPerson, product_name
        # Numerical(2): probabilidad_compra, Edad
        renames = {
            "product_name": "Product",
            "probabilidad_compra": "Probability (%)",
            "lead_scoring": "Lead Scoring",
            "base_values": "Base value",
        }

        # TODO: add weight and value to actual values
        drivers_barriers = {
            # -----
            "driver_0_name": "Driver 1",
            "driver_0_weight_pct": "Driver 1 %",
            "driver_0_value": "Driver 1 value",
            #
            "driver_1_name": "Driver 2",
            "driver_1_weight_pct": "Driver 2 %",
            "driver_1_value": "Driver 2 value",
            #
            "driver_2_name": "Driver 3",
            "driver_2_weight_pct": "Driver 3 %",
            "driver_2_value": "Driver 3 value",

            # -----
            "barrier_0_name": "Barrier 1",
            "barrier_0_weight_pct": "Barrier 1 %",
            "barrier_0_value": "Barrier 1 value",

            "barrier_1_name": "Barrier 2",
            "barrier_1_weight_pct": "Barrier 2 %",
            "barrier_1_value": "Barrier 2 value",

            "barrier_2_name": "Barrier 3",
            "barrier_2_weight_pct": "Barrier 3 %",
            "barrier_2_value": "Barrier 3 value",
        }

        drop_cols = []
        # define order of the columns
        df_premodel_cols = (
            ["sPerson", "Edad", "product_name", "lead_scoring", "probabilidad_compra", "base_values"]
            + list(drivers_barriers.keys())
            + drop_cols
        )

        df_table = dfs.df_recommender_table_split[
            df_premodel_cols
        ]


        # Filter out products that have a low lead_scoring
        if develop:
            # https://trello.com/c/pzLmuSz9
            df_table = df_table[df_table["lead_scoring"] == "High"].sort_values("probabilidad_compra", ascending=False).drop(columns=drop_cols)

        if develop_mutua:
            df_table = df_table[(df_table["lead_scoring"] == "High") | (df_table["lead_scoring"] == "Medium")].sort_values("probabilidad_compra", ascending=False).drop(columns=drop_cols)

        df_table["base_values"] = df_table["base_values"] * 100
        df_table["base_values"] = df_table["base_values"].round(decimals=1)

        # Replace NaN values of factors with '-'
        for key in drivers_barriers.keys():
            fill_val = None
            if 'name' in key:
                # df_table["driver_0_name"] = df_table["driver_0_name"].fillna("-")
                fill_val = ""

            if 'value' in key:
                fill_val = ""

            if "pct" in key:
                fill_val = 0

            if fill_val != None:
                print(key,fill_val)
                df_table[key] = df_table[key].fillna(fill_val)

        as_type_dict = {
            'sPerson': 'str',
        }

        # for key in drivers_barriers.keys():
        #     if 'name' in key:
        #         as_type_dict[key] = 'str'

        df_table = df_table.astype(
            as_type_dict
        ).rename(
            # Add a more readble name
            columns={
                **renames,
                **drivers_barriers,
            },
        )


        # do this computation later on the csv file via jupyter-lab, if it takes too long
        df_table['Probability (%)'] = df_table['Probability (%)'].round(decimals=1)

        # Common settings for the columns of the table
        common_col_options = {
        }

        # https://trello.com/c/pzLmuSz9

        data = df_table.sort_values("Probability (%)", ascending=False)

        if develop:
            # Limit to first 50 rows
            data = df_table.head(50)

        # data.dtypes.value_counts()
        columns_options = {
            'Product': {
                'width': 300,
            },
            'Probability (%)': {
                'width': 150,
            },
        }
        # Add drivers_barriers column width
        for name, re_name in drivers_barriers.items():
            if 'value' in name:
                columns_options[re_name] = {
                    'width': 120
                }

            if 'name' in name:
                columns_options[re_name] = {
                    'width': 300
                }

        shimoku.plt.table(
            order=next_order,
            data=data,
            # data=df_table,
            page_size_options=[10, 20],
            rows_size=4,
            categorical_columns=[
                "Lead Scoring", "Empresa",
            ],
            label_columns={
                ("Probability (%)", "outlined"): {
                    (0,50): "error",
                    (50,75): "warning",
                    (75,100): "success",
                },
                ("Lead Scoring", "filled"): {
                    "Low": "error",
                    "Medium": "warning",
                    "High": "success",
                },
                # This is the thing that causes problems
                # ("Drivers", "filled"): "main",
                # ("Barriers", "filled"): "caution",
            },
            columns_options=columns_options,
        )

        next_order+=1

        return next_order

    def table_simple(order: int):
        """
        Product Recommender table
        """
        # shimoku.plt.change_current_tab("Simple")
        next_order=order

        # define order of the columns
        df_premodel_cols = ["sPerson", "Edad", "product_name", "lead_scoring", "probabilidad_compra",
                           # "base_values", "positive_impact_factors", "negative_impact_factors", "alternativo_reta",
                            "_base_values_x", "positive_impact_factors", "negative_impact_factors",
                           # "etapa_vida",
                            "product_category",
                            ]
        df_table = dfs.df_recommender_table[
            df_premodel_cols
        ]


        # Filter out products that have a low lead_scoring
        if develop:
            # https://trello.com/c/pzLmuSz9
            df_table = df_table.sort_values("probabilidad_compra", ascending=False)
            # [df_table["lead_scoring"] == "Medium"]
        if develop_mutua:
            df_table = df_table[(df_table["lead_scoring"] == "High") | (df_table["lead_scoring"] == "Medium")].sort_values("probabilidad_compra", ascending=False)

        df_table["_base_values_x"] = df_table["_base_values_x"] * 100
        df_table["_base_values_x"] = df_table["_base_values_x"].round(decimals=1)

        df_table = df_table.rename(
            # Add a more readble name
            columns={
                "lead_scoring": "Lead Scoring",
                "probabilidad_compra": "Probability (%)",
                "product_name": "Product",
                "product_category": "Empresa",
                "_base_values_x": "Base value",
                "positive_impact_factors": "Drivers",
                "negative_impact_factors": "Barriers",
                "etapa_vida": "Etapa Vida",
                # "alternativo_reta": "Alternativo RETA",
            },
        ).astype(
            # Convert to string because the frontend add dots
            # to large integers
            {'sPerson': 'str'}
        )

        # Replace NaN values of factors with the empty string
        df_table["Drivers"] = df_table["Drivers"].fillna("")
        df_table["Barriers"] = df_table["Barriers"].fillna("")

        # do this computation later on the csv file via jupyter-lab, if it takes too long
        df_table['Probability (%)'] = df_table['Probability (%)'].round(decimals=1)

        # Common settings for the columns of the table
        common_col_options = {
        }

        data = df_table.sort_values("Probability (%)", ascending=False)

        # https://trello.com/c/pzLmuSz9
        if develop:
            # Limit to first 50 rows
            data = df_table.head(50)

        impact_factors_col_with = 450

        shimoku.plt.table(
            order=next_order,
            data=data,
            # data=df_table,
            page_size_options=[10, 20],
            rows_size=4,
            categorical_columns=[
                "Lead Scoring", "Empresa", "Alternativo RETA",
                "Product", "Etapa Vida",
            ],
            label_columns={
                ("Probability (%)", "outlined"): {
                    (0,50): "error",
                    (50,75): "warning",
                    (75,100): "success",
                },
                ("Lead Scoring", "filled"): {
                    "Low": "error",
                    "Medium": "warning",
                    "High": "success",
                },
                ("Alternativo RETA", "outlined"): {
                    "si": "success",
                    "no": "error",
                }
                # This is the thing that causes problems
                # ("Drivers", "filled"): "main",
                # ("Barriers", "filled"): "caution",
            },
            columns_options={
                'Product': {
                    'width': 300,
                },
                'Probability (%)': {
                    'width': 150,
                },
                'Lead Scoring': {
                    'width': 100,
                },
                'Drivers': {
                    'width': impact_factors_col_with,
                },
                'Barriers': {
                    'width': impact_factors_col_with,
                },
                "Etapa Vida": {
                    'width': 230,
                },
                "Base value": {
                    'with': 195,
                },
            },
        )

        next_order+=1

        return next_order

    def table(order: int):
        next_order=order

        shimoku.plt.set_tabs_index(
            tabs_index=('tables', "Simple"),
            order=next_order,
            just_labels=False,
            sticky=False,
        )
        next_order+=1

        next_order+=table_simple(next_order)
        # we are not going to use comples
        # next_order+=table_complex(next_order)

        shimoku.plt.pop_out_of_tabs_group()
        return next_order

    order+=headings(order)
    order+=indicators(order)
    order+=table_header(order)
    order+=info_btn(shimoku, order, info_modal_predicted)
    order+=table(order)

    shimoku.pop_out_of_menu_path()

explain_menupath_prefix="AI insights"
def explainability_page(shimoku: Client, dfs: DFs, min_plot: int = 0, max_plot: int= 0):


  #  json_insights = read_json("ai_insights")

    def feature_importance(order: int, df_product: pd.DataFrame, all_tab=False):
        """
        Feature importance chart
        """
        next_order=order
        shimoku.plt.html(
            html=shimoku.html_components.create_h1_title(
                title="Feature Importance",
                subtitle="Weight of each feature in the probability for cross selling",
            ),
            order=next_order,
        )
        next_order+=1

        ascending = not all_tab
        # Use first bacuase products are duplicated
        raw_data = df_product.dropna(subset=["value_feature"], how="all").drop_duplicates(
            subset=["feature"],
            keep="first",
        ).sort_values(
            by="importance", ascending=False
        ).head(20)

        # Importance numbers will have 1 decimal
        raw_data["importance"] = raw_data["importance"].round(decimals=1)

        # drop rows where importance is 0
        data = raw_data[raw_data['importance'] != 0].rename(columns={
            'importance': "Importance"
        })

        shimoku.plt.horizontal_bar(
            data=data,
            order=next_order,
            x="feature",
            y="Importance"
        )
        next_order+=1

        return (next_order, data["feature"].unique())

    def partial_dependence(order: int, df_pdp: pd.DataFrame, features: Iterable):
        """
        Partial dependence section
        """

        next_order=order

        shimoku.plt.html(
            html=shimoku.html_components.create_h1_title(
                title="Partial Dependence",
                subtitle="Measures the relationship between every feature and the cross selling probability",
            ),
            order=next_order,
        )
        next_order+=1

        next_order+=info_btn(shimoku,next_order,modal_partial_dependence, modal_name="partialdep_modal")

        type_feature=df_pdp.groupby(
            by="type_feature",
        )

        # --- Nominal section --- #
        df_nominal=type_feature.get_group(
            "nominal",
        )

        # Readjust df_nominal to have the 20 most important
        df_nominal = df_nominal[df_nominal["feature"].isin(features)]

        shimoku.plt.html(
            html=shimoku.html_components.create_h1_title(
                title="",
                subtitle="Nominal features",
            ),
            order=next_order,
            cols_size=12,
        )

        next_order+=1

        df_nominal = df_nominal.sort_values(by="feature")

        nominal_features = df_nominal["feature"].unique()

        # Use the features array since is already ordered by importance
        idx = 0
        for feature_name in features:
            if feature_name not in nominal_features:
                continue
            print(feature_name)
            df_feature = df_nominal.query(f"feature == '{feature_name}'")
            # TODO: find why there is empty dataframes

            if df_feature.empty:
                continue

            if idx == 0:
                shimoku.plt.set_tabs_index(
                    tabs_index=('partial_dependence_nominal', feature_name),
                    # parent_tabs_index=(products_tab_group, "All"),
                    sticky=False,
                    just_labels=True,
                    order=next_order,
                )
                next_order+=1

            if idx > 0:
                shimoku.plt.change_current_tab(feature_name)

            as_index_features = ["Ingresos"]
            as_index = feature_name in as_index_features

            df_bar = df_feature.groupby(
                by="value_feature", as_index=as_index,
            ).agg({"Probability": "sum"}).sort_values(by="value_feature")

            # Handle each specific ordering case
            if feature_name == "Ingresos":
                feature_order = [
                    '0_20.000',
                    '20.001_50.000',
                    '50.001_100.000',
                    '100.001_200.000',
                    '200.001_sup',
                ]
                # Re-order the index
                df_bar = df_bar.reindex(feature_order)

            # Reset the index
            if as_index:
                df_bar = df_bar.reset_index()

            # Format decimal numbers in Partial Dependence to % with 2 decimals '20.23'
            df_bar["Probability"] = df_bar["Probability"].round(decimals=2)

            # Convert probability to percentage
            df_bar["Probability"] = df_bar["Probability"] * 100
            shimoku.plt.bar(
                # title="Nominal features",
                data=df_bar,
                x="value_feature",
                y=["Probability"],
                x_axis_name="Category",
                order=next_order,
                cols_size=12
            )
            # Increment counter when the loop fully completes
            idx+=1


        # Don't know if this is right
        # Gives error
        # shimoku.plt.pop_out_of_tabs_group()

        next_order+=1
        # shimoku.plt.pop_out_of_tabs_group()

        # --- End Nominal section --- #

        # --------------------------------- #

        # --- Numerical section --- #

        df_numerical=type_feature.get_group(
            "numerical",
        ).astype(
            {"value_feature": 'Float32'}
        ).sort_values(
            by="feature"
        )

        # debug
        # df_numerical.query("feature=='AñosPasivoPlanplanes_22'")[["feature", "value_feature", "Probability"]]

        # Readjust df_numerical to have the 20 most important
        df_numerical = df_numerical[df_numerical["feature"].isin(features)]

        df_numerical.dropna(
            subset=["Probability", "value_feature"], inplace=True,
        )
        df_numerical.drop_duplicates(subset=["feature", "value_feature"], keep="first", inplace=True)

        # Format decimal numbers in Partial Dependence to % with 2 decimals '20.23'
        df_numerical["Probability"] = df_numerical["Probability"].round(decimals=2)

        # Convert probability to percentage
        df_numerical["Probability"] = df_numerical["Probability"] * 100

        numerical_features = df_numerical["feature"].unique()

        idx = 0
        # Use the features array since is already ordered by importance
        for feature_name  in features:
            if feature_name not in numerical_features:
                # Continue caballero!
                continue
            df_feature = df_numerical.query(f"feature == '{feature_name}'")

            if idx == 0:
                shimoku.plt.set_tabs_index(
                    tabs_index=('partial_dependence_numerical', feature_name),
                    # parent_tabs_index=(products_tab_group, "All"),
                    sticky=False,
                    just_labels=True,
                    order=next_order,
                )
                next_order+=1

                shimoku.plt.html(
                    html=shimoku.html_components.create_h1_title(
                        title="",
                        subtitle="Numerical features",
                    ),
                    order=next_order,
                    cols_size=12,
                )
                next_order+=1

            if idx > 0:
                shimoku.plt.change_current_tab(feature_name)

            if df_feature.empty:
                continue

            df_feature["value_feature"] = df_feature["value_feature"].round()

            df_feature.sort_values(by="value_feature", inplace=True)

            shimoku.plt.line(
                # title="Numerical feature",
                data=df_feature,
                y=["Probability"],
                x="value_feature",
                x_axis_name="Value of the feature",
                order=next_order,
                cols_size=12,
            )
            # Increment counter when the loop fully completes
            idx+=1

        next_order+=1

        shimoku.plt.pop_out_of_tabs_group()
        return next_order
        # --- End Numerical section --- #

    # === Main Body of explainability page ===

    value_feat_map = {
        "True": "1",
        "False": "0",
    }

    feature_to_replace = value_feat_map.keys()
    # Use this line to debug
    # dfs.df_importance_pdb.loc[(dfs.df_importance_pdb["feature"] == "AñosPasivoPlanplanes_22") & (dfs.df_importance_pdb["value_feature"] == 1)][["feature", "value_feature", "type_feature"]]

    # Force value_feature to 1 where feature name is AñosPasivoPlanplanes_22
    # https://trello.com/c/goQ8sS0K
    dfs.df_importance_pdb.loc[
        (dfs.df_importance_pdb["feature"] == "AñosPasivoPlanplanes_22") &
        (dfs.df_importance_pdb["value_feature"] == "True")
        , "type_feature"
    ] = "numerical"

    dfs.df_importance_pdb.loc[
        (dfs.df_importance_pdb["feature"] == "AñosPasivoPlanplanes_22") &
        (dfs.df_importance_pdb["value_feature"] == "True")
        , "value_feature"
    ] = 1

    # Plot only this products
    # https://trello.com/c/VFx4K7Wi
    product_list = [
        "Gran Dependència", "Baixa Laboral <90 dies",
        "Baixa Laboral >90 dies",
        "CorreduriaSalud", "CorreduriaDeceso", "CorreduriaHogar",
        "CorreduriaAutomovil", "planes_10",
    ]
    product_list = [
        "Gran Dependència",
        "CorreduriaSalud",
    ]   

    print("----", "loop", "-----")
    print(dfs.df_importance_pdb.query("product_category=='Correduria'"))
               

    for product_category, df_i_pdp_cat in dfs.df_importance_pdb.groupby(by="product_category"):

        print("----", product_category, "-----")

        product_group = df_i_pdp_cat.groupby(by="product")
        group_size = len(product_group)

        plotted = 0
        for idx, (product_name, df_product) in enumerate(product_group):
            if product_name not in product_list:
                continue

            print(f"---- {plotted} {product_name} -----")
            plotted+=1
            # Comment this off, because whe have a list of specific products

            # if develop_mutua:
            #     if group_size < min_plot:
            #         break
            #     if idx > max_plot:
            #         break
            #     if not (idx >= min_plot and idx <= max_plot):
            #         # dont plot, skip iteration
            #         continue

            if develop:
                if plotted > 1:
                    break
                # if idx > 1:
                #     break
            order=0

            # Fix paths, because the frontend doesn't supports >
            # for urls
            sub_path = product_name

            if sub_path == "Baixa Laboral >90 dies":
               sub_path = "Baixa Laboral major 90 dies"

            if sub_path == "Baixa Laboral <90 dies":
               sub_path = "Baixa Laboral menor 90 dies"

            shimoku.set_menu_path(
                name=f"{explain_menupath_prefix} {product_category}",
                sub_path=sub_path,
            )

            # Currently Modals can be plotted in subpaths
            # Uncomment line below when Hotfix is released
            order+=info_btn(shimoku, order, info_modal_ai_insights, modal_name="ai_insights_modal")

            importance_ret = feature_importance(order, df_product, all_tab=True)
            order+=importance_ret[0]

            # Change nominal features True/False for 1/0
            df_product_p = df_product.copy()
            df_product_p["value_feature"] = df_product_p["value_feature"].apply(
                lambda v: value_feat_map[v] if v in feature_to_replace else v
            )
            order+=partial_dependence(
                order,
                df_product_p,
                # 20 most important products
                importance_ret[1],
            )

            shimoku.pop_out_of_menu_path()

            # json_insights[product_category].append({
            #     "index": idx,
            #     "name": product_name,
            #     "ok": True
            # })

def configure_navigation(shimoku: Client):
    """
    Navigation configuration
    """

    shimoku.workspaces.change_menu_order(
        uuid=getenv("WORKSPACE_ID"),
        menu_order=[
            path_name_predicted_page,
            f"{explain_menupath_prefix} Mutua",
            f"{explain_menupath_prefix} Correduria",
        ]
    )

def plot_dashboard(shimoku: Client, min_plot: int = 0, max_plot: int = 0):

    # Read CSVs to DataFrames
    dfs = DFs()

    board_name="Cross Selling"
    shimoku.set_board(name=board_name)

    board = shimoku.boards.get_board(name=board_name)
    # Get indicators shared across pages
    biz_indicators = get_indicators_by_bussniess(dfs, board)

    # print("----", "explainability_page start", "-----")
    # explainability_page(
    #     shimoku, dfs,
    #     min_plot=min_plot, max_plot=max_plot
    # )
    # print("----", "explainability_page end", "-----")

    hidden_indicators_page(shimoku, biz_indicators['hidden_indicators'])
    predictions_page(shimoku, dfs, biz_indicators['indicators_summary'])

    configure_navigation(shimoku)






