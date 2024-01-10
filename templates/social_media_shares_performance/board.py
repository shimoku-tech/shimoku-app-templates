from shimoku_api_python import Client
from utils.utils import get_data
import pandas as pd
import calendar

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

        file_names = ["data/social_media_shares.csv"]
        # Name of the dashboard
        self.board_name = "eCommerce"
        # Get the data from CSV file
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

        df_social_media = self.dfs["social_media_shares"]

        # Main KPIs
        main_kpis = [
            # Total Facebook Shares
            {
                "title": "Facebook Shares",
                "value": df_social_media[
                    df_social_media["post_social_media"] == "Facebook"
                ]["post_shares"].sum(),
                "color": "default",
                "align": "center",
            },
            # Total Twitter Retweets
            {
                "title": "Twitter Retweets",
                "value": df_social_media[
                    df_social_media["post_social_media"] == "Twitter"
                ]["post_shares"].sum(),
                "color": "default",
                "align": "center",
            },
            # Total Youtube Shares
            {
                "title": "Youtube Shares",
                "value": df_social_media[
                    df_social_media["post_social_media"] == "YouTube"
                ]["post_shares"].sum(),
                "color": "default",
                "align": "center",
            },
        ]

        # Social Media Post
        social_media_posts = [
            {
                "Month": calendar.month_name[month][:3],
                "Facebook": df_social_media[
                    (df_social_media["post_date"].dt.month == month) &
                    (df_social_media["post_social_media"] == "Facebook")
                ].shape[0],
                "Twitter": df_social_media[
                    (df_social_media["post_date"].dt.month == month) &
                    (df_social_media["post_social_media"] == "Twitter")
                ].shape[0],
                "YouTube": df_social_media[
                    (df_social_media["post_date"].dt.month == month) &
                    (df_social_media["post_social_media"] == "YouTube")
                ].shape[0],
            }
        for month in range(10,13)]

        # Shares by Social Media
        share_by_social_media = [
            {
                "Month": calendar.month_name[month][:3],
                "Facebook": df_social_media[
                    (df_social_media["post_date"].dt.month == month) &
                    (df_social_media["post_social_media"] == "Facebook")
                ]["post_shares"].sum(),
                "Twitter": df_social_media[
                    (df_social_media["post_date"].dt.month == month) &
                    (df_social_media["post_social_media"] == "Twitter")
                ]["post_shares"].sum(),
                "YouTube": df_social_media[
                    (df_social_media["post_date"].dt.month == month) &
                    (df_social_media["post_social_media"] == "YouTube")
                ]["post_shares"].sum(),
            }
        for month in range(1,13)]

        # Dictionary of the dataframes
        self.df_app = {
            "main_kpis": pd.DataFrame(main_kpis),
            "social_media_posts": pd.DataFrame(social_media_posts),
            "share_by_social_media": pd.DataFrame(share_by_social_media),
        }

        return True

    def plot(self):
        """
        A method to plot Social Media Shares Performance.

        This method utilizes the SocialMediaSharesPerformance class from the paths.social_media_shares_performance
        module to create and display a plot related to the social media posts. It assumes that
        SocialMediaSharesPerformance requires a reference to the instance of the class from which
        this method is called.

        Args:
        self: A reference to the current instance of the class.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the SocialMediaSharesPerformance class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the SocialMediaSharesPerformance class has access to all necessary data
          through the passed instance.
        """

        from paths.social_media_shares_performance import SocialMediaSharesPerformance

        UO = SocialMediaSharesPerformance(self)
        UO.plot()
