from utils.utils import convert_dataframe_to_array, beautiful_indicator
from board import Board


class customer_orders_performance(Board):
    """
    This path is responsible for rendering the user overview page.
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
        self.menu_path = "Customer Orders Performance"  # Set the menu path for this page

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the user overview page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_kpi_indicators()

    def plot_kpi_indicators(self):
        order = self.shimoku.plt.indicator(
            data=convert_dataframe_to_array(self.df_app["main_kpis"]),
            order=self.order,
            rows_size=1,
            cols_size=12,
            value="value",
            header="title",
            footer="description",
            color="color",
            align="align",
        )
        self.order += len(self.df_app["main_kpis"]) + 1

        return True
