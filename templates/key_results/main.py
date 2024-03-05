from os import getenv
from dotenv import load_dotenv

from shimoku import Client

from board import Board

def main():
    # Load .env file
    load_dotenv()

    # Client connection
    shimoku = Client(
        access_token=getenv('API_TOKEN'),
        universe_id=getenv('UNIVERSE_ID'),
        async_execution=True,
        verbosity="INFO",
    )

    shimoku.set_workspace(uuid=getenv('WORKSPACE_ID'))

    # Set Dashboard object
    board = Board(shimoku)
    board.transform()
    board.plot()

    shimoku.run()


if __name__ == "__main__":
  main()
