from board import Board
from utils.components import create_title_name_head, format_raw_options
from typing import Dict, Any, List, Union


class RetailerDashboard(Board):
    """
    This class represents the retailer dashboard.
    It inherits from the Board class.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the RetailerDashboard object.

        Args:
            self_board (Board): The Board object containing data.

        """
        super().__init__(self_board.shimoku)
        self.df_app = (
            self_board.results
        )  # Assuming results are stored in self_board.results
        self.order = 0
        self.menu_path = "Store Overview"
        self.tabs_group_name = "Temporality"
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the dashboard in the specified order.
        """
        self.plot_header()
        self.plot_kpi_indicators()
        self.create_tabs()
        self.plot_tabs("Current Week")
        self.plot_tabs("Current Month")
        self.plot_tabs("Current Year")

    def plot_header(self) -> bool:
        """
        Creates and plots the dashboard header.

        Returns:
            bool: True if the operation is successful.
        """
        title_html = create_title_name_head(title="Store Overview", subtitle="")
        self.shimoku.plt.html(html=title_html, order=self.order)
        self.order += 1
        return True

    def plot_kpi_indicators(self) -> bool:
        """
        Plots the KPI (Key Performance Indicator) indicators section.

        Returns:
            bool: True if the operation is successful.
        """

        kpi_data: List[Dict[str, Union[str, Any]]] = []

        # Define the columns of interest
        columns = ["Stores", "Total Sales", "Average Sales", "Users", "Average Sales "]

        for column in columns:
            valor = self.df_app[column]["Value"]
            description = self.df_app[column]["Description"]

            # Add a new dictionary element for each column
            kpi_data.append(
                {
                    "title": column,
                    "align": "center",
                    "value": f"{round(valor, 0)}" + (" €" if "Sales" in column else ""),
                    # Add "€" only to sales columns
                    "color": "default",
                    "description": description,
                }
            )

        # Plot the KPI indicators
        self.shimoku.plt.indicator(
            data=kpi_data, order=self.order, rows_size=1, cols_size=12
        )
        self.order += len(kpi_data)
        return True

    def create_tabs(self) -> bool:
        """
        Creates the tabs for switching between temporalities.

        Returns:
            bool: True if the operation is successful.
        """

        tabs = ["Current Week", "Current Month", "Current Year"]
        self.shimoku.plt.set_tabs_index(
            (self.tabs_group_name, tabs[0]),
            order=self.order,
            just_labels=True,
        )
        for tab_name in tabs[1::]:
            self.shimoku.plt.change_current_tab(tab_name)

        self.order += 1
        return True

    def plot_tabs(self, temporality: str) -> bool:
        """
        Plots the data for the specified temporality.

        Args:
            temporality (str): The selected temporality (e.g., "Current Week").

        Returns:
            bool: True if the operation is successful.
        """

        self.shimoku.plt.change_current_tab(temporality)
        self.order = 0
        self.plot_sales_by_store(temporality)
        self.plot_sales_percentage_by_store(temporality)
        self.plot_sales_accumulated_by_store(temporality)

        self.shimoku.plt.set_tabs_index(tabs_index=(self.tabs_group_name, temporality))
        return True

    def plot_sales_by_store(self, temporality: str) -> bool:
        """
        Plots the sales by store data.

        Args:
            temporality (str): The selected temporality (e.g., "Current Week").

        Returns:
            bool: True if the operation is successful.
        """

        sales_by_store = self.df_app["Sales Users by Store"][temporality]
        self.shimoku.plt.free_echarts(
            raw_options=format_raw_options(sales_by_store),
            order=self.order,
            rows_size=4,
            cols_size=12,
            title="Sales Users by Store",
        )
        self.order += 1
        return True

    def plot_sales_percentage_by_store(self, temporality: str) -> bool:
        """
        Plots the sales percentage by store data.

        Args:
            temporality (str): The selected temporality (e.g., "Current Week").

        Returns:
            bool: True if the operation is successful.
        """
        sales_percentage_by_store = self.df_app["Sales Percentage by Store"][
            temporality
        ]
        self.shimoku.plt.pie(
            data=sales_percentage_by_store,
            order=self.order,
            names="store_id",
            values="sales_amount",
            title="Sales by Store (%)",
            rows_size=3,
            cols_size=4,
        )
        self.order += 1
        return True

    def plot_sales_accumulated_by_store(self, temporality: str) -> bool:
        """
        Plots the accumulated sales by store data.

        Args:
            temporality (str): The selected temporality (e.g., "Current Week").

        Returns:
            bool: True if the operation is successful.
        """
        sales_accumulated_by_store = self.df_app["Sales Accumulated by Store"][
            temporality
        ]
        self.shimoku.plt.line(
            data=sales_accumulated_by_store,
            order=self.order,
            x=temporality,
            title="Sales by Store (Accumulated)",
            rows_size=3,
            cols_size=8,
        )
        self.order += 1
        return True
