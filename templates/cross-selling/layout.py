# Core python libraries
from os import getenv
from typing import Callable, Iterable

# Local modules
from utils.utils import DFs, format_number, read_json
from utils.components import (
    create_title_name_head,
    info_modal_predicted,
)

from utils.utils import DFs

# Third
from shimoku_api_python import Client
import numpy as np
import pandas as pd


# Used by predictions_page and hidden_indicators_page
def plot_indicator_list(shimoku: Client, order: int, indicator_product_data):
    """
    Plot a list of HIGH indicators
    """
    next_order = order

    # Directly iterate through the list associated with the key "pepe"
    for idx, indicator_data in enumerate(indicator_product_data):
        # Pop not needed key
        indicator_data.pop(
            "percentage", None
        )  # Use None to avoid KeyError if 'percentage' does not exist

        shimoku.plt.indicator(
            data=indicator_data,
            order=next_order,
            cols_size=3,
        )
        next_order += 1

    return next_order


def make_indicator(
    product_name: str, value_lead_scoring, total_high: int, extra_options={}
):
    """
    Construct indicator dict for the indicator section
    """
    percentage = (value_lead_scoring / total_high) * 100
    perc_formatted = round(percentage, ndigits=0)

    return {
        "title": f"{product_name}",
        "value": f"{format_number(value_lead_scoring)} ({'{:.0f}'.format(perc_formatted)} %)",
        "color": "success",
        "percentage": perc_formatted,
        "align": "left",
        "variant": "topColor",
        **extra_options,
    }

