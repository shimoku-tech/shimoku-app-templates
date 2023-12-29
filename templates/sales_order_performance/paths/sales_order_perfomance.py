from board import Board


class SalesOrderPerformance(Board):
    """
    This class represents a Sales Order Performance dashboard.
    It inherits from the Board class.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the SalesOrderPerformance instance.

        Parameters:
            self_board (Board): An instance of the Board class.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.results
        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Overview"  # Set the menu path for this page
        self.shimoku.set_menu_path(name=self.menu_path)  # Set the menu path in Shimoku

    def plot(self):
        """
        Plots the Sales Order Performance dashboard.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_kpi_indicators()
        self.plot_charts()

    def plot_header(self):
        """
        Plot the header section of the dashboard.
        """
        # Create Sales Orders Performance title
        self.shimoku.plt.html(
            order=self.order,
            html=self.shimoku.html_components.create_h1_title(
                title="Sales Orders Performance", subtitle=""
            ),
        )
        self.order += 1

    def plot_kpi_indicators(self):
        """
        Plot the Key Performance Indicators (KPI) section of the dashboard.
        """
        income_total = self.df_app["income_total"]
        spend_total = self.df_app["spend_total"]
        net_profit = self.df_app["net_profit"]
        average_profit_per_order = self.df_app["average_profit_per_order"]

        # Display indicators
        indicator_data = [
            {
                "title": "Income",
                "align": "center",
                "value": f"${round(income_total, 0)}",
            },
            {
                "title": "Expenses",
                "align": "center",
                "value": f"${round(spend_total, 0)}",
            },
            {
                "title": "Net Profit",
                "align": "center",
                "value": f"${round(net_profit, 0)}",
            },
            {
                "title": "Average Profit per order",
                "align": "center",
                "value": f"${round(average_profit_per_order, 0)}",
            },
        ]

        self.shimoku.plt.indicator(data=indicator_data, order=self.order)
        self.order += len(indicator_data)

    def plot_charts(self):
        """
        Plot the charts section of the dashboard.
        """
        net_profit_by_month = self.df_app["net_profit_by_month"]

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=24, rows_size=3)

        # Display bar chart
        self.shimoku.plt.bar(
            data=net_profit_by_month[["Income", "Expenses", "Month"]],
            order=self.order,
            x="Month",
            rows_size=30,
        )
        self.order += 1

        # Display line chart
        self.shimoku.plt.line(
            data=net_profit_by_month[["Net Profit", "Month"]],
            order=self.order,
            x="Month",
            rows_size=30,
        )

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()
