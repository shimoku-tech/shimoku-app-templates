import shimoku_api_python as Shimoku

from utils.layout import plot_dashboard
from utils.settings import (
    access_token,
    universe_id,
    workspace_id,
)

# Check if this script is being run as the main program.
if __name__ == "__main__":
    # Main function to run the app.

    # Create a Shimoku Client instance.
    s = Shimoku.Client(
        access_token=access_token,
        universe_id=universe_id,
        verbosity='INFO',
    )

    # Set the workspace for the Shimoku Client using the provided UUID.
    s.set_workspace(uuid=workspace_id)

    # Delete all workspace menu paths associated with the provided UUID.
    s.workspaces.delete_all_workspace_menu_paths(uuid=workspace_id)

    # Plot the dashboard using the Shimoku Client instance.
    plot_dashboard(s)
