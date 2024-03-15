from shimoku_api_python import Client
import pandas as pd


class Board:
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

        self.board_name = "Ecommerce Analysis"
        self.df = pd.read_csv("data/data.csv")
        self.shimoku = shimoku  # Shimoku client instance
        self.shimoku.set_board(name=self.board_name)
        self.shimoku.boards.update_board(name=self.board_name, is_public=True)

    def transform(self):
        pass

    def plot(self):
        from paths.ecomerce_analysis import EcommerceAnalysis
        EA = EcommerceAnalysis(self)
        EA.plot()
