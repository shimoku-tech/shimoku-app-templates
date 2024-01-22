from shimoku_api_python import Client
from utils.utils import get_data, process_sales_data


class Board:
    """
    A class representing a Dashboard for displaying various data visualizations.

    """

    def __init__(self, shimoku: Client):
        """
        Constructor for the Dashboard class.

        Args:
            shimoku (Client): An instance of a Client class for Shimoku API interactions.
        """

        file_names = ["data/sales_orders.csv"]
        self.board_name = "Ecommerce"  # Name of the dashboard
        self.df = get_data(file_names)
        self.shimoku = shimoku  # Shimoku client instance
        self.shimoku.set_board(name=self.board_name)  # Setting up the board in Shimoku
        self.shimoku.boards.update_board(name=self.board_name, is_public=True)
        self.results = None  # Placeholder for storing processed data

    def transform(self):
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df = self.df["sales_orders"]

        # Process sales data
        results_dict = process_sales_data(df)

        # Store processed data in results attribute
        self.results = results_dict

        return True

    def plot(self):
        """
        Plot the dashboard.

        This method initializes and calls the plot method of a specific path
        class responsible for plotting the Sales Orders Dashboard.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the SalesOrdersDashboard class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the SalesOrdersDashboard class has access to all necessary data
          through the passed instance.
        """

        from paths.sales_orders_dashboard import (
            SalesOrdersDashboard,
        )

        sales_order_performance = SalesOrdersDashboard(self)
        sales_order_performance.plot()