def get_indicators_by_bussniess(dfs: DFs, board: dict):
    """
    Gets the indicators by product name since product categories have been removed.
    """

    # Count the number of 'High' lead scoring by product name
    high_scoring_per_product = (
        dfs.df_recommender_table.query(f"lead_scoring=='High'")
        .groupby(by="product_name")
        .agg({"lead_scoring": "count"})
    )
    
    # Build indicators per product
    indicators_summary = []
    hidden_indicators = []

    total_high = high_scoring_per_product["lead_scoring"].sum()

    # Sort within the dataframe
    high_scoring_per_product_sorted = high_scoring_per_product.sort_values(
        "lead_scoring", ascending=False
    )

    high_group_size = len(high_scoring_per_product_sorted)

    # Used only after the third product
    scoring_accumulator = 0

    for product_count, (product_name, row) in enumerate(
        high_scoring_per_product_sorted.iterrows()
    ):
        value_lead_scoring = row["lead_scoring"]

        extra_options = {}

        # Only the first three products are allowed to be displayed,
        # the rest are grouped into one product called 'Other products'
        # And saved to another list to be plotted in a hidden path
        if product_count > 2:
            scoring_accumulator += value_lead_scoring
            hidden_indicators.append(
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
                extra_options = {
                    "targetPath": f"{board['id']}/hidden-indicators",
                }

            else:
                # Skip the iteration so we don't create a new entry in the indicators_summary array
                continue

        # Make indicator data
        indicators_summary.append(
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
    order = 0
    menu_path = "Hidden indicators"
    shimoku.set_menu_path(name=menu_path)

    shimoku.plt.html(
        html=shimoku.html_components.create_h1_title(
            title="Otros productos",
            subtitle="Indicadores Lead Scoring HIGH, de 'otros productos'",
        ),
        order=order,
    )
    order += 1

    order += plot_indicator_list(
        shimoku, order, indicator_product_data=indicator_product_data
    )

    # Hide the menu path
    shimoku.menu_paths.update_menu_path(
        name=menu_path,
        hide_path=True,
    )

    shimoku.pop_out_of_menu_path()


def info_btn(
    shimoku: Client,
    order: int,
    modal_html_fn: Callable[[], str],
    modal_name="info_modal",
):
    next_order = order
    shimoku.plt.modal_button(
        label="Info",
        order=next_order,
        modal=modal_name,
        cols_size=1,
        # push to the right
        padding="0, 0, 0, 11",
    )
    next_order += 1

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

def headings(shimoku, order: int):
    next_order = order

    shimoku.plt.html(
        html=create_title_name_head(
            title="Predictions",
            subtitle="Cross Selling",
        ),
        order=next_order,
    )

    next_order += 1
    return next_order

def indicators(shimoku, order: int, indicators_summary, dfs: DFs):
    """
    Indicators section
    """
    next_order = order

    common_indicator_settings = {
        "align": "center",
        "variant": "topColor",
    }

    # Total rows High, Medium and LOW probability
    lead_scoring_agg = dfs.df_recommender_table.groupby(by="lead_scoring").agg(
        {"lead_scoring": "count"}
    )

    # General indicators
    shimoku.plt.html(
        html=shimoku.html_components.create_h1_title(
            title="Total opportunities",
            subtitle="",
        ),
        order=next_order,
    )
    next_order += 1

    # description prefix
    desc_prefix = "Oportunidades"
    next_order += shimoku.plt.indicator(
        data=[
            {
                "title": "HIGH",
                "value": format_number(lead_scoring_agg["lead_scoring"]["High"]),
                "color": "success",
                "description": f"{desc_prefix} con una probabilidad de éxito mayor del 75%",
                **common_indicator_settings,
            },
            {
                "title": "MEDIUM",
                "value": format_number(lead_scoring_agg["lead_scoring"]["Medium"]),
                "color": "warning",
                "description": f"{desc_prefix} con una probabilidad de éxito de entre el 50% y el 75%",
                **common_indicator_settings,
            },
            {
                "title": "LOW",
                "value": format_number(lead_scoring_agg["lead_scoring"]["Low"]),
                "color": "error",
                "description": f"{desc_prefix} con una probabilidad de éxito menor del 50%",
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
        order=next_order,
    )
    next_order += 1

    # Indicators per product category

    next_order += plot_indicator_list(
        shimoku, order=next_order, indicator_product_data=indicators_summary
    )

    return next_order

def table_simple(shimoku, order: int, dfs: DFs):
    """
    Product Recommender table
    """
    # shimoku.plt.change_current_tab("Simple")
    next_order = order

    # define order of the columns
    df_premodel_cols = [
        "sPerson",
        "Edad",
        "product_name",
        "lead_scoring",
        "probabilidad_compra",
        "_base_values_x",
        "positive_impact_factors",
        "negative_impact_factors",
    ]

    df_table = dfs.df_recommender_table[df_premodel_cols].copy()
    df_table["_base_values_x"] = df_table["_base_values_x"] * 100
    df_table["_base_values_x"] = df_table["_base_values_x"].round(decimals=1)

    df_table = df_table.rename(
        # Add a more readble name
        columns={
            "lead_scoring": "Lead Scoring",
            "probabilidad_compra": "Probability (%)",
            "product_name": "Product",
            "_base_values_x": "Base value",
            "positive_impact_factors": "Drivers",
            "negative_impact_factors": "Barriers",
            "etapa_vida": "Etapa Vida",
        },
    ).astype(
        # Convert to string because the frontend add dots
        # to large integers
        {"sPerson": "str"}
    )

    # Replace NaN values of factors with the empty string
    df_table["Drivers"] = df_table["Drivers"].fillna("")
    df_table["Barriers"] = df_table["Barriers"].fillna("")

    # do this computation later on the csv file via jupyter-lab, if it takes too long
    df_table["Probability (%)"] = df_table["Probability (%)"].round(decimals=1)

    # Common settings for the columns of the table
    common_col_options = {}

    data = df_table.sort_values("Probability (%)", ascending=False)

    impact_factors_col_with = 450

    shimoku.plt.table(
        order=next_order,
        data=data,
        page_size_options=[10, 20],
        rows_size=4,
        categorical_columns=[
            "Lead Scoring",
            "Empresa",
            "Alternativo RETA",
            "Product",
            "Etapa Vida",
        ],
        label_columns={
            ("Probability (%)", "outlined"): {
                (0, 50): "error",
                (50, 75): "warning",
                (75, 100): "success",
            },
            ("Lead Scoring", "filled"): {
                "Low": "error",
                "Medium": "warning",
                "High": "success",
            },
            ("Alternativo RETA", "outlined"): {
                "si": "success",
                "no": "error",
            },
        },
        columns_options={
            "Product": {
                "width": 100,
            },
            "Probability (%)": {
                "width": 150,
            },
            "Lead Scoring": {
                "width": 130,
            },
            "Drivers": {
                "width": impact_factors_col_with,
            },
            "Barriers": {
                "width": impact_factors_col_with,
            },
            "Base value": {
                "with": 200,
            },
        },
    )

    next_order += 1

    return next_order

def table(shimoku, order: int, dfs: DFs):
    next_order = order

    shimoku.plt.html(
        html=shimoku.html_components.create_h1_title(
            title="Leads data",
            subtitle="Per user and products",
        ),
        order=next_order,
    )
    next_order += 1

    next_order += table_simple(shimoku, next_order, dfs)

    return next_order

def predictions_page(shimoku: Client, dfs: DFs, indicators_summary):
    """
    Predictions page sections and plots
    """
    dfs = DFs()
    shimoku.set_menu_path(name=path_name_predicted_page)
    order = 0
    order += headings(shimoku, order)
    order += indicators(shimoku, order, indicators_summary, dfs)
    order += info_btn(shimoku, order, info_modal_predicted)
    order += table(shimoku, order, dfs)

    shimoku.pop_out_of_menu_path()


def plot_dashboard(shimoku: Client, min_plot: int = 0, max_plot: int = 0):
    # Read CSVs to DataFrames
    dfs = DFs()

    board_name = "Cross Selling"
    shimoku.set_board(name=board_name)

    board = shimoku.boards.get_board(name=board_name)
    # Get indicators shared across pages
    biz_indicators = get_indicators_by_bussniess(dfs, board)

    # Plot pages
    hidden_indicators_page(shimoku, biz_indicators["hidden_indicators"])
    predictions_page(shimoku, dfs, biz_indicators["indicators_summary"])
