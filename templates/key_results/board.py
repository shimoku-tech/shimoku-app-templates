import pandas as pd

from shimoku import Client
from utils.utils import (
    get_data,
    get_indicator_color,
    get_gauge_color,
    add_new_charts,
    compute_percentage,
)
from pathlib import Path


class Board:
    """
    A class used to represent a Dashboard for displaying various data visualizations.

    Attributes:
        board_name (str): Name of the dashboard.
        dfs (DFs): An instance of a DFs class for handling data frames.
        shimoku (Client): An instance of a Client class for Shimoku API interactions.
    """

    def __init__(self, shimoku: Client):
        """
        The constructor for the Dashboard class.

        Parameters:
            shimoku (Client): An instance of a Client class for Shimoku API interactions.
        """

        path = Path(__file__).parent / "data"
        file_names = ['OBJ-1_KR-2.csv', 'charts_frequency.csv', 'data_templates.csv', 'available_charts_SDK_version.csv']
        file_names = [f"{path}/{filename}" for filename in file_names]

        # Name of the dashboard
        self.board_name = "OBJ-1 OKR-2"
        # Get the data from CSV file
        self.dfs = get_data(file_names)
        # Shimoku client instance
        self.shimoku = shimoku
        # Setting up the board in Shimoku
        self.shimoku.set_board(name=self.board_name)
        # Make the board public
        self.shimoku.boards.update_board(name=self.board_name, is_public=True)

    def transform(self) -> bool:
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        # Get dataframe
        df_okr = self.dfs["OBJ-1_KR-2"]
        df_frequency = self.dfs["charts_frequency"]
        df_templates = self.dfs["data_templates"]
        df_sdk = self.dfs["available_charts_SDK_version"]

        main_kpis = [
            {
                "title": "Analysis date",
                "value": str(df_okr["analysis_date"].dt.date.values[0]),
                "color": "default",
                "align" : "center",
                "variant" : "topColor",
            },
            {
                "title": "Template number",
                "value": df_okr["template_number"].values[0],
                "color": "default",
                "align" : "center",
                "variant" : "topColor",
            },
            {
                "title": "SDK Chart",
                "value": df_okr["SDK_chart_number"].values[0],
                "color": "success",
                "align" : "center",
                "variant" : "topColor",
            },
            {
                "title": "SDK Chart",
                "value": df_okr["template_chart_number"].values[0],
                "color": get_indicator_color(df_okr["value(%)"].values[0]),
                "align" : "center",
                "variant" : "topColor",
            },
        ]

        df_okr_value = {
            "title": df_okr["name"].values[0],
            "value": df_okr["value(%)"].values[0],
            "color": get_gauge_color(df_okr["value(%)"].values[0]),
        }

        df_template_notnull = df_templates[df_templates.version.notna()]
        list_versions = sorted(df_template_notnull["version"].unique())
        avaible_charts = list(df_sdk[df_sdk["sdk_version"].isin(list_versions)]["charts_number"])
        number_charts = []
        for version in list_versions:
            charts = []
            for _, row in df_template_notnull[df_template_notnull["version"] == version].iterrows():
                charts = add_new_charts(charts, row["charts"])
            number_charts.append(len(charts))
        df_sdk_by_version = {
            "SDK version": list_versions,
            "Available charts": avaible_charts,
            "Charts used": number_charts,
            "Percentage used (%)": [
                compute_percentage(total, value)
            for total, value in zip(avaible_charts, number_charts)],
        }

        df_templates["dashboard_url"] = df_templates["dashboard_url"].apply(lambda value: "" if pd.isna(value) else value)
        df_templates["version"] = df_templates["version"].apply(lambda value: "" if pd.isna(value) else value)

        df_templates = df_templates.reindex([
            'title',
            'type',
            'stakeholder',
            'public',
            'charts_number',
            'version',
            'analysis_date',
            'charts',
            'dashboard_url',
            'template_url',
        ], axis=1)
        # Dictionary of the dataframes
        self.df_app = {
            "main_kpis": main_kpis,
            "okr_value": df_okr_value,
            "frequency": df_frequency,
            "sdk_version": pd.DataFrame(df_sdk_by_version),
            "templates": df_templates,
        }

        return True

    def plot(self):
        """
        A method to plot KeyResults.

        This method utilizes the KeyResults class from the paths. key_results module
        to create and display a plot related to the key results. It assumes
        that KeyResults requires a reference to the instance of the class from which
        this method is called.

        Args:
        self: A reference to the current instance of the class.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the KeyResults class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the KeyResults class has access to all necessary data
          through the passed instance.
        """

        from paths.key_results import KeyResults

        KeyResults = KeyResults(self)
        KeyResults.plot()
