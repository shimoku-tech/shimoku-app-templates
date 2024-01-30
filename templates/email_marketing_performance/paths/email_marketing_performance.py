from utils.utils import convert_dataframe_to_array, beautiful_header
from board import Board


class EmailMarketingPerformance(Board):
    """
    This path is responsible for rendering the Email Marketing Performance page.
    """

    def __init__(self, self_board: Board):
        """
        Initializes EmailMarketingPerformance instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.df_app

        # Initialize order of plotting elements
        self.order = 0
        # Set the menu path for this page
        self.menu_path = "Email Marketing Performance"

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the Email Marketing Performance page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_kpi_indicators()

    def plot_header(self) -> bool:
        """Header plot of the menu path

        Returns:
            bool: Execution status
        """
        title = "Email Marketing Performance"

        self.shimoku.plt.html(
            beautiful_header(title=title),
            order = self.order,
            rows_size = 1,
            cols_size = 12,
        )
        self.order += 1

        return True

    def plot_kpi_indicators(self) -> bool:
        """Indicatos plot of Main KPIs

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.indicator(
            data = convert_dataframe_to_array(self.df_app["main_kpis"]),
            order = self.order,
            rows_size = 1,
            cols_size = 12,
            value = "value",
            header = "title",
            footer = "description",
            color = "color",
            align = "align",
        )
        self.order += len(self.df_app["main_kpis"]) + 1

        return True