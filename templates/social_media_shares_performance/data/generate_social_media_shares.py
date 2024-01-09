# DATA

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

total_data = 1000
output_file = "social_media_shares.csv"
date_ini = datetime(2023, 1, 1)
date_end = datetime.now() 
share_range = (0, 1000)

def generate_data():

    def random_date(start_date, end_date):
        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )


    n = total_data

    # post_date
    post_date_list = [random_date(date_ini, date_end) for _ in range(n)]
    post_date_list = sorted(post_date_list)


    # post_id
    post_id_list = [i for i in range(1, n+1)]


    # post_social_media
    post_social_media_list = (
        ["Facebook"] * int(n * 0.55)
        + ["Twitter"] * int(n * 0.25)
        + ["YouTube"] * int(n * 0.20)
    )
    random.shuffle(post_social_media_list)

    # post_shares
    post_shares_list = np.random.randint(share_range[0], share_range[1], size=n)
    

  

    
    # Create the DataFrame
    data = {
        "post_date": post_date_list,
        "post_id": post_id_list,
        "post_social_media": post_social_media_list,
        "post_shares": post_shares_list
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
