import os
import shimoku_api_python as Shimoku

from utils.utils import DFs
from utils.components.header import create_title_name_head
from utils.utils import format_number
from utils.transform import (
    count_column_values,
    count_column_values_with_filter,
    df_to_indicator_product_data,
)


class PredictionsPage:
    def __init__(self, shimoku: Shimoku.Client, board: dict):
        """
        Initialize an instance of the 'YourClassName' class.

        Args:
            shimoku (Shimoku.Client): An instance of the Shimoku Client.
            board (dict): A dictionary representing the Shimoku board.

        This constructor initializes the instance with a Shimoku client, board
        information, an order value, and a menu path derived from the file name.
        It also loads and transforms data using 'load_tranform_data' method and
        sets the menu path for Shimoku.
        """
        self.shimoku = shimoku
        self.board = board
        self.order = 0

        # Derive a menu path from the file name.
        self.menu_path = (
            os.path.basename(__file__).replace(".py", "").capitalize()
        )

        # Load and transform data using the 'load_tranform_data' method.
        self.dataframe = self.load_transform_data()

        # Set the menu path for Shimoku.
        self.shimoku.set_menu_path(self.menu_path)

    def load_transform_data(self):
        """
        Load and transform data using an instance of the 'DFs' class.

        Returns:
            pandas.DataFrame: The transformed data in the form of a DataFrame.
        """
        # Create an instance of the 'DFs' class.
        df = DFs()

        # Retrieve the DataFrame 'x' from the 'DFs' instance.
        x = df.df

        return x

    def plot_indicator_list(self, hidden_path=False):
        """
        Plot a list of HIGH indicators for the Shimoku board.

        Args:
            hidden_path (bool, optional): Flag indicating if hidden path is enabled.
                                         Defaults to False.

        Returns:
            bool: True if the indicators are successfully plotted, False otherwise.
        """
        # Define common settings for indicators.
        common_indicator_settings = {
            "align": "left",
            "variant": "topColor",
        }

        if hidden_path:
            # Save the current order to restore it later.
            temp_order = self.order
            self.order = 1

        for prod_cat in self.product_count_dict.keys():
            # Add a title for the product category.
            self.shimoku.plt.html(
                html=self.shimoku.html_components.create_h1_title(
                    title="",
                    subtitle=f"{prod_cat}",
                ),
                order=self.order,
            )

            self.order += 1

            # Plot up to 4 products within the product category.
            for product in self.product_count_dict[prod_cat][:4]:
                _product = {**product, **common_indicator_settings}
                self.shimoku.plt.indicator(
                    data=_product,
                    order=self.order,
                    cols_size=3,
                )
                # Remove the plotted product from the dictionary.
                del self.product_count_dict[prod_cat][
                    self.product_count_dict[prod_cat].index(product)
                ]

                self.order += 1

        if hidden_path:
            # Restore the original order if hidden path is enabled.
            self.order = temp_order

        return True

    def headings(self):
        """
        Create and display headings for the Predictions page.

        Returns:
            bool: True if the headings are successfully displayed, False otherwise.
        """
        # Create and display the main title and subtitle.
        self.shimoku.plt.html(
            html=create_title_name_head(
                title="Predictions",
                subtitle="Product Recommender",
            ),
            order=self.order,
        )

        self.order += 1

        return True

    def indicators(self):
        """
        Create and display indicators section for the Predictions page.

        Returns:
            bool: True if the indicators are successfully displayed, False otherwise.
        """
        # Common settings for indicators
        common_indicator_settings = {
            "align": "center",
            "variant": "topColor",
        }

        # Increment order
        self.order += 1

        # Display general indicators section title
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Total opportunities",
                subtitle="",
            ),
            order=self.order,
        )
        self.order += 1

        # Define description prefix
        desc_prefix = "Oportunidades"

        # Display indicators for HIGH, MEDIUM, and LOW probabilities
        self.order += self.shimoku.plt.indicator(
            data=[
                {
                    "title": "HIGH",
                    "value": format_number(
                        self.lead_scoring_agg["Lead Scoring"]["High"]
                    ),
                    "color": "success",
                    "description": f"{desc_prefix} con una probabilidad de éxito mayor del 75%",
                    **common_indicator_settings,
                },
                {
                    "title": "MEDIUM",
                    "value": format_number(
                        self.lead_scoring_agg["Lead Scoring"]["Medium"]
                    ),
                    "color": "warning",
                    "description": f"{desc_prefix} con una probabilidad de éxito de entre el 50% y el 75%",
                    **common_indicator_settings,
                },
                {
                    "title": "LOW",
                    "value": format_number(
                        self.lead_scoring_agg["Lead Scoring"]["Low"]
                    ),
                    "color": "error",
                    "description": f"{desc_prefix} con una probabilidad de éxito menor del 50%",
                    **common_indicator_settings,
                },
            ],
            order=self.order,
        )

        # Display product opportunities section title
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Product opportunities",
                subtitle="Basado en Lead Scoring High",
            ),
            order=self.order,
        )
        self.order += 1

        # Display indicators per product category
        self.plot_indicator_list()

        # Plot hidden indicators page
        self.hidden_indicators_page()

        return True

    def table_simple(self):
        """
        Create and display a simple table for the Product Recommender on the Predictions page.

        Returns:
            bool: True if the table is successfully displayed, False otherwise.
        """
        # Define the order of the columns in the table
        df_premodel_cols = [
            "Lead ID",
            "Lead Scoring",
            "Probability",
            "Drivers",
            "Barriers",
            "Product",
        ]

        # Filter and sort the dataframe for High and Medium Lead Scoring
        df_table = self.dataframe[
            (self.dataframe["Lead Scoring"] == "High")
            | (self.dataframe["Lead Scoring"] == "Medium")
        ].sort_values("Probability", ascending=False)

        # Replace NaN values of factors with the empty string
        df_table["Drivers"] = df_table["Drivers"].fillna("")
        df_table["Barriers"] = df_table["Barriers"].fillna("")

        # Round Probability values to one decimal place
        # Consider doing this later on the CSV file via Jupyter Lab if it takes too long
        df_table["Probability"] = df_table["Probability"].round(decimals=1)

        # Common settings for the columns of the table
        common_col_options = {}

        # Sort the data by Probability in descending order
        data = df_table.sort_values("Probability", ascending=False)

        impact_factors_col_width = 450

        # Set the menu path for Shimoku
        self.shimoku.set_menu_path(self.menu_path)

        # Plot the table
        self.shimoku.plt.table(
            order=self.order,
            data=data,
            page_size_options=[10, 20],
            rows_size=4,
            categorical_columns=[
                "Lead Scoring",
                "Empresa",
            ],
            label_columns={
                ("Probability (%)", "outlined"): {
                    (0, 50): "error",
                    (50, 75): "warning",
                    (75, 100): "success",
                },
                ("Lead Scoring", "filled"): {
                    "Low": "error",
                    "Medium": "warning",
                    "High": "success",
                },
                # Uncomment these lines if needed
                # ("Drivers", "filled"): "main",
                # ("Barriers", "filled"): "caution",
            },
            columns_options={
                "Product": {
                    "width": 300,
                },
                "Probability (%)": {
                    "width": 150,
                },
                "Lead Scoring": {
                    "width": 100,
                },
                "Drivers": {
                    "width": impact_factors_col_width,
                },
                "Barriers": {
                    "width": impact_factors_col_width,
                },
                "Etapa Vida": {
                    "width": 230,
                },
            },
        )

        self.order += 1

        return True

    def hidden_indicators_page(self):
        """
        Create a detailed page of all product indicators falling into the 'Other products' category.

        This method sets up a page to display indicators for products categorized as 'Other products'
        with Lead Scoring HIGH. It includes a title, subtitle, and the indicators themselves.

        Returns:
            None
        """
        order = 0
        menu_path = "Hidden indicators"

        # Set the menu path for Shimoku to 'Hidden indicators'
        self.shimoku.set_menu_path(name=menu_path)

        # Display the title and subtitle for the page
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Otros productos",
                subtitle="Indicadores Lead Scoring HIGH, de 'otros productos'",
            ),
            order=order,
        )

        order += 1

        # Plot the indicators for the 'Other products' category
        self.plot_indicator_list(hidden_path=True)

        # Hide the menu path for 'Hidden indicators'
        self.shimoku.menu_paths.update_menu_path(
            name=menu_path,
            hide_path=True,
        )

        # Pop out of the current menu path
        self.shimoku.pop_out_of_menu_path()

    def compute(self):
        """
        Perform data computations and transformations for generating predictions page.

        This method calculates various data statistics and performs transformations
        to prepare data for displaying on the predictions page.

        Returns:
            None
        """
        # Transformation

        # Count occurrences of Lead Scoring values in the dataframe.

        self.lead_scoring_agg = count_column_values(
            df=self.dataframe, column="Lead Scoring"
        )

        # Count occurrences of Product when Lead Scoring is "High."
        self.high_product_count = count_column_values_with_filter(
            df=self.dataframe,
            column="Product",
            filter_column="Lead Scoring",
            filter_value="High",
        )

        # Convert high_product_count DataFrame to a dictionary.
        high_product_count_dict = df_to_indicator_product_data(
            df=self.high_product_count,
            column_name="Product",
        )

        # Order the dictionary by value and create two lists.
        sorted_data = dict(
            sorted(
                high_product_count_dict["Productos"].items(),
                key=lambda x: x[1]["value"],
                reverse=True,
            )
        )

        other_values = list(sorted_data.values())[3:]
        other_values_sum = sum([x["value"] for x in other_values])
        highest_values = list(sorted_data.values())[:3]

        total_value = sum(
            item["value"] for item in highest_values + other_values
        )

        # Calculate and format percentage values for the items.
        for item in highest_values + other_values:
            percentage = (item["value"] / total_value) * 100
            item["value"] = f'{item["value"]} ({percentage:.1f}%)'

        # Calculate and format the percentage of other_values_sum.
        percentage = (other_values_sum / total_value) * 100
        other_values_sum = f"{other_values_sum} ({percentage:.1f}%)"

        # Create a dictionary for product counts, including "Otros productos."
        self.product_count_dict = (
            highest_values
            + [
                {
                    "title": "Otros productos",
                    "value": other_values_sum,
                    "color": "success",
                    "targetPath": f'{self.board["id"]}/hidden-indicators',
                }
            ]
            + other_values
        )

        # Organize the product count data into a dictionary.
        self.product_count_dict = {"Productos": self.product_count_dict}

        # Plotting

        # Generate headings for the predictions page.
        self.headings()

        # Create indicators for the predictions page.
        self.indicators()

        # Generate a simple table for the predictions page.
        self.table_simple()
