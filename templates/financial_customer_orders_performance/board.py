from shimoku_api_python import Client
from utils.utils import get_data
import pandas as pd
from datetime import datetime, timedelta


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

        file_names = ["data/customer_orders_performance.csv"]
        self.board_name = "Financial"  # Name of the dashboard
        self.dfs = get_data(file_names)
        self.shimoku = shimoku  # Shimoku client instance
        self.shimoku.set_board(name=self.board_name)  # Setting up the board in Shimoku

    def transform(self) -> bool:
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df_customer_orders = self.dfs["customer_orders_performance"]

        # Main KPIs
        main_kpis = [
            # Total Customers
            {
                "title": "Customers",
                "value": len(df_customer_orders["customer_id"].unique()),
                "color": "default",
                "align": "center",
            },
            # Total orders
            {
                "title": "Orders",
                "value": len(df_customer_orders["order_id"].unique()),
                "color": "default",
                "align": "center",
            },
            # Total order revenue
            {
                "title": "Revenue",
                "value": f'{sum(df_customer_orders["order_spend"]):,.0f}€',
                "color": "default",
                "align": "center",
            },
            # Total order expenses
            {
                "title": "Expenses",
                "value": f'{sum(df_customer_orders["order_cost"]):,.0f}€',
                "color": "default",
                "align": "center",
            },
            # Net profit from the order
            {
                "title": "Net Profit",
                "value": f'{sum(df_customer_orders["order_spend"] - df_customer_orders["order_cost"]):,.0f}€',
                "color": "default",
                "align": "center",
            },
            # The percentage of net profit in relation to revenue
            {
                "title": "Profit Margin",
                "value": f'{sum(df_customer_orders["order_spend"] - df_customer_orders["order_cost"]) * 100 / sum(df_customer_orders["order_spend"]):.1f}%',
                "color": "default",
                "align": "center",
            },
        ]

        # Customers and orders
        import calendar
        customers_orders = [
            {
                "Month": calendar.month_name[month][:3],
                "Customer": len(
                    df_customer_orders["customer_id"][df_customer_orders["order_date"].dt.month == month].unique()
                ),
                "Orders": len(
                    df_customer_orders["order_id"][df_customer_orders["order_date"].dt.month == month].unique()
                ),
            }
        for month in range(1,13)]

        # Profit Margin
        profit_margin = [
            {
                "Month": calendar.month_name[month][:3],
                "Expenses": sum(df_customer_orders["order_cost"][df_customer_orders["order_date"].dt.month == month]),
                "Revenues": sum(df_customer_orders["order_spend"][df_customer_orders["order_date"].dt.month == month]),
                "Profit Margin": sum(
                        df_customer_orders["order_spend"][df_customer_orders["order_date"].dt.month == month] -
                        df_customer_orders["order_cost"][df_customer_orders["order_date"].dt.month == month]
                    )
                    * 100 / sum(df_customer_orders["order_spend"][df_customer_orders["order_date"].dt.month == month]
                ),
            }
        for month in range(1,13)]

        self.df_app = {
            "main_kpis": pd.DataFrame(main_kpis),
            "customers_orders": pd.DataFrame(customers_orders),
            "profit_margin": pd.DataFrame(profit_margin),
        }

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

        from paths.customer_orders_performance import customer_orders_performance

        UO = customer_orders_performance(self)
        UO.plot()
