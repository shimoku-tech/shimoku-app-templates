# DATA

import pandas as pd
import random
from datetime import datetime, timedelta

total_data = 1000
output_file = "active_users.csv"
date_ini = datetime(2023, 1, 1)
date_end = datetime.now() # Current date

def generate_data():

    def random_date(start_date, end_date):
        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

    n = total_data

    user_ids = [
        "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        for _ in range(n)
    ]

    gender_set = (
        ["Male"] * int(n * 0.4)
        + ["Female"] * int(n * 0.6)
    )
    random.shuffle(gender_set)

    age_set = [random.randint(18, 74) for _ in range(n)]

    acquisition_source = (
        ["Organic"] * int(n * 0.3)
        + ["Google-Ads"] * int(n * 0.5)
        + ["Facebook"] * int(n * 0.2)
    )
    random.shuffle(acquisition_source)

    register_dates = [random_date(date_ini, date_end) for _ in range(n)]

    unregister_dates = [
        random_date(register_dates[i], date_end) if random.random() < 0.1 else None
        for i in range(n)
    ]

    last_login_dates = []
    for i in range(n):
        if unregister_dates[i] is not None:
            # If unregister_dates[i] is not None, choose a date between register_dates[i] and unregister_dates[i]
            last_login_dates.append(random_date(register_dates[i], unregister_dates[i]))
        else:
            # If unregister_dates[i] is None
            if random.random() < 0.5:
                # Generate a date within a window of X days backward from date_end
                days_to_past = timedelta(days=60)
                start_window = date_end - days_to_past
                last_login_dates.append(random_date(start_window, date_end))
            else:
                # Choose a date between register_dates[i] and date_end, generate a date within the window of register_dates[i] to date_end
                last_login_dates.append(random_date(register_dates[i], date_end))

    # Create the DataFrame
    data = {
        "user_id": user_ids,
        "register_date": register_dates,
        "unregister_date": unregister_dates,
        "last_login_date": last_login_dates,
        "gender": gender_set,
        "age": age_set,
        "acquisition_source": acquisition_source,
    }

    df = pd.DataFrame(data)

    # Display the DataFrame
    print("\n### Total registers generated: " + str(len(df)))
    print("\n")
    print(df.head(10))
    print("\n\n")

    # Save the dataframe to CSV
    df.to_csv(output_file, index=False)

    return df


if __name__ == "__main__":
    generate_data()
