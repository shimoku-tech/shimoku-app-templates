import os
import shimoku_api_python as Shimoku

from tqdm import tqdm
from utils.utils import DFs
from utils.components.header import create_title_name_head
from utils.utils import format_number
from utils.transform import (
    count_column_values,
    count_column_values_with_filter,
    df_to_indicator_product_data,
)


class InsightsPage:
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
    
    @staticmethod
    def extract_features_from_dict(dictionary):
        data_list = []
        for feature, attributes in dictionary.items():
            x = attributes['prob'].strip('%')
            importance = abs(int(x))  # Extract and convert the 'prob' to absolute integer
            data_list.append({'feature': feature, 'importance': importance})
        return data_list

    def feature_importance(self, df_product):
        """
        Feature importance chart
        """
    
        self.shimoku.plt.html(
            html=self.shimoku.html_components.create_h1_title(
                title="Feature Importance",
                subtitle="Weight of each feature in the probability for cross selling",
            ),
            order=self.order,
        )
        self.order+=1

        all_variables = []

        for index, row in df_product.iterrows():
            drivers = self.string_to_dict(row['Drivers'])
            barriers = self.string_to_dict(row['Barriers'])
            
            all_variables.extend(self.extract_features_from_dict(drivers))
            all_variables.extend(self.extract_features_from_dict(barriers))
            
        # If you need to eliminate duplicates
        final_data = []
        seen_features = set()
        for item in all_variables:
            if item['feature'] not in seen_features:
                seen_features.add(item['feature'])
                final_data.append(item)

        # Ordenar final_data de menor a mayor importancia
        sorted_final_data = sorted(final_data, key=lambda x: x['importance'])
        sorted_final_data = sorted_final_data[::-1]  # Invertir la lista

        # Usar data_list para plotear la barra
        self.shimoku.plt.horizontal_bar(
            data=sorted_final_data,
            x="feature",
            # y no es necesario si solo estás usando una columna de 'Probability'
            x_axis_name="Category",
            order=self.order,  # Asegúrate de tener definido self.order en algún lugar de tu clase
            cols_size=12
        )
        self.order+=1


    @staticmethod
    def string_to_dict(s):
        elements = s.split(' - ')
        result = {}
        for element in elements:
            parts = element.split(' % ')
            name = parts[0].split(' ')[0].strip()

            if len(parts) == 1:  # Solo hay un elemento (como 'Edad 30% 50')
                prob_parts = parts[0].split(' ')
                prob = prob_parts[1] if len(prob_parts) > 1 else ''
                val = ' '.join(prob_parts[2:]) if len(prob_parts) > 2 else None
            else:
                prob_parts = parts[1].split(' ')
                prob = prob_parts[0] + '%' if len(prob_parts) > 0 else ''
                val = ' '.join(prob_parts[1:]) if len(prob_parts) > 1 else None

            result[name] = {'prob': prob, 'val': val}
        return result
    
    def compute(self, filter=False):
        
        list_of_products = self.dataframe['Product'].unique()

        for i in tqdm(list_of_products[:3]):

            # menu path set up
            self.shimoku.set_menu_path(self.menu_path, i)

            #just keep the i product
            df_product = self.dataframe[self.dataframe['Product'] == i]
            self.feature_importance(df_product)
