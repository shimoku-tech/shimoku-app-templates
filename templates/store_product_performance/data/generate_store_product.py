import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
from typing import List, Dict

# Initial Configuration
total_stores = 6  # Total number of stores
total_products = 50  # Assumed number of different products
date_ini = datetime(2023, 1, 2)  # Initial date
date_end = datetime(2024, 12, 25)  # End date, adjust as needed
output_file = "store_product_data.csv"
total_data = 10000  # Total data points to generate
sales_range = (100.00, 300.00)  # Range for generating random sales values


def generate_data() -> pd.DataFrame:
    """
    Generate sales data for retailers and save it to a CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the generated sales data.
    """

    def random_date(start_date: datetime, end_date: datetime) -> datetime:
        """
        Generate a random date between two given dates.

        Args:
            start_date (datetime): Start date.
            end_date (datetime): End date.

        Returns:
            datetime: Random date between start_date and end_date.
        """
        return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    data: Dict[str, List] = {
        "sale_id": [],
        "store_id": [],
        "product_id": [],
        "sale_date": [],
        "sales_amount": []
    }

    for i in range(total_data):
        sale_id: int = i + 1
        store_id: int = np.random.randint(1, total_stores + 1)
        # Use random.choices to select products more randomly
        product_id: int = random.choices(range(1, total_products + 1), k=1)[0]
        sale_date: datetime = random_date(date_ini, date_end)
        sales_amount: float = round(random.uniform(*sales_range), 2)

        data["sale_id"].append(sale_id)
        data["store_id"].append(store_id)
        data["product_id"].append(product_id)
        data["sale_date"].append(sale_date)
        data["sales_amount"].append(sales_amount)

    df: pd.DataFrame = pd.DataFrame(data)
    df["sale_date"] = pd.to_datetime(df["sale_date"]).dt.date
    df.sort_values(by="sale_date", inplace=True)

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)

    return df


if __name__ == "__main__":
    generate_data()
