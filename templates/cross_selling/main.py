import argparse
from os import getenv
from shimoku_api_python import Client
from dotenv import load_dotenv

from transformations.get_predictions_table import get_predicted_opportunities
from dashboard import Dashboard


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
        verbosity="INFO",
    )
    shimoku.set_workspace(getenv("WORKSPACE_ID"))

    # Delete all existing boards and menu paths in the workspace
    shimoku.workspaces.delete_all_workspace_menu_paths(uuid=getenv("WORKSPACE_ID"))
    shimoku.workspaces.delete_all_workspace_boards(uuid=getenv("WORKSPACE_ID"))

    # Instantiate and set up the dashboard
    dashboard = Dashboard(shimoku)
    dashboard.transform()  # Perform data transformations
    dashboard.plot()  # Plot the dashboard


if __name__ == "__main__":
    main()
