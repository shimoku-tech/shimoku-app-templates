from utils.paths.predictions import PredictionsPage
from utils.paths.IA_insights import InsightsPage
from utils.paths.IA_insights_filters import InsightsPageFilters
from utils.paths.IA_insights_filters_A import InsightsPageFiltersA


def plot_dashboard(shimoku):
    """
    Plot a dashboard for a given Shimoku client instance.

    Args:
        shimoku (Shimoku.Client): The Shimoku client instance to work with.

    This function sets up a dashboard for a specified board in Shimoku using
    the provided client instance and computes predictions using the
    PredictionsPage class.
    """
    # Define the name of the dashboard board.
    board_name = "Cross Selling"

    # Set the current board in Shimoku to the specified board name.
    shimoku.set_board(name=board_name)

    # Get the board object for the specified board name.
    board = shimoku.boards.get_board(name=board_name)

    # Create an instance of the PredictionsPage class, passing the Shimoku client
    # instance and the board object as arguments.
    # pp = PredictionsPage(shimoku, board)
    # pp.compute()

    # ia = InsightsPage(shimoku, board)
    # ia.compute()

    # iaf = InsightsPageFilters(shimoku, board)
    # iaf.compute()

    iaf_a = InsightsPageFiltersA(shimoku, board)
    iaf_a.compute()
