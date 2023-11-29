from shimoku_api_python import Client
from utils.utils import get_data
import pandas as pd
from datetime import datetime, timedelta


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

        file_names = ["data/active_users.csv"]
        self.board_name = "SaaS Template"  # Name of the dashboard
        self.dfs = get_data(file_names)
        self.shimoku = shimoku  # Shimoku client instance
        self.shimoku.set_board(name=self.board_name)  # Setting up the board in Shimoku

    def transform(self):
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df = self.dfs["active_users"]

        main_kpis = [
            {
                "title": "Registered Users",
                "description": "Total of registered users",
                "value": len(df[df["unregister_date"].isnull()]),
                "color": "success",
                "align": "center",
            },
            {
                "title": "Active Users 24h",
                "description": "Active Users on last 24h",
                "value": len(
                    df[df["last_login_date"] >= (datetime.now() - timedelta(days=1))]
                ),
                "color": "success",
                "align": "center",
            },
            {
                "title": "WAU",
                "description": "Weekly Active Users",
                "value": len(
                    df[df["last_login_date"] >= (datetime.now() - timedelta(days=7))]
                ),
                "color": "success",
                "align": "center",
            },
            {
                "title": "MAU",
                "description": "Monthly Active Users",
                "value": len(
                    df[df["last_login_date"] >= (datetime.now() - timedelta(days=30))]
                ),
                "color": "success",
                "align": "center",
            },
            {
                "title": "New Users",
                "description": "New Users in the last 30 days",
                "value": len(
                    df[df["register_date"] >= (datetime.now() - timedelta(days=30))]
                ),
                "color": "success",
                "align": "center",
            },
            {
                "title": "Subscribers",
                "description": "Total active newsletter subscribers",
                "value": len(
                    df[
                        (df["subscription_date"].notnull())
                        & (df["unsubscription_date"].isnull())
                        & (df["unregister_date"].isnull())
                    ]
                ),
                "color": "success",
                "align": "center",
            },
        ]

        self.df_app = {"main_kpis": pd.DataFrame(main_kpis)}

        return True

    def plot(self):
        """
        A method to plot user overview.

        This method utilizes the UserOverview class from the paths.user_overview
        module to create and display a plot related to the user. It assumes that
        UserOverview requires a reference to the instance of the class from which
        this method is called.

        Args:
        self: A reference to the current instance of the class.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the UserOverview class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the UserOverview class has access to all necessary data
          through the passed instance.
        """

        from paths.user_overview import UserOverview

        UO = UserOverview(self)
        UO.plot()
