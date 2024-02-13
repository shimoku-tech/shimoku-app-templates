from utils.utils import get_campaign_model
from utils.components import Components
from board import Board


class Campaign(Components):
    """
    This path is responsible for rendering the Email Marketing Performance page.
    """

    def __init__(self, board: Board, id: str, title: str):
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
        self.menu_path_id = id
        self.menu_path = title

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

        campaign_model = self.df_app["campaign_model"]
        model = self.df_app["model"]

        campaign_model, model = get_campaign_model(self.menu_path_id, model, campaign_model)
        for _, row in model.iterrows():
            self.shimoku.plt.set_tabs_index(
                ("Models", row["name"]),
                order=self.order,
                just_labels=True,
                cols_size = 24,
            )
            self.order += 1

            overview_name = f"{self.menu_path_id}_{row['id']}_overview"
            open_name = f"{self.menu_path_id}_{row['id']}_open"
            click_name = f"{self.menu_path_id}_{row['id']}_click"
            answer_name = f"{self.menu_path_id}_{row['id']}_answer"
            rebound_name = f"{self.menu_path_id}_{row['id']}_rebound"
            table_open = f"{self.menu_path_id}_{row['id']}_table_open"
            table_click = f"{self.menu_path_id}_{row['id']}_table_click"

            self.plot_description_section(row["subject"])

            self.plot_dates_secuence(campaign_model[campaign_model["id_model"] == row["id"]]["delivery_days"])

            self.plot_resumen(overview_name)
            self.plot_pie("Contacts Achieved", overview_name)

            self.plot_results(open_name, click_name, answer_name, rebound_name)

            self.plot_pie("Open Rate", open_name, True, "left")
            self.plot_pie("Click Rate", click_name, True, "right")
            self.plot_pie("Answer Rate", answer_name, True, "left")
            self.plot_pie("Rebound Rate", rebound_name, True, "right")

            self.plot_table(table_open, "Opens")
            self.plot_table(table_click, "Clicks")