from shimoku_api_python import Client
from utils.utils import get_data, process_retail_data


class Board:
    """
    A class representing a Retail Overview Dashboard for displaying various data visualizations related to retailers.
    """

    def __init__(self, shimoku: Client):
        """
        Constructor for the Retail Overview Dashboard class.

        Args:
            shimoku (Client): An instance of a Client class for Shimoku API interactions.
        """

        file_names = ["data/retailer_sales_data.csv"]
        self.board_name = "Retailer Template"  # Name of the dashboard
        self.df = get_data(file_names)
        self.shimoku = shimoku  # Shimoku client instance
        self.shimoku.set_board(name=self.board_name)  # Setting up the board in Shimoku
        self.shimoku.boards.update_board(name=self.board_name, is_public=True)
        self.results = None  # Placeholder for storing processed data

    def transform(self):
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the Retail Overview dashboard.
        """

        df = self.df["retailer_sales_data"]

        # Process sales data
        results_dict = process_retail_data(df)

        # Store processed data in results attribute
        self.results = results_dict

        return True

    def plot(self):
        """
        Plot the Retail Overview dashboard.

        This method initializes and calls the plot method of a specific path
        class responsible for plotting the Retail Overview Dashboard.

        Returns:
            None. The function is used for its side effect of plotting data.

        Note:
            - This method imports the RetailOverviewDashboard class within the function scope
              to avoid potential circular dependencies.
            - Ensure that the RetailOverviewDashboard class has access to all necessary data
              through the passed instance.
        """

        from paths.store_overview import (
            RetailerDashboard,
        )

        store_overview = RetailerDashboard(self)
        store_overview.plot_order()
