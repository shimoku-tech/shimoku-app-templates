from shimoku_api_python import Client
from utils.utils import get_data, compute_percent
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


        # Delivery Emails
        df_delivery_emails = [
            {
                "name": "Entregados",
                "value" : df_email[df_email["rebound_flag"]==False].shape[0],
                "percentage": compute_percent(
                    df_email[df_email["rebound_flag"]==False].shape[0],
                    df_email.shape[0]
                ),
            },
            {
                "name": "Rebotados",
                "value" : df_email[df_email["rebound_flag"]].shape[0],
                "percentage": compute_percent(
                    df_email[df_email["rebound_flag"]].shape[0],
                    df_email.shape[0]
                ),
            }
        ]

        # Main KPIs
        main_kpis = [
            # Total users
            {
                "title": "Open Rate",
                "value": 0,
            },
        ]


        # Saved as Dataframe to plot
        self.df_app = {
            "models": df_model,
            "delivery_emails": pd.DataFrame(df_delivery_emails),
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
        from paths.modelA import ModelA
        from paths.modelB import ModelB

        # OverView
        EM = EmailMarketingPerformance(self)
        EM.plot()

        # Model A
        MA = ModelA(self)
        MA.plot()

        # Model B
        MB = ModelB(self)
        MB.plot()
