from utils.components import Components
from board import Board


class ModelA(Board, Components):
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
        self.menu_path = "Model A"

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the Email Marketing Performance pag e.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header(self.menu_path)
        self.plot_title_section("PUNTO DE PARTIDA")
        self.plot_description_section("A")
        self.plot_dates_secuence()
        self.plot_resumen("delivery_emails")
        self.plot_pie("Contactos Realizados", "delivery_emails")
        self.plot_title_section("RESULTADOS")
        self.plot_results()
        self.plot_title_section("REPRESENTACIÓN GRÁFICA")
        self.plot_pie("Open Rate", "delivery_emails")
        self.plot_pie("Click Rate", "delivery_emails")
        self.plot_pie("Answer Rate", "delivery_emails")
        self.plot_pie("Rebound Rate", "delivery_emails")
