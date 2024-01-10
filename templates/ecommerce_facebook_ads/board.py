from shimoku_api_python import Client
from utils import get_data, groupby_sum
import pandas as pd
import calendar
import numpy as np

class Board:
    """
    A class used to represent a Dashboard for displaying various data visualizations.
    """

    def __init__(self, shimoku: Client):
        """
        The constructor for the Dashboard class.

        Parameters:
            shimoku (Client): An instance of a Client class for Shimoku API interactions.
        """

        file_names = ["data/facebook_ads.csv"]
        # Name of the dashboard
        self.board_name = "Facebook Ads"  
        self.dfs = get_data(file_names)

        # Shimoku client instance
        self.shimoku = shimoku  
        self.shimoku.set_board(name=self.board_name)
        self.shimoku.boards.update_board(name=self.board_name, is_public=True)

    def transform(self):
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df = self.dfs["facebook_ads"]

        # To replace numbers for month names
        month_names = list(calendar.month_abbr)[1:]
        month_dict = {i: abbr_name for i, abbr_name in enumerate(month_names, start=1)}
        
        #Indicators data
        ad_spend = round(df["ad_cost"].sum(),2)
        cpm = round(df["ad_cost"].mean(),2)*1000
        cpc = round((df["ad_cost"].sum())/(df["click"].sum()),2)
        ctr = round((len(df))/(df["click"].sum()),2)

        #Stacked bar data
        df["month"] = df["impression_date"].dt.month
        ad_name_by_month = df.groupby(['month', 'ad_name']).size().reset_index(name='count')
        ad_name_by_month = ad_name_by_month.pivot(index='month', columns='ad_name', values='count').fillna(0).astype(int).reset_index()
        ad_name_by_month["month"] = ad_name_by_month["month"].replace(month_dict)

        #Line data
        ad_clicks = groupby_sum(df,df["impression_date"].dt.month,"click")
        ad_clicks["impression_date"] = ad_clicks["impression_date"].replace(month_dict)


        self.df_app = {
            "ad_spend":ad_spend,
            "cpm":cpm,
            "cpc":cpc,
            "ctr":ctr,
            "ad_name_by_month":ad_name_by_month,
            "ad_clicks":ad_clicks
        }

        return True

    def plot(self):
        """
        A method to plot overview.

        This method utilizes the Overview class from the paths.overview
        module to create and display a plot related to facebook ads. It assumes that
        Overview requires a reference to the instance of the class from which
        this method is called.

        Args:
        self: A reference to the current instance of the class.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the Overview class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the Overview class has access to all necessary data
          through the passed instance.
        """

        from paths.overview import Overview

        overview_path = Overview(self)
        overview_path.plot()
