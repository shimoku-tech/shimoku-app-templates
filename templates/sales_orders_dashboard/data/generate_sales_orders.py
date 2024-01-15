# DATA

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

total_data = 1000
output_file = "sales_orders.csv"
date_ini = datetime(2023, 1, 1)
date_end = datetime.now() 
total_customers = 150
spend_range = (20.00, 200.00)

def generate_data()-> pd.DataFrame:

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
    
    # order_spend
    order_spend_list = np.round(np.random.uniform(spend_range[0], spend_range[1], size=n), 2)

    # market_segment
    market_segment_list = (
        ["Electronics"] * int(n * 0.58)
        + ["Household items"] * int(n * 0.15)
        + ["Food and nutrition"] * int(n * 0.27)
    )
    random.shuffle(market_segment_list)

    # geo_segment
    geo_segment_list = (
        ["National"] * int(n * 0.72)
        + ["International"] * int(n * 0.28)
    )
    random.shuffle(geo_segment_list)


    
    # Create the DataFrame
    data = {
        "order_date": order_date_list,
        "order_id": order_id_list,
        "customer_id": customer_id_list,
        "order_spend": order_spend_list,
        "market_segment": market_segment_list,
        "geo_segment": geo_segment_list
    }

    df = pd.DataFrame(data)
    df.sort_values(by='order_date', inplace=True)

    # Display the DataFrame
    print("\n### Output CSV: " + output_file + " (" + str(len(df)) + " registers)\n")    
    print(df.head(10))
    print("\n")

    # Save the dataframe to CSV
    df.to_csv(output_file, index=False)

    
    return df


if __name__ == "__main__":
    generate_data()
