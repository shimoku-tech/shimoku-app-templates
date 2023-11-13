
from transformations.get_predictions_table import get_predicted_opportunities
from utils.utils import DFs, format_number
from shimoku_api_python import Client
from utils.components import create_title_name_head
from typing import Callable
from utils.components import info_modal_predicted

# Main dashboard
class Dashboard:
    
    # Init Dashboard class
    def __init__(self, shimoku: Client):
        self.board_name = "Cross Selling" 
        self.dfs = DFs()
        self.shimoku = shimoku
        self.shimoku.set_board(name=self.board_name)

    # Data transformations
    def transform(self):
        get_predicted_opportunities()

    # Plotting dashboard pages
    def plot(self):

        hi = HiddenIndicatorsPage(self.shimoku)
        hi.plot()

        pp = PredictionsPage(self.shimoku)
        pp.plot()



    # Utils
    def get_indicators_by_bussniess_v1(self, board_id):
        """
        Gets the indicators by product name since product categories have been removed.
        """

        # Count the number of 'High' lead scoring by product name
        high_scoring_per_product = (
            self.dfs.df_recommender_table.query(f"lead_scoring=='High'")
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
                    self.make_indicator(
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
                        "targetPath": f"{board_id}/hidden-indicators",
                    }

                else:
                    # Skip the iteration so we don't create a new entry in the indicators_summary array
                    continue

            # Make indicator data
            indicators_summary.append(
                self.make_indicator(
                    product_name,
                    value_lead_scoring,
                    total_high,
                    **extra_options,
                )
            )

        return {
            "indicators_summary": indicators_summary,
            "hidden_indicators": hidden_indicators,
        }

    def plot_indicator_list(self, indicator_product_data):
        """
        Plot a list of HIGH indicators
        """
        # Directly iterate through the list associated with the key "pepe"
        for idx, indicator_data in enumerate(indicator_product_data):
            # Pop not needed key
            indicator_data.pop(
                "percentage", None
            )  # Use None to avoid KeyError if 'percentage' does not exist

            self.shimoku.plt.indicator(
                data=indicator_data,
                order=self.order,
                cols_size=3,
            )
            self.order += 1

        return True

    @staticmethod
    def make_indicator(
        product_name: str, value_lead_scoring, total_high: int, **kwargs
    ):
        """
        Construct indicator dict for the indicator section
        """

        percentage = (value_lead_scoring / total_high) * 100
        perc_formatted = round(percentage, ndigits=0)

        indicator_dict = {
            "title": f"{product_name}",
            "value": f"{format_number(value_lead_scoring)} ({'{:.0f}'.format(perc_formatted)} %)",
            "color": "success",
            "percentage": perc_formatted,
            "align": "left",
            "variant": "topColor",
        }

        # Merge kwargs into the indicator_dict
        indicator_dict.update(kwargs)

        return indicator_dict


class PredictionsPage(Dashboard):

    def __init__(self, shimoku):

        # init as a dougther class of Dashboard
        super().__init__(shimoku)
        self.order = 0
        self.menu_path="Predicted opportunities"
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):

        board_id = self.shimoku.boards.get_board(name=self.board_name)["id"]
        indicators_ = self.get_indicators_by_bussniess_v1(board_id)

        self.headings()
        self.indicators(indicators_)
        self.info_btn(info_modal_predicted)
        self.table()
        self.shimoku.pop_out_of_menu_path()

    # Utils 
    def headings(self):
        self.shimoku.plt.html(
            html=create_title_name_head(
                title="Predictions",
                subtitle="Cross Selling",
            ),
            order=self.order,
        )
        self.order += 1
        return True

    def indicators(self, indicators):
        """
        Indicators section
        """

        common_indicator_settings = {
            "align": "center",
            "variant": "topColor",
        }

        # Total rows High, Medium and LOW probability
        lead_scoring_agg = self.dfs.df_recommender_table.groupby(by="lead_scoring").agg(
            {"lead_scoring": "count"}
        )

        # General indicators
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Total opportunities",
                subtitle="",
            ),
            order=self.order,
        )
        self.order += 1

        # description prefix
        desc_prefix = "Oportunidades"
        self.shimoku.plt.indicator(
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
                    **common_indicator_settings,
                },
            ],
            order=self.order,
        )
        self.order += 3

        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Product opportunities",
                subtitle="Basado en Lead Scoring High",
            ),
            order=self.order,
        )
        self.order += 1

        # Indicators per product category
        self.plot_indicator_list(indicator_product_data=indicators["indicators_summary"])

        return True

    def info_btn(self,
        modal_html_fn: Callable[[], str],
        modal_name="info_modal",
    ):
        self.shimoku.plt.modal_button(
            label="Info",
            order=self.order,
            modal=modal_name,
            cols_size=1,
            # push to the right
            padding="0, 0, 0, 11",
        )
        self.order += 1

        # Begin modal content
        self.shimoku.plt.set_modal(modal_name=modal_name)
        modal_order = 0
        self.shimoku.plt.html(
            order=modal_order,
            html=modal_html_fn(),
        )

        # End Modal content
        self.shimoku.plt.pop_out_of_modal()

        return True

    def table(self):

        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Leads data",
                subtitle="Per user and products",
            ),
            order=self.order,
        )
        self.order += 1

        # define order of the columns
        df_premodel_cols = [
            "sPerson",
            "Edad",
            "product_name",
            "lead_scoring",
            "purchase_probability",
            "_base_values_x",
            "positive_impact_factors",
            "negative_impact_factors",
        ]

        df_table = self.dfs.df_recommender_table[df_premodel_cols].copy()
        df_table["_base_values_x"] = df_table["_base_values_x"] * 100
        df_table["_base_values_x"] = df_table["_base_values_x"].round(decimals=1)

        df_table = df_table.rename(
            # Add a more readble name
            columns={
                "lead_scoring": "Lead Scoring",
                "purchase_probability": "Probability (%)",
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

        self.shimoku.plt.table(
            order=self.order,
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

        self.order += 1



class HiddenIndicatorsPage(Dashboard):

    def __init__(self, shimoku):
        super().__init__(shimoku)
        self.order = 0
        self.menu_path="Hidden indicators"
        self.shimoku.set_menu_path(name=self.menu_path)
    
    def plot(self):

        board_id = self.shimoku.boards.get_board(name=self.board_name)["id"]
        indicators_ = self.get_indicators_by_bussniess_v1(board_id)

        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Otros productos",
                subtitle="Indicadores Lead Scoring HIGH, de 'otros productos'",
            ),
            order=self.order,
        )
        self.order += 1

        self.plot_indicator_list(indicator_product_data=indicators_["hidden_indicators"])

        # Hide the menu path
        self.shimoku.menu_paths.update_menu_path(
            name=self.menu_path,
            hide_path=True,
        )

        self.shimoku.pop_out_of_menu_path()
