# DATA

import pandas as pd
import random
from datetime import datetime, timedelta
import names
from barnum import gen_data
from math import ceil


total_models = 2
total_clients = 50
email_by_model = 4

date_ini = datetime(2024, 1, 24)
date_end = datetime(2024, 2, 7)

model_output_file = "model.csv"
client_output_file = "client.csv"
email_output_file = "email.csv"


def generate_data() -> pd.DataFrame:
    """Generate CSV files with a data fake
    """

    def random_date(start_date: datetime, end_date: datetime) -> datetime:
        """Generate a random date between two dates using a uniform distribution.

        Args:
            start_date (datetime): start date
            end_date (datetime): end date

        Returns:
            datetime: random date
        """
        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

    def random_secuence(start_date: datetime, end_date: datetime) -> str:
        """Generate a random secuence of dates

        Args:
            start_date (datetime): start date
            end_date (datetime): end date

        Returns:
            str: String of the random secuences dates
        """
        days = [start_date]
        for i in range(1,email_by_model):
            email_day = random_date(
                days[-1] + timedelta(days=2),
                end_date + timedelta(days=-3*(email_by_model-i-1))
            )
            days.append(email_day)
        days = [day.strftime('%m/%d/%Y') for day in days]
        return " ".join(days)


    # Model CSV
    model_ids = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
        for i in range(total_models)
    ]

    delivery_days  = [
        random_secuence(date_ini, date_end)
    for _ in range(total_models)]

    subjects = [
        "Shimoku, la Inteligencia Artificial (IA) en la que se apoyan empresas como Amazon",
        "Shimoku, tu proyecto llave en mano de Inteligencia Artificial (IA) para sacarle el máximo partido a tu software",
    ]


    # Client CSV
    client_id = [
        "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        for _ in range(total_clients)
    ]

    client_fullnames = [names.get_full_name() for _ in range(total_clients)]

    first_names = [fullname.split(" ")[0] for fullname in client_fullnames]
    last_names = [fullname.split(" ")[1] for fullname in client_fullnames]

    company_names = [gen_data.create_company_name(biz_type="Generic") for _ in range(total_clients)]

    def chunk_into_n(lst: list, n: int) -> list:
        """Return a list with the number of elements of the n subgroup generate of lst

        Args:
            lst (list): list of elements
            n (int): number of chunks

        Returns:
            list: list of number of elements for each chunk
        """
        size = ceil(len(lst) / n)
        groups = list(map(lambda x: lst[x * size:x * size + size], list(range(n))))
        return [len(group) for group in groups]

    counts = chunk_into_n(client_id, total_models)
    model_by_client = random.sample(model_ids, counts=counts, k=total_clients)

    # Email CSV
    rebound_flag = (
        [True] * int(total_clients * 0.2)
        + [False] * int(total_clients * 0.8)
    )
    random.shuffle(rebound_flag)


    rebound_email_by_client = sum(rebound_flag)

    total_emails = rebound_email_by_client + (total_clients - rebound_email_by_client) * email_by_model


    email_id = [
        "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        for _ in range(total_emails)
    ]

    email_client_key = []
    email_rebound = []

    number_emails = lambda flag: 4 if not flag else 1
    for client_index in range(total_clients):
        rebound_email = rebound_flag[client_index]
        n_emails = number_emails(rebound_email)
        for _ in range(n_emails):
            email_client_key += [client_id[client_index]]
            email_rebound += [rebound_email]

    def random_bolean(flag_rebound: bool, flag: bool) -> bool:
        """Return a random value considering the flags

        Args:
            flag_rebound (bool): rebound flag
            flag (bool): flag if we get True or not

        Returns:
            bool: random bolean
        """
        if flag_rebound:
            return None
        else:
            return True if flag else False

    open_flag = [
        random_bolean(
            email_rebound[i],
            random.random() < 0.4
        )
        for i in range(total_emails)
    ]

    click_flag = [
        random_bolean(
            email_rebound[i],
            (random.random() < 0.06) & (open_flag[i] if pd.notna(open_flag[i]) else False)
        )
        for i in range(total_emails)
    ]

    answer_flag = [
        random_bolean(
            email_rebound[i],
            (random.random() < 0.01) & (open_flag[i] if pd.notna(open_flag[i]) else False)
        )
        for i in range(total_emails)
    ]

    # Create the DataFrame
    data_model = {
        "model_id": model_ids,
        "delivery_days": delivery_days,
        "subject": subjects,
    }
    data_client = {
        "client_id": client_id,
        "first_name": first_names,
        "last_name": last_names,
        "company_name": company_names,
        "model_id": model_by_client,
    }
    data_email = {
        "email_id": email_id,
        "client_id": email_client_key,
        "rebound_flag": email_rebound,
        "open_flag": open_flag,
        "click_flag": click_flag,
        "answer_flag": answer_flag,
    }

    df_model = pd.DataFrame(data_model)
    df_client = pd.DataFrame(data_client)
    df_email = pd.DataFrame(data_email)

    # Display the DataFrame
    print("\n### Total Models registers generated: " + str(len(df_model)))
    print("\n")
    print(df_model.head(10))
    print("\n### Total Clients registers generated: " + str(len(df_client)))
    print("\n")
    print(df_client.head(10))
    print("\n### Total Emails registers generated: " + str(len(df_email)))
    print("\n")
    print(df_email.head(10))
    print("\n\n")

    # Save the dataframe to CSV
    df_model.to_csv(model_output_file, index=False)
    df_client.to_csv(client_output_file, index=False)
    df_email.to_csv(email_output_file, index=False)

    return {
        "model": df_model,
        "client": df_client,
        "email": df_email,
    }


if __name__ == "__main__":
    generate_data()
