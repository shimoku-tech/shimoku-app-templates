from utils.utils import convert_dataframe_to_array, beautiful_header, categories, cohort_colors
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
        self.plot_tabs()
        self.plot_all()
        self.plot_gender()
        self.plot_age()
        self.plot_acquisition_source()

    def plot_header(self) -> bool:
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

    def plot_tabs(self) -> bool:
        """plot the principal tabs on the dashboard

        Returns:
            bool: Execution status
        """
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
        """Plot the principal tab called 'All'. It plots two sections: Users Life Time and Cohort Analysis.

        Returns:
            bool: Execution status
        """
        # Change current tab
        self.shimoku.plt.change_current_tab("All")

        # User life time - line chart
        self.plot_users_life_time("all_life_time", 10)

        # Cohort analysis by gender - table chart
        self.plot_cohort_analysis(f"all_cohort")

        return True

    def plot_gender(self) -> bool:
        """Plot the principal tab called "Gender". It plots three sections: Category,
        Users Life Time and Cohort Analysis.

        Returns:
            bool: Execution status
        """
        # Change current tab
        self.shimoku.plt.change_current_tab("Gender")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=4, rows_size=3)
        # Gender category - pie chart
        self.plot_category("gender_category")
        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # User life time - line chart
        self.plot_users_life_time("gender_life_time")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=12, rows_size=5)
        # Plot cohort analysis table in a diferent tab
        for gender in self.df_app["gender_category"].name.unique():
            self.shimoku.plt.set_tabs_index(
                ("Gender Tabs", gender),
                order=self.order,
                just_labels=True,
                cols_size = 24,
                rows_size = 6,
                parent_tabs_index=("Charts", "Gender"),
            )
            self.order += 1

            # Cohort analysis by gender - table chart
            self.plot_cohort_analysis(f"gender_cohort_{gender}")

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # Go back to principal tabs
        self.shimoku.plt.set_tabs_index(tabs_index=("Charts", "Gender"))

        return True

    def plot_age(self) -> bool:
        """Plot the principal tab called "Age". It plots three sections: Category,
        Users Life Time and Cohort Analysis.

        Returns:
            bool: Execution status
        """
        # Change current tab
        self.shimoku.plt.change_current_tab("Age")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=4, rows_size=3)
        # Age category - Pie Chart
        self.plot_category("age_category")
        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # User life time - line chart
        self.plot_users_life_time("age_life_time")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=12, rows_size=5)
        # Plot cohort analysis table in a diferent tab
        for age_range in self.df_app["age_category"].name.unique():
            self.shimoku.plt.set_tabs_index(
                ("Age Tabs", age_range),
                order=self.order,
                just_labels=True,
                parent_tabs_index=("Charts", "Age"),
            )
            self.order += 1

            # Cohort analysis by age range - table chart
            self.plot_cohort_analysis(f"age_cohort_{age_range}")

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # Go back to principal tabs
        self.shimoku.plt.set_tabs_index(tabs_index=("Charts", "Age"))

        return True

    def plot_acquisition_source(self) -> bool:
        """Plot the principal tab called "Acquisition Source". It plots three sections: Category,
        Users Life Time and Cohort Analysis.

        Returns:
            bool: Execution status
        """
        # Change Current Tab
        self.shimoku.plt.change_current_tab("Acquisition Source")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=4, rows_size=3)
        # Gender category - pie chart
        self.plot_category("source_category")
        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # User life time - line chart
        self.plot_users_life_time("source_life_time")

        # Set bentobox size
        self.shimoku.plt.set_bentobox(cols_size=12, rows_size=6)
        # Plot cohort analysis table in a diferent tab
        for source in self.df_app["source_category"].name.unique():
            self.shimoku.plt.set_tabs_index(
                ("Acquisition Source Tabs", source),
                order=self.order,
                just_labels=True,
                cols_size = 24,
                rows_size = 5,
                parent_tabs_index=("Charts", "Acquisition Source"),
            )
            self.order += 1

            # Cohort analysis by adquisition source - table chart
            self.plot_cohort_analysis(f"source_cohort_{source}")

        # Pop out of bentobox
        self.shimoku.plt.pop_out_of_bentobox()

        # Go back to principal tabs
        self.shimoku.plt.set_tabs_index(tabs_index=("Charts", "Acquisition Source"))

        # Pop out of tabs group
        self.shimoku.plt.pop_out_of_tabs_group()

        return True

    def plot_category(self, dataframe_name: str, ):
        """Function basic to plot the category section for each tab

        Args:
            dataframe_name (str): Dataframe name used  in the dictionary of dataframes.

        Returns:
            bool: Execution status
        """
        # Pie chart
        self.shimoku.plt.pie(
            data = self.df_app[dataframe_name],
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
            html = categories(self.df_app[dataframe_name].sort_values(
                by=["value"],
                ascending=False,
            ))
        )
        self.order += 1

        return True

    def plot_users_life_time(self, dataframe_name: str, cols_size: int = 6):
        """Function basic to plot the User Life Time section for each tab

        Args:
            dataframe_name (str): Dataframe name used  in the dictionary of dataframes.
            cols_size (int, optional): Columns size to plot the chart. Defaults to 6.

        Returns:
            bool: Execution status
        """
        # Line chart
        self.shimoku.plt.line(
            data = self.df_app[dataframe_name],
            order = self.order,
            cols_size = cols_size,
            rows_size = 3,
            title = "Users Life Time",
            x = "week",
            x_axis_name="Weeks",
        )
        self.order += 1

        return True

    def plot_cohort_analysis(self, dataframe_name: str):
        """Function basic to plot the Cohort Analysis section for each tab

        Args:
            dataframe_name (str): Dataframe name used  in the dictionary of dataframes.

        Returns:
            bool: Execution status
        """
        # Table Chart
        self.shimoku.plt.table(
            data=self.df_app[dataframe_name],
            order=self.order,
            cols_size = 24,
            rows_size = 4,
            title="Cohort Analysis",
            initial_sort_column="Week (Date)",
            sort_descending=False,
            label_columns={
                f"W{index}": cohort_colors()
            for index in range(self.df_app[dataframe_name].columns.shape[0] - 2)},
            columns_options={
                "Week (Date)": {"width": 110},
                "Users": {"width": 80},
            },
        )
        self.order += 1

        return True