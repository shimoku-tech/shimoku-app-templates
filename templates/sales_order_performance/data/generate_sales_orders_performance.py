import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Total number of data points to generate
total_data = 1000

# Output file path for the generated data
output_file = "data/sales_orders_performance.csv"

# Initial and final dates for order_date generation
date_ini = datetime(2023, 1, 1)
date_end = datetime.now()

# Range for generating random order_cost values
cost_range = (15.00, 55.00)

# Range for generating random benefit factors to calculate order_spend
benefit_factor_range = (1.3, 1.5)


def generate_data():
    """
    Generates synthetic sales order performance data and saves it to a CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the generated data.
    """

    def random_date(start_date, end_date):
        """
        Generates a random date between start_date and end_date.

        Args:
        start_date (datetime): The start date.
        end_date (datetime): The end date.

        Returns:
        datetime: A random date between start_date and end_date.
        """
        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

    n = total_data

    # Generate random order dates
    order_date_list = [random_date(date_ini, date_end) for _ in range(n)]
    order_date_list = sorted(order_date_list)

    # Generate sequential order IDs
    order_id_list = [i for i in range(1, n + 1)]

    # Generate random order costs within the specified range
    order_cost_list = np.round(
        np.random.uniform(cost_range[0], cost_range[1], size=n), 2
    )

    # Generate random benefit factors and calculate order spend
    benefit_factors = np.round(
        np.random.uniform(benefit_factor_range[0], benefit_factor_range[1], size=n), 2
    )
    order_spend_list = np.round(order_cost_list * benefit_factors, 2)

    # Create the DataFrame
    data = {
        "order_date": order_date_list,
        "order_id": order_id_list,
        "order_cost": order_cost_list,
        "order_spend": order_spend_list,
    }

    df = pd.DataFrame(data)
    df.sort_values(by="order_date", inplace=True)

    # Display the DataFrame
    print("\n### Output CSV: " + output_file + " (" + str(len(df)) + " records)\n")
    print(df.head(10))
    print("\n")

    # Save the dataframe to CSV
    df.to_csv(output_file, index=False)

    return df


if __name__ == "__main__":
    generate_data()
