from shimoku_api_python import Client
from utils.utils import get_data
import pandas as pd
import datetime as dt
import numpy as np

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

        file_names = ["data/client.csv", "data/email.csv", "data/model.csv"]
        # Name of the dashboard
        self.board_name = "Email Marketing Performance"
        # Get data from CSV files
        self.dfs = get_data(file_names)
        # Shimoku client instance
        self.shimoku = shimoku
        # Setting up the board in Shimoku
        self.shimoku.set_board(name=self.board_name)
        # Make the board public
        self.shimoku.boards.update_board(name=self.board_name, is_public=True)

    def transform(self) -> bool:
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df_client = self.dfs["client"]
        df_model = self.dfs["model"]
        df_email = self.dfs["email"]


        # Main KPIs
        main_kpis = [
            # Total users
            {
                "title": "Users",
                "description": "Total Users",
                "value": 0,
                "color": "default",
                "align": "center",
            },
        ]


        # Saved as Dataframe to plot
        self.df_app = {
            "main_kpis": pd.DataFrame(main_kpis),
        }

        return True

    def plot(self):
        """
        A method to plot Email Marketing Performance.

        This method utilizes the EmailMarketingPerformance class from the paths.email_marketing_performance
        module to create and display a plot related to the user. It assumes that
        EmailMarketingPerformance requires a reference to the instance of the class from which
        this method is called.

        Args:
        self: A reference to the current instance of the class.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the EmailMarketingPerformance class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the EmailMarketingPerformance class has access to all necessary data
          through the passed instance.
        """

        from paths.email_marketing_performance import EmailMarketingPerformance

        EM = EmailMarketingPerformance(self)
        EM.plot()
