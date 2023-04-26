import pandas as pd
import numpy as np
import datetime

from app import origins, product_names

def gen_df(date_range, origins: list[str], product_names: list[str]):
    """
    Generates a Dataframe with random data
    """
    rng = np.random.default_rng() # Numpy random value generator

    df_size = 400 # Dataframe row size

    order_ids = list(range(df_size))
    order_choice = rng.choice(order_ids, size=df_size)

    dates = rng.choice(date_range, size=df_size)

    # Generate random values for the columns prod_billing and quantity
    prod_billing = rng.uniform(low=1, high=50, size=df_size)
    quantity = rng.integers(low=1, high=6, size=df_size)

    # Make a permutated list of origings
    origin = rng.choice(origins, size=df_size)
    product_name = rng.choice(product_names, size=df_size)

    # Craft the dataframe by date range
    df = pd.DataFrame(data={
        'date': dates,
        'order_id': order_choice,
        'prod_billing': prod_billing,
        'quantity': quantity,
        'origin': origin,
        'product_name': product_name
    })

    return df

def generate_dfs():
    """
    Generates two dataframes for two time periods, current week (cw)
    and last week (lw) an saves them to data/ folder as .csv files
    """
    # --- Calculate week start date for cw and lw ---

    # Start with last week (lw)
    lastweek_dtref = datetime.datetime.now() - datetime.timedelta(weeks=2)

    # Shift back lw to monday (start of the week)
    lastweek_start = lastweek_dtref - datetime.timedelta(days=lastweek_dtref.weekday())

    # Advance one week to get the start of the current week (cw)
    currentweek_start = lastweek_start + datetime.timedelta(weeks=1)

    # --- End week calculate week ---

    # Generate days of the week for cw and lw
    cw_range = pd.date_range(start=lastweek_start.date(), periods=7)
    lw_range = pd.date_range(start=currentweek_start.date(), periods=7)

    # Generate dataframes
    cw_data = gen_df(cw_range, origins, product_names)
    lw_data = gen_df(lw_range, origins, product_names)

    # Save dataframes to data/ folder
    cw_data.to_csv('data/cw_data.csv', index=False)
    lw_data.to_csv('data/lw_data.csv', index=False)

