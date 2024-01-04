from board import Board
import pandas as pd
from io import StringIO
from utils import beautiful_indicator


class Overview(Board):
    """
    This path is responsible for rendering the overview page.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the HiddenIndicatorsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.df_app

        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Overview"  # Set the menu path for this page

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the overview page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_revenue_by_product()
        self.plot_online_vs_in_store_revenues()
        self.plot_incremental_sales_by_origin_campaign()
        self.plot_cost_by_product()


    def plot_header(self):
        """
        Plots the header section.

        Returns:
            True if the operation is successful.
        """

        title = "Sales Product Performance Dashboard"

        indicator = beautiful_indicator(title=title)
        self.shimoku.plt.html(
            indicator,
            order=self.order,
            rows_size=1,
            cols_size=12
        )

        self.order += 1

        return True


    def plot_revenue_by_product(self):
        """
        Plots a doughnut for Revenue by Product KPI.

        Returns:
            True if the operation is successful.
        """

        df = self.df_app["main_kpis"]

        revenue_by_product = df[df["title"] == "Revenue by Product"]["value"]
        revenue_by_product = pd.read_json(StringIO(revenue_by_product.values[0]))

        products_name = df[df["title"] == "Product"]["value"]
        products_name = pd.read_json(StringIO(products_name.values[0]))
        products_name["product_name"] = products_name["product_name"].apply(
            lambda x: x.replace("_", " ")
        )

        data = [
            {"name": p_name.iloc[0], "value": revenue_product.iloc[0]}
            for (index1, p_name), (index2, revenue_product) in zip(
                products_name.iterrows(), revenue_by_product.iterrows()
            )
        ]

        self.shimoku.plt.doughnut(
            title="Revenue by Product",
            data=data,
            order=self.order,
            names="name",
            values="value",
            rows_size=2,
            cols_size=5,
        )

        self.order += 1

        return True

    def plot_online_vs_in_store_revenues(self):
        """
        Plots an area for Online vs In-Store Revenues KPI

        Returns:
            True if the operation is successful.
        """

        df = self.df_app["main_kpis"]

        online_revenues = df[df["title"] == "Online Revenues"]["value"]
        online_revenues = pd.read_json(StringIO(online_revenues.values[0]))

        in_store_revenues = df[df["title"] == "In Store Revenues"]["value"]
        in_store_revenues = pd.read_json(StringIO(in_store_revenues.values[0]))

        data = [
            {
                "date": online["sale_date"],
                "Online": online["revenue"],
                "In-Store": round(in_store["revenue"], 3),
            }
            for (index1, online), (index2, in_store) in zip(
                online_revenues.iterrows(), in_store_revenues.iterrows()
            )
        ]

        self.shimoku.plt.area(
            title="Online vs In-Store Revenues",
            data=data,
            order=self.order,
            x="date",
            x_axis_name="Months in 2023",
            rows_size=2,
            cols_size=7,
            option_modifications={"yAxis": {"axisLabel": {"formatter": "${value}"}}}
        )

        self.order += 1

        return True

    def plot_incremental_sales_by_origin_campaign(self):
        """
        Plots a horizontal bar for Incremental Sales by Origin Campaign KPI

        Returns:
            True if the operation is successful.
        """

        df = self.df_app["main_kpis"]

        sales_by_origin_campaign = df[
            df["title"] == "Incremental Sales by Origin Campaign"
        ]["value"]
        sales_by_origin_campaign = pd.read_json(
            StringIO(sales_by_origin_campaign.values[0])
        )

        data = [
            {
                "campaign": campaign["origin_campaign"],
                "Incremental Sale": campaign["revenue_k"],
            }
            for (index, campaign) in sales_by_origin_campaign.iterrows()
        ]

        self.shimoku.plt.horizontal_bar(
            title="Incremental Sales by Origin Campaign",
            data=data,
            order=self.order,
            x="campaign",
            rows_size=2,
            cols_size=5,
            option_modifications={"xAxis": {"axisLabel": {"formatter": "${value}K"}}}
        )

        self.order += 1

        return True

    def plot_cost_by_product(self):
        """
        Plots a stacked bar for Cost by Product KPI

        Returns:
            True if the operation is successful.
        """

        df = self.df_app["main_kpis"]

        cost_by_product = df[df["title"] == "Cost by Product"]["value"]
        cost_by_product = pd.read_json(StringIO(cost_by_product.values[0]))

        columns_name = cost_by_product.columns.tolist()[1:]
        new_names = {name: name.replace("_", " ") for name in columns_name}
        cost_by_product.rename(columns=new_names, inplace=True)

        self.shimoku.plt.stacked_bar(
            title="Cost by Product",
            data=cost_by_product,
            order=self.order,
            x="month",
            x_axis_name="Months in 2023",
            rows_size=2,
            cols_size=7,
            option_modifications={"yAxis": {"axisLabel": {"formatter": "{value}%"}}}
        )

        self.order += 1

        return True
