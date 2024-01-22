import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Initial Configuration
total_stores = 6
total_users = 2500
date_ini = datetime(2023, 1, 1)
date_end = datetime(2025, 1, 1)
output_file = "retailer_sales_data.csv"
total_data = 10000  # Total number of data points to generate
sales_range = (10.00, 80.00)  # Range for generating random sales values


def generate_data() -> pd.DataFrame:
    """
    Generate retailer sales data and save it to a CSV file.

    Returns:
        pd.DataFrame: DataFrame containing generated sales data.
    """

    def random_date(start_date, end_date):
        """
        Generate a random date between two given dates.

        Args:
            start_date (datetime): Start date.
            end_date (datetime): End date.

        Returns:
            datetime: Random date between start_date and end_date.
        """
        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

    data = {
        "sale_id": [],
        "store_id": [],
        "user_id": [],
        "sale_date": [],
        "sales_amount": [],
    }

    for i in range(total_data):
        sale_id = i + 1
        store_id = np.random.randint(1, total_stores + 1)
        user_id = np.random.randint(1, total_users + 1)
        sale_date = random_date(date_ini, date_end)
        sales_amount = round(random.uniform(*sales_range), 2)

        data["sale_id"].append(sale_id)
        data["store_id"].append(store_id)
        data["user_id"].append(user_id)
        data["sale_date"].append(sale_date)
        data["sales_amount"].append(sales_amount)

    df = pd.DataFrame(data)
    df["sale_date"] = pd.to_datetime(df["sale_date"]).dt.date
    df.sort_values(by="sale_date", inplace=True)
    # Save the dataframe to a CSV file
    df.to_csv(output_file, index=False)
    return df


if __name__ == "__main__":
    generate_data()
