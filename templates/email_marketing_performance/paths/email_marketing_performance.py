from utils.components import Components
from board import Board


class EmailMarketingPerformance(Components):
    """
    This path is responsible for rendering the Email Marketing Performance page.
    """

    def __init__(self, board: Board):
        """
        Initializes EmailMarketingPerformance instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        self.shimoku = board.shimoku
        self.df_app = board.df_app

        # Initialize order of plotting elements
        self.order = 0
        # Set the menu path for this page
        self.menu_path = "Overview"

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
        self.plot_header("Email Marketing Performance")

        self.plot_resumen("overview")
        self.plot_pie("Contacts Achieved", "overview", False, "right")

        self.plot_results("open", "click", "answer", "rebound")

        self.plot_pie("Open Rate", "open", True, "left")
        self.plot_pie("Click Rate", "click", True, "right")
        self.plot_pie("Answer Rate", "answer", True, "left")
        self.plot_pie("Rebound Rate", "rebound", True, "right")