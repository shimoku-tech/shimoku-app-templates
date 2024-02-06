from os import getenv
from shimoku_api_python import Client
from dotenv import load_dotenv

from board import Board


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
        universe_id=getenv("UNIVERSE_ID"),
        async_execution=True,
        verbosity="INFO",
    )
    shimoku.set_workspace(getenv("WORKSPACE_ID"))

    # Instantiate and set up the dashboard
    board = Board(shimoku)
    # Perform data transformations
    board.transform()
    # Plot the dashboard
    board.plot()

    shimoku.run()


if __name__ == "__main__":
    main()
