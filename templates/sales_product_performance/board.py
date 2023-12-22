from shimoku_api_python import Client
from utils import get_data
import pandas as pd


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

        file_names = ["data/sales_product_performance.csv"]
        self.board_name = "Sales Product Performance" # Name of the dashboard
        self.dfs = get_data(file_names)
        
        self.shimoku = shimoku  # Shimoku client instance
        self.shimoku.set_board(name=self.board_name)
        self.shimoku.boards.update_board(name=self.board_name)

    def transform(self):
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df = self.dfs["sales_product_performance"]

        revenue_by_product = df.groupby("product_name")["revenue"].sum().reset_index()

        online_revenues = df[df["sale_type"] == "Online"]
        online_revenues = online_revenues.groupby(online_revenues["sale_date"].dt.month)["revenue"].sum().reset_index()

        in_store_revenues = df[df["sale_type"] == "In-Store"]
        in_store_revenues = in_store_revenues.groupby(in_store_revenues["sale_date"].dt.month)["revenue"].sum().reset_index()

        sales_by_origin_campaign = df.groupby("origin_campaign")["revenue"].sum().reset_index()

        # Agrupar por mes, año y producto, sumando los valores de 'cost'
        df['month'] = df['sale_date'].dt.month
        cost_by_product = df.groupby(['month', 'product_name'])['cost'].sum().reset_index()
        cost_by_product = cost_by_product.pivot_table(index=['month'], columns='product_name', values='cost', aggfunc='sum').reset_index()


        main_kpis = [
            {
                "title": "Revenue by Product",
                "description": "Revenue value by product",
                "value": revenue_by_product[["revenue"]].to_json(),
                "color": "success",
                "align": "center",
            },
            {
                "title": "Product",
                "description": "Products for sale",
                "value": revenue_by_product[["product_name"]].to_json(),
                "color": "success",
                "align": "center",
            },
            {
                "title": "Online Revenues",
                "description": "Online revenues by month in 2023",
                "value": online_revenues.to_json(),
                "color": "success",
                "align": "center",
            },
            {
                "title": "In Store Revenues",
                "description": "In store revenues by month in 2023",
                "value": in_store_revenues.to_json(),
                "color": "success",
                "align": "center",
            },
            {
                "title": "Incremental Sales by Origin Campaign",
                "description": "Revenues according to the origin of the marketing campaign",
                "value": sales_by_origin_campaign.to_json(),
                "color": "success",
                "align": "center",
            },
            {
                "title": "Cost by Product",
                "description": "Cost weight of each product",
                "value": cost_by_product.to_json(),
                "color": "success",
                "align": "center",
            }
        ]

        self.df_app = {"main_kpis": pd.DataFrame(main_kpis)}

        return True

    def plot(self):
        """
        A method to plot user overview.

        This method utilizes the UserOverview class from the paths.user_overview
        module to create and display a plot related to the user. It assumes that
        UserOverview requires a reference to the instance of the class from which
        this method is called.

        Args:
        self: A reference to the current instance of the class.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the UserOverview class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the UserOverview class has access to all necessary data
          through the passed instance.
        """

        from paths.overview import Overview

        overview_path = Overview(self)
        overview_path.plot()