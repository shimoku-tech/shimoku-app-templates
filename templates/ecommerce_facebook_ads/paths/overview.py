from board import Board
import pandas as pd
from io import StringIO
from utils import beautiful_indicator


class Overview(Board):
    """
    This path is responsible for rendering the overview page.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the HiddenIndicatorsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.df_app

        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Ad Metrics"  # Set the menu path for this page

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)
        
        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the overview page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_kpi_indicators()
        self.plot_kpi_ad_reach()
        self.plot_kpi_ad_clicks()


    def plot_header(self):
        """
        Plots the header section.

        Returns:
            True if the operation is successful.
        """

        title = "Facebook Ads Dashboard"

        indicator = beautiful_indicator(title=title)
        self.shimoku.plt.html(
            indicator,
            order=self.order,
            rows_size=1,
            cols_size=12
        )

        self.order += 1

        return True


    def plot_kpi_indicators(self):
        """
        Plot the Key Performance Indicators (KPI) section of the dashboard.

        Returns:
            True if the operation is successful.
        """
        ad_spend = self.df_app["ad_spend"]
        cpm = self.df_app["cpm"]
        cpc = self.df_app["cpc"]
        ctr = self.df_app["ctr"]

        # Display indicators
        indicator_data = [
            {
                "title": "Ad Spend",
                "description":"vs previous year",
                "align": "center",
                "value": f"${ad_spend}",
                "color":"black"
            },
            {
                "title": "Cost Per Thousand (CPM)",
                "description":"vs previous year",
                "align": "center",
                "value": f"${cpm}",
                "color":"black"
            },
            {
                "title": "Cost Per Click (CPC)",
                "description":"vs previous year",
                "align": "center",
                "value": f"${cpc}",
                "color":"black"
            },
            {
                "title": "Click-Through Rate (CTR)",
                "description":"vs previous year",
                "align": "center",
                "value": f"{ctr}%",
                "color":"black"
            }
        ]

        self.shimoku.plt.indicator(
            data=indicator_data, order=self.order
        )

        self.order += len(indicator_data)
        return True


    def plot_kpi_ad_reach(self):
        """
        Plots a stacked bar for Ad Reach KPI

        Returns:
            True if the operation is successful.
        """
        ad_reach = self.df_app["ad_name_by_month"]

        self.shimoku.plt.stacked_bar(
            data = ad_reach, x="month",
            order=self.order, title="Ad Reach",
            rows_size=2,cols_size=6
        )

        self.order += 1
        return True


    def plot_kpi_ad_clicks(self):
        """
        Plots a line for Ad Clicks KPI

        Returns:
            True if the operation is successful.
        """
        ad_clicks = self.df_app["ad_clicks"]

        self.shimoku.plt.line(
            data=ad_clicks,x="impression_date",order=self.order,
            rows_size=2,cols_size=6,title="Ad Clicks",variant="clean"
        )

        self.order += 1
        return True