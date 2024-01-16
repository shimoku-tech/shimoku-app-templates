from utils.utils import convert_dataframe_to_array, beautiful_header, categories
from board import Board


class CohortAnalysis(Board):
    """
    This path is responsible for rendering the cohort analysis page.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the HiddenIndicatorsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.df_app

        # Initialize order of plotting elements
        self.order = 0
        # Set the menu path for this page
        self.menu_path = "Cohort Analysis"

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the cohort analysis page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_kpi_indicators()
        self.set_tabs()
        self.plot_all()
        self.plot_gender()
        self.plot_age()
        self.plot_acquisition_source()

    def plot_header(self):
        """Header plot of the menu path

        Returns:
            bool: Execution status
        """
        title = "Mobile App - Cohort Analysis"

        self.shimoku.plt.html(
            beautiful_header(title=title),
            order = self.order,
            rows_size = 1,
            cols_size = 12,
        )
        self.order += 1

        return True

    def plot_kpi_indicators(self) -> bool:
        """Indicatos plot of Main KPIs

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.indicator(
            data = convert_dataframe_to_array(self.df_app["main_kpis"]),
            order = self.order,
            rows_size = 1,
            cols_size = 12,
            value = "value",
            header = "title",
            footer = "description",
            color = "color",
            align = "align",
        )
        self.order += len(self.df_app["main_kpis"]) + 1

        return True

    def set_tabs(self):
        self.shimoku.plt.set_tabs_index(("Charts", "All"),
            order=self.order,
            just_labels=True, cols_size = 22,
            rows_size = 10,
            padding='0,1,0,1',
        )
        self.shimoku.plt.change_current_tab("Gender")
        self.shimoku.plt.change_current_tab("Age")
        self.shimoku.plt.change_current_tab("Acquisition Source")
        self.order += 1

        return True

    def plot_all(self) -> bool:
        self.shimoku.plt.change_current_tab("All")

        # Lie chart
        self.shimoku.plt.line(
            data = self.df_app["all_line_chart"],
            order = self.order,
            cols_size = 10,
            rows_size = 3,
            x = "week",
            x_axis_name="Weeks",
        )
        self.order += 1

        # Table Chart
        self.shimoku.plt.table(
            data=self.df_app["all_table_chart"],
            order=self.order,
            cols_size = 10,
            rows_size = 4,
            title="Cohort Analysis",
            initial_sort_column="Week (Date)",
            sort_descending=False,
            columns_options={
                "Week (Date)": {"width": 110},
                "Users": {"width": 80},
            },
        )
        self.order += 1

        return True

    def plot_gender(self) -> bool:
        self.shimoku.plt.change_current_tab("Gender")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=4, rows_size=3)

        # pie chart
        self.shimoku.plt.pie(
            data = self.df_app["gender_pie_chart"],
            order = self.order,
            cols_size = 24,
            rows_size = 21,
            names = "name",
            values = "value",
            padding="2,2,2,2",
        )
        self.order += 1

        # Html
        self.shimoku.plt.html(
            order = self.order,
            cols_size = 24,
            rows_size = 10,
            padding="0,2,1,2",
            html = categories(self.df_app["gender_pie_chart"].sort_values(
                by=["value"],
                ascending=False,
            ))
        )
        self.order += 1

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # Lie chart
        self.shimoku.plt.line(
            data = self.df_app["gender_line_chart"],
            order = self.order,
            cols_size = 6,
            rows_size = 3,
            x = "week",
        )
        self.order += 1

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=12, rows_size=5)

        # Table Tabs
        for gender in self.df_app["gender_pie_chart"].name.unique():
            self.shimoku.plt.set_tabs_index(
                ("Gender Tabs", gender),
                order=self.order,
                just_labels=True,
                cols_size = 24,
                rows_size = 6,
                padding='0,0,0,0',
                parent_tabs_index=("Charts", "Gender"),
            )
            self.order += 1

            # Table Chart

            self.shimoku.plt.table(
                data=self.df_app[f"gender_table_chart_{gender}"],
                order=self.order,
                cols_size = 24,
                rows_size = 4,
                title="Cohort Analysis",
                initial_sort_column="Week (Date)",
                sort_descending=False,
            )
            self.order += 1

        self.shimoku.plt.set_tabs_index(tabs_index=("Charts", "Gender"))

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        return True

    def plot_age(self) -> bool:
        self.shimoku.plt.change_current_tab("Age")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=4, rows_size=3)

        # pie chart
        self.shimoku.plt.pie(
            data = self.df_app["age_pie_chart"],
            order = self.order,
            cols_size = 24,
            rows_size = 18,
            names = "name",
            values = "value",
            padding="2,2,2,2",
        )
        self.order += 1

        # Html
        self.shimoku.plt.html(
            order = self.order,
            cols_size = 24,
            rows_size = 10,
            padding="0,2,1,2",
            html = categories(self.df_app["age_pie_chart"].sort_values(
                by=["value"],
                ascending=False,
            ))
        )
        self.order += 1

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # Lie chart
        self.shimoku.plt.line(
            data = self.df_app["age_line_chart"],
            order = self.order,
            cols_size = 6,
            rows_size = 3,
            x = "week",
        )
        self.order += 1

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=12, rows_size=5)

        # Table Tabs
        for age_range in self.df_app["age_pie_chart"].name.unique():
            self.shimoku.plt.set_tabs_index(
                ("Age Tabs", age_range),
                order=self.order,
                just_labels=True,
                parent_tabs_index=("Charts", "Age"),
            )
            self.order += 1

            self.shimoku.plt.table(
                data=self.df_app[f"age_table_chart_{age_range}"],
                order=self.order,
                cols_size = 24,
                rows_size = 4,
                title="Cohort Analysis",
                initial_sort_column="Week (Date)",
                sort_descending=False,
            )
            self.order += 1
            self.order += 1

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()
        self.shimoku.plt.set_tabs_index(tabs_index=("Charts", "Age"))

        return True

    def plot_acquisition_source(self) -> bool:
        self.shimoku.plt.change_current_tab("Acquisition Source")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=4, rows_size=3)

        # Pie chart
        self.shimoku.plt.pie(
            data = self.df_app["source_pie_chart"],
            order = self.order,
            cols_size = 24,
            rows_size = 21,
            names = "name",
            values = "value",
            padding="2,2,2,2",
        )
        self.order += 1

        # Html
        self.shimoku.plt.html(
            order = self.order,
            cols_size = 24,
            rows_size = 10,
            padding="0,2,1,2",
            html = categories(self.df_app["source_pie_chart"].sort_values(
                by=["value"],
                ascending=False,
            ))
        )
        self.order += 1

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # Line chart
        self.shimoku.plt.line(
            data = self.df_app["source_line_chart"],
            order = self.order,
            cols_size = 6,
            rows_size = 3,
            x = "week",
        )
        self.order += 1


        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=12, rows_size=6)

        # Table Tabs
        for source in self.df_app["source_pie_chart"].name.unique():
            self.shimoku.plt.set_tabs_index(
                ("Acquisition Source Tabs", source),
                order=self.order,
                just_labels=True,
                cols_size = 24,
                rows_size = 5,
                parent_tabs_index=("Charts", "Acquisition Source"),
            )
            self.order += 1

            # Table Chart
            self.shimoku.plt.table(
                data=self.df_app[f"source_table_chart_{source}"],
                order=self.order,
                cols_size = 24,
                rows_size = 4,
                title="Cohort Analysis",
                initial_sort_column="Week (Date)",
                sort_descending=False,
            )
            self.order += 1

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        self.shimoku.plt.set_tabs_index(tabs_index=("Charts", "Acquisition Source"))
        self.shimoku.plt.pop_out_of_tabs_group()
        return True
