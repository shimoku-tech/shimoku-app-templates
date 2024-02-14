from utils.utils import (
    beautiful_header,
    beautiful_section,
    beautiful_email_subject,
    overview_section,
    results_section,
    generate_indicators_delivery_days,
)
import numpy as np

class Components:
    def plot_header(self, title: str) -> bool:
        """Header plot of the menu path

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.html(
            beautiful_header(title = title),
            order = self.order,
            rows_size = 1,
            cols_size = 12,
        )
        self.order += 1

        return True

    def plot_description_section(self, subject: str) -> bool:
        """Plot description section dedicate to Email subject

        Args:
            subject (str): Email subject of the model.

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.html(
            beautiful_email_subject(subject),
            order = self.order,
            cols_size = 12,
            rows_size = 1,
            padding = "0,3,0,3",
        )
        self.order += 1

        return True

    def plot_dates_secuence(self, delivery_days: str) -> bool:
        """Delivery days of each campaign model with indicators

        Args:
            delivery_days (str): Delivery days for each campaign model.

        Returns:
            bool: Execution status
        """
        data = generate_indicators_delivery_days(delivery_days.values[0])
        self.shimoku.plt.indicator(
            data = data,
            order = self.order,
            cols_size = 12,
            rows_size = 1,
        )
        self.order += len(data) + 1

        return True

    def plot_resumen(self, dataframe_name: str) -> bool:
        """Resume of the Email sent

        Args:
            dataframe_name (str): Dataframe with email sent information.

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.html(
            html = overview_section(self.df_app[dataframe_name]),
            order = self.order,
            cols_size = 5,
            rows_size = 3,
            padding = "0,1,0,1",
        )
        self.order += 1

        return True

    def plot_pie(self,
            title: str,
            dataframe_name: str,
            flag_size: bool = False,
            position: str = None
        ) -> bool:
        """Pie Chart to plot diferent email information from a dataframe.

        Args:
            title (str): Title pie charts
            dataframe_name (str): email information on a dataframe
            flag_size (bool, optional): flag to change between cols_size option. Defaults to False.
            position (str, optional): _description_. Defaults to None.

        Returns:
            bool: Execution status
        """
        cols_size = 4
        padding = "0,0,0,1" if position == "left" else "0,1,0,0"
        if flag_size:
            cols_size = 5
        self.shimoku.plt.pie(
            data = self.df_app[dataframe_name],
            order = self.order,
            title = title,
            cols_size = cols_size,
            rows_size = 3,
            padding = padding,
            names = 'name',
            values = 'percentage',
        )
        self.order += 1

        return True

    def plot_results(self, open: str, click: str, answer: str, rebound: str) -> bool:
        """Plot HTML structure with the Email results: opened, clicked, answered and rebounded

        Args:
            open (str): Dataframe name of opened data
            click (str): Dataframe name of clicked data
            answer (str): Dataframe name of answered data
            rebound (str): Dataframe name of rebounded data

        Returns:
            bool: Execution status
        """
        # Html
        self.shimoku.plt.html(
            html = results_section(
                self.df_app[open],
                self.df_app[click],
                self.df_app[answer],
                self.df_app[rebound],
            ),
            order = self.order,
            cols_size = 10,
            rows_size = 5,
            padding = "1,1,1,1",
        )
        self.order += 1

        return True

    def plot_table(self, df_name: str, table: str) -> bool:
        """Plot Table chart with the client information about open

        Args:
            df_name (str): Dataframe name of the client info by email opened/clicked
            table (str): Column name opened/clicked

        Returns:
            bool: Execution status
        """
        if self.df_app[df_name].shape[0]:
            self.shimoku.plt.table(
                data = self.df_app[df_name],
                order = self.order,
                cols_size = 10,
                rows_size = 4,
                page_size = 10,
                page_size_options = [10, 15, 20],
                initial_sort_column = f"Nº of {table}",
                categorical_columns = ["Contact Name", "Last Name", "Company"],
                sort_descending=True,
                label_columns = {
                    f"Nº of {table}": {
                        (3,  np.inf) : 'active'
                    }
                },
                columns_options = {
                    "Contact Name": {"width": 180},
                    "Last Name": {"width": 180},
                    "Company": {"width": 380},
                    f"Nº of {table}": {"width": 200},
                },
                padding = "0,1,0,1",
            )
            self.order += 1

        return True
