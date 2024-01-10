# DATA

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

total_data = 1000
output_file = "facebook_ads.csv"
date_ini = datetime(2023, 1, 1)
date_end = datetime.now() 
total_ads = 2
click_ratio = 80
cost_range = (0.05, 0.20)

def generate_data():

    def random_date(start_date: datetime, end_date: datetime):
        """
        Generates a random date within a specified date range.

        Parameters:
        start_date (datetime): The starting date of the range.
        end_date (datetime): The ending date of the range.

        Returns:
        datetime: A random date between start_date and end_date.
        """

        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )


    n = total_data

    # impression_date
    impression_date_list = [random_date(date_ini, date_end) for _ in range(n)]
    impression_date_list = sorted(impression_date_list)
    
    # ad_name
    ad_name = [f"Advertising-{i}" for i in range(1, total_ads + 1)]
    ad_name_list = np.random.choice(ad_name, size=n)
    
    # click
    click_list = np.random.choice([0, 1], size=n, p=[click_ratio/100, (100 - click_ratio)/100])

    # ad_cost
    ad_cost_list = np.round(np.random.uniform(cost_range[0], cost_range[1], size=n), 2)


    
    # Create the DataFrame
    data = {
        "impression_date": impression_date_list,
        "ad_name": ad_name_list,
        "click": click_list,
        "ad_cost": ad_cost_list
    }

    df = pd.DataFrame(data)
    df.sort_values(by='impression_date', inplace=True)

    # Display the DataFrame
    print("\n### Output CSV: " + output_file + " (" + str(len(df)) + " registers)\n")    
    print(df.head(10))
    print("\n")

    # Save the dataframe to CSV
    df.to_csv(output_file, index=False)

    
    return df


if __name__ == "__main__":
    generate_data()
