from os import getenv
from dotenv import load_dotenv
import pandas as pd

from shimoku import Client

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

    chart_name = "chart_name"
    dict_charts_name = {
        chart_name : dir(shimoku.plt)
    }

    dict_charts_name[chart_name] = [name for name in dict_charts_name[chart_name] if not name.startswith("_")]
    df_charts_name = pd.DataFrame(dict_charts_name)
    df_charts_name = df_charts_name.sort_values(by=[chart_name], key=lambda col: col.str.lower())
    df_charts_name.to_csv("charts_name_SDK.csv", index=False)


if __name__ == "__main__":
    main()