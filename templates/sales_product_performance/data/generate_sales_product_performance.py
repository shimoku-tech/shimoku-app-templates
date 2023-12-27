# DATA

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

total_data = 1000
output_file = "sales_product_performance.csv"
date_ini = datetime(2023, 1, 1)
date_end = datetime.now()
total_products = 5
cost_range = (15.00, 55.00)
benefit_factor_range = (1.3, 1.5)


def generate_data():
    def random_date(start_date, end_date):
        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

    n = total_data

    # sale_date
    sale_date_list = [random_date(date_ini, date_end) for _ in range(n)]

    # product_name
    product_names = [f"Product_{i}" for i in range(1, total_products + 1)]
    costs = np.round(
        np.random.uniform(cost_range[0], cost_range[1], size=total_products), 2
    )
    benefit_factors = np.round(
        np.random.uniform(
            benefit_factor_range[0],
            benefit_factor_range[1],
            size=total_products,
        ),
        2,
    )
    benefits = np.round(costs * benefit_factors, 2)

    products = {}
    for i, product_name in enumerate(product_names):
        products[product_name] = {
            "cost": costs[i],
            "benefit": benefits[i],
        }

    product_name_list = np.random.choice(product_names, size=n)

    # origin_campaign
    origin_campaign_list = (
        ["Organic"] * int(n * 0.25)
        + ["Email"] * int(n * 0.55)
        + ["Google-Ads"] * int(n * 0.05)
        + ["Facebook"] * int(n * 0.15)
    )
    random.shuffle(origin_campaign_list)

    # sale_type
    sale_type_list = ["Online"] * int(n * 0.4) + ["In-Store"] * int(n * 0.6)
    random.shuffle(sale_type_list)

    # revenue
    revenue_list = np.array(
        [products[product]["benefit"] for product in product_name_list]
    )

    # cost
    cost_list = np.array([products[product]["cost"] for product in product_name_list])

    # Create the DataFrame
    data = {
        "sale_date": sale_date_list,
        "product_name": product_name_list,
        "origin_campaign": origin_campaign_list,
        "sale_type": sale_type_list,
        "cost": cost_list,
        "revenue": revenue_list,
    }

    df = pd.DataFrame(data)
    df.sort_values(by="sale_date", inplace=True)

    # Display the DataFrame
    print("\n### Output CSV: " + output_file + " (" + str(len(df)) + " registers)\n")
    print(df.head(10))
    print("\n")

    # Save the dataframe to CSV
    df.to_csv(output_file, index=False)

    return df


if __name__ == "__main__":
    generate_data()
