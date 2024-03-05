from utils.utils import (
    beautiful_header,
    get_table_color_range_numerical,
    get_table_color_range_categorical,
    get_columns_options,
)
from board import Board

class Fase2:
    """
    This path is responsible for rendering the Pizza Sales page.
    """

    def __init__(self, board: Board):
        """
        Initializes the OKR with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        self.df_app = board.df_app

        self.shimoku = board.shimoku

        # Initialize order of plotting elements
        self.order = 0
        # Set the menu path for this page
        self.menu_path = "Overview Fase 2"

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)


    def __str__(self) -> str:
        return f"Dashboard {self.menu_path}"


    def plot(self):
        """
        Plots the Pizza Sales page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_indicators()
        self.plot_indicators_gauge()
        self.plot_table_frequency()
        self.plot_table_sdk_version()
        self.plot_table_template()

    def plot_header(self) -> bool:
        """Header plot of the menu path

        Returns:
            bool: Execution status
        """
        title = "OBJ-1 OKR-2"
        indicator = beautiful_header(title=title)
        self.shimoku.plt.html(
            indicator,
            order=self.order,
            rows_size=1,
            cols_size=10,
            padding="0,1,0,1",
        )
        self.order += 1

        return True

    def plot_indicators(self) -> bool:
        """Plot indicator chart for Total Sales, Total Pizzas, Total Orders, Avg. Pizzas/day and Avg. Orders/day

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.indicator(
            data = self.df_app["main_kpis"],
            order = self.order,
            rows_size = 1,
            cols_size = 8,
            padding='0,0,0,1',
        )

        self.order += len(self.df_app["main_kpis"]) + 1

    def plot_indicators_gauge(self) -> bool:
        data = self.df_app["okr_value"]
        self.shimoku.plt.shimoku_gauge(
            value=int(data["value"]),
            order=self.order,
            rows_size=1,
            cols_size=2,
            name=data["title"],
            color=data["color"],
            padding='0,1,0,0',
            is_percentage=True,
        )
        self.order += 1

        return True

    def plot_table_frequency(self) -> bool:
        self.shimoku.plt.table(
            data=self.df_app["frequency"],
            order=self.order,
            cols_size = 5,
            rows_size = 4,
            page_size=10,
            page_size_options = [3, 5, 10],
            initial_sort_column = "frequency",
            sort_descending = True,
            categorical_columns = ["chart_name"],
            label_columns={
                ("chart_name", "outlined"): get_table_color_range_categorical(self.df_app["frequency"]),
                ("frequency", "outlined"): get_table_color_range_numerical(self.df_app["frequency"])
            },
            columns_options = {
                "chart_name": {"width": 200},
                "frequency": {"width": 250},
            },
            export_to_csv=False,
            padding="0,0,0,1",
        )
        self.order += 1

        return True

    def plot_table_sdk_version(self) -> bool:
        self.shimoku.plt.table(
            data=self.df_app["sdk_version"],
            order=self.order,
            cols_size = 5,
            rows_size = 4,
            page_size=10,
            page_size_options = [3, 5, 10],
            initial_sort_column = "SDK version",
            sort_descending = True,
            categorical_columns = ["SDK version"],
            columns_options = {
                "SDK version": {"width": 150},
                "Available charts": {"width": 150},
                "Charts used": {"width": 150},
                "Percentage used (%)": {"width": 220},
            },
            export_to_csv=False,
            padding="0,1,0,0",
        )
        self.order += 1

        return True

    def plot_table_template(self) -> bool:
        self.shimoku.plt.table(
            data=self.df_app["templates"],
            order=self.order,
            cols_size = 10,
            rows_size = 4,
            page_size=10,
            page_size_options = [3, 5, 10],
            initial_sort_column = "title",
            sort_descending = True,
            categorical_columns = [
                "title",
                "type",
                "stakeholder",
                "public",
                "version",
            ],
            columns_options = get_columns_options(self.df_app["templates"]),
            export_to_csv=False,
            padding="0,1,0,1",
        )
        self.order += 1

        return True