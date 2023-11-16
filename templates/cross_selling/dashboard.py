from transformations.get_predictions_table import get_predicted_opportunities
from utils.utils import DFs, format_number
from shimoku_api_python import Client


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
        Plot the dashboard paths.

        This method generates plots for the dashboard paths, including hidden indicators
        and predictions, using the data provided by the `shimoku` object. It calls the
        `plot` method of two separate pages:
            - HiddenIndicatorsPage
            - PredictionsPage

        The importation of the two pages is done within the method to avoid circular
        imports, look for 'lazy importing' for more information.

        Returns:
            bool: True if the plotting is successful, otherwise False.

        """
        # Import necessary modules
        from paths.predictions_page import PredictionsPage
        from paths.hidden_indicators_page import HiddenIndicatorsPage

        # Create an instance of HiddenIndicatorsPage and plot
        hi = HiddenIndicatorsPage(self.shimoku)
        hi.plot()

        # Create an instance of PredictionsPage and plot
        pp = PredictionsPage(self.shimoku)
        pp.plot()

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
