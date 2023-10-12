import os
import shimoku_api_python as Shimoku
import pandas as pd

from tqdm import tqdm
from collections import Counter
from utils.settings import nominal
from utils.settings import numerical
from utils.utils import DFs
from utils.components.header import create_title_name_head
from utils.utils import format_number
from utils.transform import (
    count_column_values,
    count_column_values_with_filter,
    df_to_indicator_product_data,
)


class InsightsPageFiltersA:
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
            os.path.basename(__file__).replace(".py", "").replace("_", " ").title()
        )

        # Load and transform data using the 'load_tranform_data' method.
        self.dataframe = self.load_transform_data()

        # Set the menu path for Shimoku.
        self.shimoku.set_menu_path(self.menu_path)
        self.shimoku.reuse_data_sets()

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

    @staticmethod
    def extract_features_from_dict(dictionary):
        data_list = []
        for feature, attributes in dictionary.items():
            x = attributes["prob"].strip("%")
            importance = abs(
                int(x)
            )  # Extract and convert the 'prob' to absolute integer
            data_list.append({"feature": feature, "importance": importance})
        return data_list

    @staticmethod
    def extract_number(s):
        """Extrae todos los números de una cadena y los une."""
        return int("".join([char for char in s if char.isdigit()]))

    @staticmethod
    def string_to_dict(s):
        elements = s.split(" - ")
        result = {}
        for element in elements:
            parts = element.split(" % ")
            name = parts[0].split(" ")[0].strip()

            if len(parts) == 1:  # Solo hay un elemento (como 'Edad 30% 50')
                prob_parts = parts[0].split(" ")
                prob = prob_parts[1] if len(prob_parts) > 1 else ""
                val = " ".join(prob_parts[2:]) if len(prob_parts) > 2 else None
            else:
                prob_parts = parts[1].split(" ")
                prob = prob_parts[0] + "%" if len(prob_parts) > 0 else ""
                val = " ".join(prob_parts[1:]) if len(prob_parts) > 1 else None

            result[name] = {"prob": prob, "val": val}
        return result

    def headings(self, title, subtitle):
        """
        Create and display headings for the Predictions page.

        Returns:
            bool: True if the headings are successfully displayed, False otherwise.
        """
        # Create and display the main title and subtitle.
        self.shimoku.plt.html(
            html=create_title_name_head(
                title=title,
                subtitle=subtitle,
            ),
            order=self.order,
        )

        self.order += 1

        return True

    def compute(self):
        list_of_products = self.dataframe["Product"].unique()

        self.dataframe["Drivers"] = self.dataframe["Drivers"].apply(self.string_to_dict)
        self.dataframe["Barriers"] = self.dataframe["Barriers"].apply(
            self.string_to_dict
        )

        self.headings(title="AI Insights", subtitle="Exaplainbility per product")

        for product in list_of_products[:2]:
            # Init for every iteration
            all_variables = []

            # Filter by product
            df_product_filtered = self.dataframe[self.dataframe["Product"] == product]

            # Create a tab per product
            self.shimoku.plt.set_tabs_index(
                tabs_index=("product_tab", product),
                sticky=False,
                just_labels=True,
                order=self.order,
            )
            self.order += 1

            # Feature importance section

            self.shimoku.plt.html(
                html=self.shimoku.html_components.create_h1_title(
                    title=f"Feature Importance",
                    subtitle="Weight of each feature in the probability for cross selling",
                ),
                order=self.order,
            )
            self.order += 1

            for _, row in df_product_filtered.iterrows():
                x1 = self.extract_features_from_dict(row["Drivers"])
                x2 = self.extract_features_from_dict(row["Barriers"])
                all_variables.extend(x1)
                all_variables.extend(x2)

            # Initialize dictionaries for sum and count of each feature's importance
            sum_importances = {}
            count_features = {}

            # Iterate over the dictionaries in all_variables
            for item in all_variables:
                feature = item["feature"]
                importance = item["importance"]

                # Accumulate importance and count for each feature
                sum_importances[feature] = sum_importances.get(feature, 0) + importance
                count_features[feature] = count_features.get(feature, 0) + 1

            # Calculate the average importance for each feature
            average_importances = {
                feature: sum_importances[feature] / count_features[feature]
                for feature in sum_importances
            }

            # Convert to the desired format round to 1 decimal average_importances[feature]
            result = [
                {
                    "feature": feature,
                    "importance": round(average_importances[feature], 1),
                }
                for feature in average_importances
            ]

            # order by importance descendent
            result = sorted(result, key=lambda x: x["importance"])[::-1]

            self.shimoku.plt.horizontal_bar(
                data=result,
                x=["feature"],
                y=["importance"],
                order=self.order,
                cols_size=12,
            )
            self.order += 1

            # Partial Dependence
            self.shimoku.plt.html(
                html=self.shimoku.html_components.create_h1_title(
                    title=f"Partial Dependence",
                    subtitle="Measures the relationship between every feature and the cross selling probability",
                ),
                order=self.order,
            )
            self.order += 1

            self.shimoku.plt.html(
                html=self.shimoku.html_components.create_h1_title(
                    title="",
                    subtitle="Nominal features",
                ),
                order=self.order,
            )
            self.order += 1

            nominal_data = []
            for i in nominal:
                print(nominal.index(i), "nominal")

                count = []
                for _, row in df_product_filtered.iterrows():
                    x1 = row["Drivers"]
                    x2 = row["Barriers"]
                    x = {**x1, **x2}
                    try:
                        x = x[i]["val"]
                        count.append(x)
                    except KeyError:
                        pass

                x = Counter(count)
                x = [
                    {"Feature": key, "Probability": value, "Feature": i}
                    for key, value in x.items()
                ]
                nominal_data.extend(x)

            self.shimoku.plt.set_shared_data(
                dfs={f"nominal_data_{product}": pd.DataFrame(nominal_data)}
            )
            self.shimoku.plt.filter(
                order=self.order, data=f"nominal_data_{product}", field="Feature"
            )
            self.order += 1

            self.shimoku.plt.bar(
                data=f"nominal_data_{product}",
                y=["Probability"],
                x=["Feature"],
                order=self.order,
                cols_size=12,
            )
            self.order += 1

            self.shimoku.plt.html(
                html=self.shimoku.html_components.create_h1_title(
                    title="",
                    subtitle="Numerical features",
                ),
                order=self.order,
            )
            self.order += 1

            numerical_data = []
            for i in numerical:
                count = []
                for _, row in df_product_filtered.iterrows():
                    x1 = row["Drivers"]
                    x2 = row["Barriers"]
                    x = {**x1, **x2}
                    try:
                        x = x[i]["val"]
                        count.append(x)
                    except KeyError:
                        pass
                x = Counter(count)  # {'Rural': 6, 'Urbana': 4}
                x = [
                    {"Variable": k, "Probability": v, "Feature": i}
                    for k, v in x.items()
                ]
                numerical_data.extend(x)

            self.shimoku.plt.set_shared_data(
                dfs={f"numerical_data_{product}": pd.DataFrame(numerical_data)}
            )

            self.shimoku.plt.filter(
                order=self.order, data=f"numerical_data_{product}", field="Feature"
            )
            self.order += 1

            self.shimoku.plt.line(
                data=f"numerical_data_{product}",
                y=["Probability"],
                x=["Variable"],
                order=self.order,
                cols_size=12,
            )
            self.order += 1

            self.shimoku.plt.pop_out_of_tabs_group()
