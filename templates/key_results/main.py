from os import getenv
from dotenv import load_dotenv

from shimoku import Client

from board import Board

def main():
    # Load .env file
    load_dotenv()

    # Import enrivomental variable
    access_token: str = getenv('SHIMOKU_TOKEN')
    universe_id: str = getenv('UNIVERSE_ID')
    workspace_id: str = getenv('WORKSPACE_ID')

    # Client connection
    shimoku = Client(
        access_token=access_token,
        universe_id=universe_id,
        async_execution=True,
        verbosity="INFO",
    )

    shimoku.set_workspace(uuid=workspace_id)

    # Set Dashboard object
    board = Board(shimoku)
    board.transform()
    board.plot()

    shimoku.run()


if __name__ == "__main__":
  main()
