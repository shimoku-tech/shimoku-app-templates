import argparse
from os import getenv
from shimoku_api_python import Client

# from dotenv import load_dotenv

from board import Board


def main():
    """
    Main function to initialize and plot the dashboard.

    This script initializes a Shimoku client, deletes existing boards and menu paths,
    and then creates and plots a new dashboard.
    """
    # Load environment variables
    # load_dotenv()

    # Create the Shimoku client with necessary credentials
    shimoku = Client(local_port=8080, verbosity="INFO")
    shimoku.set_workspace()

    # Instantiate and set up the dashboard
    board = Board(shimoku)
    board.transform()  # Perform data transformations
    board.plot()  # Plot the dashboard


if __name__ == "__main__":
    main()
