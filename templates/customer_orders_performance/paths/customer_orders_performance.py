from utils.utils import convert_dataframe_to_array, beautiful_header
from board import Board


class CustomerOrdersPerformance(Board):
    """
    This path is responsible for rendering the customer orders performance page.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the CustomerOrdersPerformance with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.df_app

        # Initialize order of plotting elements
        self.order = 0
        # Set the menu path for this page
        self.menu_path = "Customer Orders Performance"

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the customer orders performance page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_kpi_indicators()
        self.plot_customers_orders()
        self.plot_profit_margin()
        self.plot_top_customers_number_orders()
        self.plot_customers_number_orders()
        self.plot_customer_profitability()

    def plot_header(self) -> bool:
        """Header plot of the menu path

        Returns:
            bool: Execution status
        """
        title = "Customer Orders Performance"

        indicator = beautiful_header(title=title)
        self.shimoku.plt.html(
            indicator,
            order=self.order,
            rows_size=1,
            cols_size=12,
        )
        self.order += 1

        return True

    def plot_kpi_indicators(self) -> bool:
        """Indicatos plot of Main KPIs

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.indicator(
            data=convert_dataframe_to_array(self.df_app["main_kpis"]),
            order=self.order,
            rows_size=1,
            cols_size=12,
            value="value",
            header="title",
            footer="description",
            color="color",
            align="align",
        )
        self.order += len(self.df_app["main_kpis"]) + 1

        return True

    def plot_customers_orders(self) -> bool:
        """Line plot of customer and orders over each month

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.line(
            data=self.df_app["customers_orders"],
            order=self.order,
            title="Customers & Orders",
            rows_size=2,
            cols_size=6,
            x='Month',
            x_axis_name="Month",
            option_modifications={
                'toolbox': {'show': True}
            },
        )
        self.order += 1

        return True

    def plot_profit_margin(self) -> bool:
        """Line and Bar plot using profit margin compute from revenues and expenses over each month

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.line_and_bar_charts(
            data=self.df_app["profit_margin"],
            order=self.order,
            title="Profit margin",
            rows_size=2,
            cols_size=6,
            x='Month',
            x_axis_name='Month',
            bar_names=['Expenses', 'Revenues'],
            line_names=['Profit Margin'],
            line_axis_name='Profit Margin',
            line_suffix='%',
            bar_axis_name='€',
            bar_suffix='€'
        )
        self.order += 1

        return True

    def plot_top_customers_number_orders(self) -> bool:
        """Bar plot using Top customers by number of orders

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.bar(
            data=self.df_app["top_customers"],
            order=self.order,
            title="Top customers by number of orders",
            rows_size=2,
            cols_size=4,
            x="Customer",
            x_axis_name="Customers",
        )
        self.order += 1

        return True

    def plot_customers_number_orders(self) -> bool:
        """Doughnut plot using Customers by number of orders

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.doughnut(
            data=self.df_app["customers_by_orders"],
            order=self.order,
            title="Customers by number of orders",
            rows_size=2,
            cols_size=4,
            names="Orders",
            values="Customers",
        )
        self.order += 1

        return True

    def plot_customer_profitability(self) -> bool:
        """Stacked bar plot using Customer Profitability considering Top 5 customers by number of orders

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.stacked_bar(
            data=self.df_app["customer_profitability"],
            order=self.order,
            title="Customer Profitability",
            cols_size=4,
            rows_size=2,
            x="Month",
            x_axis_name="Month",
        )
        self.order += 1

        return True