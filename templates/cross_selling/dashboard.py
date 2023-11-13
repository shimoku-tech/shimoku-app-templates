from transformations.get_predictions_table import get_predicted_opportunities
from utils.utils import DFs, format_number
from shimoku_api_python import Client
from utils.components import create_title_name_head
from typing import Callable
from utils.components import info_modal_predicted


class Dashboard:
    """
    A class used to represent a Dashboard for displaying various data visualizations.

    Attributes:
        board_name (str): Name of the dashboard.
        dfs (DFs): An instance of a DFs class for handling data frames.
        shimoku (Client): An instance of a Client class for Shimoku API interactions.
    """

    def __init__(self, shimoku: Client):
        """
        The constructor for the Dashboard class.

        Parameters:
            shimoku (Client): An instance of a Client class for Shimoku API interactions.
        """
        self.board_name = "Cross Selling"  # Name of the dashboard
        self.dfs = DFs()  # DataFrames handler
        self.shimoku = shimoku  # Shimoku client instance
        self.shimoku.set_board(name=self.board_name)  # Setting up the board in Shimoku

    def transform(self):
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """
        get_predicted_opportunities()  # Function call to get predicted opportunities
        return True


    def plot(self):
        """
        Plot the dashboard pages.

        This method handles the plotting of various pages in the dashboard.
        It creates instances of different page classes and calls their plot methods.
        """
        hi = HiddenIndicatorsPage(self.shimoku)  # Instance of HiddenIndicatorsPage
        hi.plot()  # Plotting the hidden indicators page

        pp = PredictionsPage(self.shimoku)  # Instance of PredictionsPage
        pp.plot()  # Plotting the predictions page
        return True

    def get_indicators_by_business(self, board_id):
        """
        Gets the indicators by product name.

        This method counts the number of 'High' lead scoring by product name and
        creates indicators for each product. Products beyond the top three are
        grouped into 'Other products'.

        Parameters:
            board_id: The board identifier used for creating hidden indicator links.

        Returns:
            A dictionary containing summaries of visible and hidden indicators.
        """
        # Count 'High' lead scoring by product name
        high_scoring_per_product = (
            self.dfs.df_recommender_table.query("lead_scoring=='High'")
            .groupby("product_name")
            .agg({"lead_scoring": "count"})
        )

        indicators_summary = []
        hidden_indicators = []

        total_high = high_scoring_per_product["lead_scoring"].sum()

        # Sort the dataframe by lead scoring
        high_scoring_per_product_sorted = high_scoring_per_product.sort_values(
            "lead_scoring", ascending=False
        )

        high_group_size = len(high_scoring_per_product_sorted)
        scoring_accumulator = (
            0  # Accumulator for scores of products beyond the top three
        )

        for product_count, (product_name, row) in enumerate(
            high_scoring_per_product_sorted.iterrows()
        ):
            value_lead_scoring = row["lead_scoring"]
            extra_options = {}

            if product_count > 2:
                scoring_accumulator += value_lead_scoring
                hidden_indicators.append(
                    self.make_indicator(
                        product_name,
                        value_lead_scoring,
                        total_high,
                    )
                )

                if product_count == high_group_size - 1:
                    product_name = "Otros productos"
                    value_lead_scoring = scoring_accumulator
                    extra_options = {"targetPath": f"{board_id}/hidden-indicators"}
                else:
                    continue

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
        Plots a list of HIGH indicators.

        Parameters:
            indicator_product_data: Data of the product indicators to be plotted.
        """
        for idx, indicator_data in enumerate(indicator_product_data):
            # Remove 'percentage' key if it exists
            indicator_data.pop("percentage", None)

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
        Constructs an indicator dictionary for the indicator section.

        Parameters:
            product_name (str): Name of the product.
            value_lead_scoring: The lead scoring value of the product.
            total_high (int): The total high score across all products.
            **kwargs: Additional keyword arguments to be included in the indicator.

        Returns:
            A dictionary representing the indicator with various attributes.
        """
        percentage = (value_lead_scoring / total_high) * 100
        perc_formatted = round(percentage)

        indicator_dict = {
            "title": product_name,
            "value": f"{format_number(value_lead_scoring)} ({perc_formatted:.0f}%)",
            "color": "success",
            "percentage": perc_formatted,
            "align": "left",
            "variant": "topColor",
        }

        indicator_dict.update(kwargs)

        return indicator_dict


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

        self.headings()
        self.indicators(indicators)
        self.info_btn(info_modal_predicted)
        self.table()
        self.shimoku.pop_out_of_menu_path()

    def headings(self):
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

    def indicators(self, indicators):
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

    def info_btn(self, modal_html_fn: Callable[[], str], modal_name="info_modal"):
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

    def table(self):
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

class HiddenIndicatorsPage(Dashboard):
    """
    A class representing a page of hidden indicators within a dashboard.

    Inherits from the Dashboard class and is used to display indicators that are
    not immediately visible on the main dashboard page.

    Attributes:
        order (int): Order of elements to be plotted.
        menu_path (str): Path of the menu in the dashboard.
    """

    def __init__(self, shimoku):
        """
        Initializes the HiddenIndicatorsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(shimoku)
        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Hidden indicators"  # Set the menu path for this page
        self.shimoku.set_menu_path(name=self.menu_path)  # Set the menu path in Shimoku

    def plot(self):
        """
        Plots the hidden indicators page.

        This method retrieves hidden indicators and plots them on the page.
        It also sets the title and hides the menu path after plotting.
        """
        # Retrieve the board ID using the board name
        board_id = self.shimoku.boards.get_board(name=self.board_name)["id"]
        # Get indicators by business logic
        indicators = self.get_indicators_by_business(board_id)

        # Plot the title for the hidden indicators section
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Otros productos",
                subtitle="Indicadores Lead Scoring HIGH, de 'otros productos'",
            ),
            order=self.order,
        )
        self.order += 1  # Increment the order for the next plot element

        # Plot the list of hidden indicators
        self.plot_indicator_list(indicator_product_data=indicators["hidden_indicators"])

        # Hide the menu path after plotting
        self.shimoku.menu_paths.update_menu_path(
            name=self.menu_path,
            hide_path=True,
        )

        # Navigate out of the current menu path
        self.shimoku.pop_out_of_menu_path()

        return True