from os import getenv
from dotenv import load_dotenv
import pandas as pd

from shimoku import Client

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