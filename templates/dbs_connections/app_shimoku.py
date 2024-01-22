from os import getenv
from dotenv import load_dotenv
import shimoku_api_python as shimoku


def init_sdk() -> shimoku.Client:
    # Load environment variables
    load_dotenv()
    
    api_key: str = getenv('API_TOKEN')
    universe_id: str = getenv('UNIVERSE_ID')
    workspace_id: str = getenv('WORKSPACE_ID')
    async_exec: bool = getenv('ASYNC_EXECUTION') == 'TRUE'

    shimoku_client = shimoku.Client(
        access_token=api_key,
        universe_id=universe_id,
        verbosity='INFO',
        async_execution=async_exec,
    )

    shimoku_client.set_workspace(workspace_id)

    return shimoku_client
