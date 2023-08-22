# Core python libraries
from os import getenv

# Third party
from shimoku_api_python import Client

# Local imports
from layout import plot_dashboard

if __name__ == "__main__":

    # Create the client
    s = Client(
        access_token=getenv('API_TOKEN'),
        universe_id=getenv('UNIVERSE_ID'),
        verbosity='INFO',
        async_execution=False,
    )
    s.set_workspace(getenv('WORKSPACE_ID'))
    s.set_board('Revenue')
    plot_dashboard(s)

    # Execute all plots in asynchronous mode
    s.run()

