# Core python libraries
from os import getenv
import argparse

# Third party
from shimoku_api_python import Client

# Local imports
from layout import plot_dashboard
from dotenv import load_dotenv

from transformations.get_predictions_table import get_predictions_table

from dotenv import load_dotenv

if __name__ == "__main__":
    # Load env variables
    load_dotenv()

    # Create the client
    api_key: str = getenv("API_TOKEN")
    config = {
        "access_token": api_key,
    }

    shimoku = Client(
        config=config,
        universe_id=getenv("UNIVERSE_ID"),
        verbosity="INFO",
        async_execution=True,
    )

    shimoku.set_workspace(getenv("WORKSPACE_ID"))

    shimoku.workspaces.delete_all_workspace_menu_paths(uuid=getenv("WORKSPACE_ID"))
    shimoku.workspaces.delete_all_workspace_boards(uuid=getenv("WORKSPACE_ID"))
    
    # Tranfromations
    get_predictions_table()

    plot_dashboard(shimoku)

    # Execute all plots in asynchronous mode
    shimoku.activate_async_execution()
    shimoku.run()
