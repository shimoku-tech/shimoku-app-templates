from utils.components import create_title_name_head, info_modal_predicted
from typing import Callable
from utils.utils import format_number
from dashboard import Dashboard


class PredictionsPage(Dashboard):
    """
    A class representing a page for displaying predictions within a dashboard.

    Inherits from the Dashboard class and is used to display prediction-related
    indicators and data tables.

    Attributes:
        order (int): Order of elements to be plotted.
        menu_path (str): Path of the menu in the dashboard.
    """

    def __init__(self, shimoku):
        """
        Initializes the PredictionsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(shimoku)
        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Predicted opportunities"  # Set the menu path for this page
        self.shimoku.set_menu_path(name=self.menu_path)  # Set the menu path in Shimoku

    def plot(self):
        """
        Plots the predictions page.

        This method retrieves indicators, plots headings, indicators, info buttons,
        and a data table. It also navigates out of the menu path after plotting.
        """
        board_id = self.shimoku.boards.get_board(name=self.board_name)["id"]
        indicators = self.get_indicators_by_business(board_id)

        self.plot_headings()
        self.plot_indicators(indicators)
        self.plot_info_btn(info_modal_predicted)
        self.plot_table()
        self.shimoku.pop_out_of_menu_path()

    def plot_headings(self):
        """
        Plots the headings for the predictions page.

        Returns:
            True if the operation is successful.
        """
        self.shimoku.plt.html(
            html=create_title_name_head(
                title="Predictions",
                subtitle="Cross Selling",
            ),
            order=self.order,
        )
        self.order += 1
        return True

    def plot_indicators(self, indicators):
        """
        Plots the indicators section on the predictions page.

        Parameters:
            indicators: Data for the indicators to be plotted.
        """
        common_indicator_settings = {
            "align": "center",
            "variant": "topColor",
        }

        # Aggregate lead scoring data
        lead_scoring_agg = self.dfs.df_recommender_table.groupby("lead_scoring").agg(
            {"lead_scoring": "count"}
        )

        # Plot general indicators
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Total opportunities",
                subtitle="",
            ),
            order=self.order,
        )
        self.order += 1

        desc_prefix = "Oportunidades"
        self.shimoku.plt.indicator(
            data=[
                {
                    "title": "HIGH",
                    "color": "success",
                    "value": format_number(lead_scoring_agg["lead_scoring"]["High"]),
                    "description": f"{desc_prefix} with a success probability greater than 75%",
                    **common_indicator_settings,
                },
                {
                    "title": "MEDIUM",
                    "color": "warning",
                    "value": format_number(lead_scoring_agg["lead_scoring"]["Medium"]),
                    "description": f"{desc_prefix} with a success probability between 50% and 75%",
                    **common_indicator_settings,
                },
                {
                    "title": "LOW",
                    "color": "error",
                    "value": format_number(lead_scoring_agg["lead_scoring"]["Low"]),
                    "description": f"{desc_prefix} with a success probability of less than 50%",
                    **common_indicator_settings,
                },
            ],
            order=self.order,
        )
        self.order += 3

        # Plot product opportunity indicators
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Product opportunities",
                subtitle="Based on Lead Scoring High",
            ),
            order=self.order,
        )
        self.order += 1

        self.plot_indicator_list(
            indicator_product_data=indicators["indicators_summary"]
        )

        return True

    def plot_info_btn(self, modal_html_fn: Callable[[], str], modal_name="info_modal"):
        """
        Creates an info button with a modal on the predictions page.

        Parameters:
            modal_html_fn: A callable function that returns HTML content for the modal.
            modal_name (str): The name of the modal.
        """
        self.shimoku.plt.modal_button(
            label="Info",
            order=self.order,
            modal=modal_name,
            cols_size=1,
            padding="0, 0, 0, 11",
        )
        self.order += 1

        self.shimoku.plt.set_modal(modal_name=modal_name)
        modal_order = 0
        self.shimoku.plt.html(
            order=modal_order,
            html=modal_html_fn(),
        )
        self.shimoku.plt.pop_out_of_modal()

        return True

    def plot_table(self):
        """
        Plots a table of leads data on the predictions page.

        This method prepares and displays a table showing various details about leads,
        including personal information, product details, and scoring metrics.
        """
        # Plot the title for the leads data section
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Leads data",
                subtitle="Per user and products",
            ),
            order=self.order,
        )
        self.order += 1

        # Define the order of the columns for the table
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

        # Prepare the data frame for the table
        df_table = self.dfs.df_recommender_table[df_premodel_cols].copy()
        df_table["_base_values_x"] = df_table["_base_values_x"] * 100
        df_table["_base_values_x"] = df_table["_base_values_x"].round(decimals=1)

        # Rename columns for readability and convert types as needed
        df_table = df_table.rename(
            columns={
                "lead_scoring": "Lead Scoring",
                "purchase_probability": "Probability (%)",
                "product_name": "Product",
                "_base_values_x": "Base value",
                "positive_impact_factors": "Drivers",
                "negative_impact_factors": "Barriers",
            }
        ).astype({"sPerson": "str"})

        # Replace NaN values in 'Drivers' and 'Barriers' columns with empty strings
        df_table["Drivers"] = df_table["Drivers"].fillna("")
        df_table["Barriers"] = df_table["Barriers"].fillna("")

        # Round 'Probability (%)' to one decimal place
        df_table["Probability (%)"] = df_table["Probability (%)"].round(decimals=1)

        # Sort data by 'Probability (%)' in descending order
        data = df_table.sort_values("Probability (%)", ascending=False)

        # Width setting for 'Drivers' and 'Barriers' columns
        impact_factors_col_width = 450

        # Plot the table with specified settings
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
                "Product": {"width": 100},
                "Probability (%)": {"width": 150},
                "Lead Scoring": {"width": 130},
                "Drivers": {"width": impact_factors_col_width},
                "Barriers": {"width": impact_factors_col_width},
                "Base value": {"width": 200},
            },
        )

        self.order += 1

        return True
