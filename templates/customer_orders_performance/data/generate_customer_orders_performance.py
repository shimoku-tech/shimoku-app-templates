# DATA

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

total_data = 1000
output_file = "customer_orders_performance.csv"
date_ini = datetime(2023, 1, 1)
date_end = datetime.now()
total_customers = 150
cost_range = (15.00, 55.00)
benefit_factor_range = (1.3, 1.5)

def generate_data():

    def random_date(start_date, end_date):
        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

    n = total_data

    # order_date
    order_date_list = [random_date(date_ini, date_end) for _ in range(n)]
    order_date_list = sorted(order_date_list)

    # order_id
    order_id_list = [i for i in range(1, n+1)]

    # customer_id
    customer_id = [i for i in range(1, total_customers)]
    customer_id_list = np.random.choice(customer_id, size=n)

    # order_cost
    order_cost_list = np.round(np.random.uniform(cost_range[0], cost_range[1], size=n), 2)

    # order_spend
    benefit_factors = np.round(np.random.uniform(benefit_factor_range[0], benefit_factor_range[1], size=n), 2)
    order_spend_list = np.round(order_cost_list * benefit_factors, 2)

    # Create the DataFrame
    data = {
        "order_date": order_date_list,
        "order_id": order_id_list,
        "customer_id": customer_id_list,
        "order_cost": order_cost_list,
        "order_spend": order_spend_list,
    }

    df = pd.DataFrame(data)

    # Display the DataFrame
    print("\n### Output CSV: " + output_file + " (" + str(len(df)) + " registers)\n")
    print(df.head(10))
    print("\n")

    # Save the dataframe to CSV
    df.to_csv(output_file, index=False)

    return df


if __name__ == "__main__":
    generate_data()
