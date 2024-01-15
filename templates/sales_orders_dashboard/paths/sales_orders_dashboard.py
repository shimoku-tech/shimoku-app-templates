import shimoku_api_python
from board import Board
from utils.components import create_title_name_head
from utils.utils import get_column_name_by_value
import pandas as pd


class SalesOrdersDashboard(Board):
    """
    This class represents a Sales Orders Dashboard.
    It inherits from the Board class.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the SalesOrdersDashboard instance.

        Args:
            self_board (Board): An instance of the Board class.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.results
        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Sales Orders Dashboard"

        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the Sales Orders Dashboard.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_kpi_indicators()
        self.plot_sales_growth_by_market_segment()
        self.plot_sales_national_vs_international()

    def plot_header(self):
        """
        Plot the header section of the dashboard.

        Returns: True if the operation is successful.
        """
        self.shimoku.plt.html(
            html=create_title_name_head(
                title="Sales Orders Dashboard",
                subtitle="",
            ),
            order=self.order,
        )

        # Increment the order
        self.order += 1
        return True

    def plot_kpi_indicators(self):
        """
        Plot the Key Performance Indicators (KPI) section of the dashboard.

        Returns:
            bool: True if the operation is successful.
        """
        # Extract KPI data from the DataFrame
        total_accounts = self.df_app["Total Accounts"]
        orders_per_month = self.df_app["Orders per Month"]
        average_spend_per_order = self.df_app["Average spend per order"]
        growth_rate = self.df_app["Growth Rate"]

        # Prepare data for KPI indicators
        kpi_data = [
            {
                "title": get_column_name_by_value(self.df_app, total_accounts),
                "align": "center",
                "value": f"{round(total_accounts, 0)}",
                "color": "default",
            },
            {
                "title": get_column_name_by_value(self.df_app, orders_per_month),
                "align": "center",
                "value": f"{round(orders_per_month, 0)}",
                "color": "default",
            },
            {
                "title": get_column_name_by_value(self.df_app, average_spend_per_order),
                "align": "center",
                "value": f"${round(average_spend_per_order, 0)}",
                "color": "default",
            },
            {
                "title": get_column_name_by_value(self.df_app, growth_rate),
                "align": "center",
                "value": f"{round(growth_rate, 2)}%",
                "color": "default",
            },
        ]

        # Plot the KPI indicators
        self.shimoku.plt.indicator(data=kpi_data, order=self.order, color="color")

        # Increment the order
        self.order += len(kpi_data)

        return True

    def plot_sales_growth_by_market_segment(self):
        """
        Plot the Sales Growth by Market Segment section of the dashboard.

        Returns:
            bool: True if the operation is successful.
        """
        # Extract sales growth by market segment data from the DataFrame
        sales_growth_by_market_segment = self.df_app["Sales Growth by Market Segment"]

        # Pivot the data for better visualization
        sales_growth_by_market_segment_processed = sales_growth_by_market_segment.pivot(
            index="month", columns="market_segment", values="order_spend"
        ).reset_index()

        # Plot the line chart for sales growth by market segment
        self.shimoku.plt.line(
            data=sales_growth_by_market_segment_processed,
            x="month",
            order=self.order,
            cols_size=6,
            title=get_column_name_by_value(self.df_app, sales_growth_by_market_segment),
            option_modifications={
                "dataZoom": {"show": True},
                "toolbox": {"show": True},
            },
        )

        # Increment the order
        self.order += 1

        return True

    def plot_sales_national_vs_international(self):
        """
        Plot the Sales National vs. International section of the dashboard.

        Returns: True if the operation is successful.
        """

        # Extract the "Sales National vs. International" data from the DataFrame
        sales_national_vs_international = self.df_app["Sales National vs International"]

        # Pivot the data for better visualization
        sales_national_vs_international_processed = (
            sales_national_vs_international.pivot(
                index="month", columns="geo_segment", values="order_spend"
            ).reset_index()
        )

        # Plot the line chart for sales national vs. international
        self.shimoku.plt.line(
            data=sales_national_vs_international_processed,
            x="month",
            order=self.order,
            cols_size=6,
            title=get_column_name_by_value(
                self.df_app, sales_national_vs_international
            ),
            option_modifications={
                "dataZoom": {"show": True},
                "toolbox": {"show": True},
            },
        )

        # Increment the order
        self.order += 1

        return True
