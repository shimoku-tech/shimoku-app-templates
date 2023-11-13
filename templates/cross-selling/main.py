import argparse

from os import getenv
from shimoku_api_python import Client
from dotenv import load_dotenv

from transformations.get_predictions_table import get_predicted_opportunities
from dashboard import Dashboard

if __name__ == "__main__":

    # Load env variables
    load_dotenv()

    # Create the client
    shimoku = Client(
        access_token=getenv("API_TOKEN"),
        universe_id=getenv("UNIVERSE_ID"),
        verbosity="INFO",
    )
    shimoku.set_workspace(getenv("WORKSPACE_ID"))

    # Delete all the boards and menu paths
    shimoku.workspaces.delete_all_workspace_menu_paths(uuid=getenv("WORKSPACE_ID"))
    shimoku.workspaces.delete_all_workspace_boards(uuid=getenv("WORKSPACE_ID"))

    # Instantiate the dashboard
    x = Dashboard(shimoku)
    # Perform the transformations to predict opportunities
    x.transform()
    # Plot the dashboard
    x.plot()
    