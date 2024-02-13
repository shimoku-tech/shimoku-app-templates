from shimoku_api_python import Client
from utils.utils import (
    get_data,
    genenerate_data_by_campaign,
    generate_tables_by_campaign,
)
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

        file_names = [
            "data/campaign.csv",
            "data/model.csv",
            "data/client.csv",
            "data/campaign_model.csv",
            "data/email.csv",
        ]
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

        # if self.shimoku.boards.get_board(name=self.board_name):
        #     self.shimoku.boards.remove_all_menu_paths_from_board(name=self.board_name)

    def transform(self) -> bool:
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df_campaign = self.dfs["campaign"]
        df_model = self.dfs["model"]
        df_client = self.dfs["client"]
        df_campaign_model = self.dfs["campaign_model"]
        df_email = self.dfs["email"]

        dataframe_general_name = ["overview", "open", "click", "answer", "rebound"]

        dfs_overview = genenerate_data_by_campaign(df_email)

        dfs_campaign = {}
        for _, row in df_campaign_model.iterrows():
            df_email_filter = df_email[df_email["id_campaign_model"] == row["id"]]
            df_client_filter = df_client[df_client["id"].isin(df_email_filter["id_client"].unique())]

            df_table_open, df_table_click = generate_tables_by_campaign(df_client_filter, df_email)
            dfs_campaign |= {
                row["id"] : genenerate_data_by_campaign(df_email_filter)
            }
            dfs_campaign |= {
                f"table_open_{row['id']}" : df_table_open,
                f"table_click_{row['id']}" : df_table_click,
            }


        # Saved as Dataframe to plot
        self.df_app = {
            "campaign": df_campaign,
            "model": df_model,
            "campaign_model": df_campaign_model,
        }

        self.df_app |= {
            section: pd.DataFrame(dfs_overview[section])
        for section in dataframe_general_name}

        self.df_app |= {
            f"{row['id_campaign']}_{row['id_model']}_{section}": pd.DataFrame(dfs_campaign[row["id"]][section])
        for section in dataframe_general_name for _, row in df_campaign_model.iterrows()}
        self.df_app |= {
            f"{row['id_campaign']}_{row['id_model']}_table_{table}": dfs_campaign[f"table_{table}_{row['id']}"]
        for table in ["open", "click"] for _, row in df_campaign_model.iterrows()}

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
        from paths.campaign import Campaign

        # OverView
        EM = EmailMarketingPerformance(self)
        EM.plot()

        df_campaign = self.dfs["campaign"]
        for _, row in df_campaign.iterrows():
            # Campaign
            CM = Campaign(self, row["id"], row["name"])
            CM.plot()
