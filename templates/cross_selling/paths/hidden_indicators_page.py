from dashboard import Dashboard


class HiddenIndicatorsPage(Dashboard):
    """
    A class representing a page of hidden indicators within a dashboard.

    Inherits from the Dashboard class and is used to display indicators that are
    not immediately visible on the main dashboard page.

    Attributes:
        order (int): Order of elements to be plotted.
        menu_path (str): Path of the menu in the dashboard.
    """

    def __init__(self, shimoku):
        """
        Initializes the HiddenIndicatorsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(shimoku)
        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Hidden indicators"  # Set the menu path for this page
        self.shimoku.set_menu_path(name=self.menu_path)  # Set the menu path in Shimoku

    def plot(self):
        """
        Plots the hidden indicators page.

        This method retrieves hidden indicators and plots them on the page.
        It also sets the title and hides the menu path after plotting.
        """
        # Retrieve the board ID using the board name
        board_id = self.shimoku.boards.get_board(name=self.board_name)["id"]
        # Get indicators by business logic
        indicators = self.get_indicators_by_business(board_id)

        # Plot the title for the hidden indicators section
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Other products",
                subtitle="High Lead Scoring Indicators for 'other products'",
            ),
            order=self.order,
        )
        self.order += 1  # Increment the order for the next plot element

        # Plot the list of hidden indicators
        self.plot_indicator_list(indicator_product_data=indicators["hidden_indicators"])

        # Hide the menu path after plotting
        self.shimoku.menu_paths.update_menu_path(
            name=self.menu_path,
            hide_path=True,
        )

        # Navigate out of the current menu path
        self.shimoku.pop_out_of_menu_path()

        return True
