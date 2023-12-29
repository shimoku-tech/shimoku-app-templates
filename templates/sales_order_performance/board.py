from shimoku_api_python import Client
from utils.utils import get_data, process_sales_data


class Board:
    """
    A class representing a Dashboard for displaying various data visualizations.

    """

    def __init__(self, shimoku: Client):
        """
        Constructor for the Dashboard class.

        Parameters:
            shimoku (Client): An instance of a Client class for Shimoku API interactions.
        """

        file_names = ["data/sales_orders_performance.csv"]
        self.board_name = "FP-Sales Order Performance"  # Name of the dashboard
        self.df = get_data(file_names)
        self.shimoku = shimoku  # Shimoku client instance
        self.shimoku.set_board(name=self.board_name)  # Setting up the board in Shimoku
        self.results = None  # Placeholder for storing processed data

    def transform(self):
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df = self.df["sales_orders_performance"]

        # Process sales data
        (
            income_total,
            spend_total,
            net_profit,
            average_profit_per_order,
            net_profit_by_month,
        ) = process_sales_data(df)

        # Store processed data in results attribute
        self.results = {
            "income_total": income_total,
            "spend_total": spend_total,
            "net_profit": net_profit,
            "average_profit_per_order": average_profit_per_order,
            "net_profit_by_month": net_profit_by_month,
        }

        return True

    def plot(self):
        """
        Plot the dashboard.

        This method initializes and calls the plot method of a specific path
        class responsible for plotting the Sales Order Performance dashboard.

        Returns:
        None. The function is used for its side effect of plotting data.
        """

        from paths.sales_order_perfomance import SalesOrderPerformance

        sales_order_performance = SalesOrderPerformance(self)
        sales_order_performance.plot()
