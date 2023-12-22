from os import getenv
from shimoku_api_python import Client
from dotenv import load_dotenv

from board import Board

#from freezegun import freeze_time
#from settings import date

#@freeze_time(date)
def main():
    """
    Main function to initialize and plot the dashboard.

    This script initializes a Shimoku client, deletes existing boards and menu paths,
    and then creates and plots a new dashboard.
    """
    # Load environment variables
    load_dotenv()

    # Create the Shimoku client with necessary credentials
    shimoku = Client(
        access_token=getenv("API_TOKEN"),
        universe_id=getenv("UNIVERSE_SOLUTIONS_ID"),
        verbosity="INFO",
    )
    shimoku.set_workspace(getenv("WORKSPACE_SOLUTIONS_ID"))

    #shimoku.set_board("Sales Product Performance")
    #shimoku.set_menu_path('Diagrams')
    #shimoku.boards.delete_board("Sales Product Performance")
    #shimoku.boards.get_board("Sales Product Performance")

    # Instantiate and set up the dashboard
    board = Board(shimoku)
    board.transform()
    board.plot()




if __name__ == "__main__":
    main()