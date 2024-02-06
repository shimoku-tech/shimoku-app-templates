# DATA

import pandas as pd
import random
from datetime import datetime, timedelta
import names
from barnum import gen_data
from math import ceil

campaign_output_file = "campaign.csv"
model_output_file = "model.csv"
client_output_file = "client.csv"
model_by_campaign_output_file = "campaign_model.csv"
email_output_file = "email.csv"


total_campaign = 1
total_models = 2
total_clients = 50

total_model_by_campaign = 2
total_email_by_model = 4

date_ini = datetime(2024, 1, 24)
date_end = datetime(2024, 2, 7)


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
        for i in range(1,total_email_by_model):
            email_day = random_date(
                days[-1] + timedelta(days=2),
                end_date + timedelta(days=-3*(total_email_by_model-i-1))
            )
            days.append(email_day)
        days = [day.strftime('%m/%d/%Y') for day in days]
        return " ".join(days)

    def chunks(L, n):
        """ Yield successive n-sized chunks from L.
        """
        return [L[i:i+n] for i in range(0, len(L), n)]

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
        return groups

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


    # Campaign CSV
    campaign_ids = [
        "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
    for _ in range(total_campaign)]

    campaign_names = [
        " ".join(["Campaña", "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=2))])
    for _ in range(total_campaign)]

    campaign_start_date = [
        date_ini
    for _ in range(total_campaign)]

    campaign_end_date = [
        date_end
    for _ in range(total_campaign)]


    # Model CSV
    model_ids = [
        "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
    for _ in range(total_models)]

    model_names = [
        "".join(["Model", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]])
    for i in range(total_models)]

    # ToDo: generar texto con lipsum
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


    # Model by Campaign CSV
    model_by_campaign_ids = [
        "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
    for _ in range(total_model_by_campaign * total_campaign)]

    foreign_key_campaign_ids = [
        campaign_ids[ i // 2]
    for i in range(total_model_by_campaign * total_campaign)]

    chunk_model_ids = chunks(model_ids, total_model_by_campaign)

    foreign_key_model_ids = [
        model
    for i in range(total_campaign) for model in chunk_model_ids[i]]

    # delivery_days  = [
    #     random_secuence(date_ini, date_end)
    # for _ in range(total_campaign)]


    # Email CSV
    counts = [len(group) for group in chunk_into_n(client_id, total_models)]
    model_by_client = random.sample(model_by_campaign_ids, counts=counts, k=total_clients)

    rebound_flag = (
        [True] * int(total_clients * 0.2)
        + [False] * int(total_clients * 0.8)
    )
    random.shuffle(rebound_flag)

    rebound_email_by_client = sum(rebound_flag)

    total_emails = rebound_email_by_client + (total_clients - rebound_email_by_client) * total_email_by_model

    email_ids = [
        "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        for _ in range(total_emails)
    ]

    email_client_key = []
    email_rebound = []
    email_delivery_days = []

    # number_emails = lambda flag: 4 if not flag else 1
    # for client_index in range(total_clients):
    #     rebound_email = rebound_flag[client_index]
    #     n_emails = number_emails(rebound_email)
    #     for _ in range(n_emails):
    #         email_client_key += [client_id[client_index]]
    #         email_rebound += [rebound_email]



    # open_flag = [
    #     random_bolean(
    #         email_rebound[i],
    #         random.random() < 0.4
    #     )
    #     for i in range(total_emails)
    # ]

    # click_flag = [
    #     random_bolean(
    #         email_rebound[i],
    #         (random.random() < 0.06) & (open_flag[i] if pd.notna(open_flag[i]) else False)
    #     )
    #     for i in range(total_emails)
    # ]

    # answer_flag = [
    #     random_bolean(
    #         email_rebound[i],
    #         (random.random() < 0.01) & (open_flag[i] if pd.notna(open_flag[i]) else False)
    #     )
    #     for i in range(total_emails)
    # ]

    # Create the DataFrame
    data_campaign = {
        "id": campaign_ids,
        "name": campaign_names,
        "start_date": campaign_start_date,
        "end_date": campaign_end_date,
    }
    data_model = {
        "id": model_ids,
        "name": model_names,
        "subject": subjects,
    }
    data_client = {
        "id": client_id,
        "first_name": first_names,
        "last_name": last_names,
        "company_name": company_names,
    }
    data_model_by_campaign = {
        "id" : model_by_campaign_ids,
        "id_campaign": foreign_key_campaign_ids,
        "id_model": foreign_key_model_ids,
        # "delivery_days": delivery_days,
    }
    data_email = {
        "email_id": email_ids,
        # "rebound_flag": email_rebound,
        # "open_flag": open_flag,
        # "click_number": click_number,
        # "answer_flag": answer_flag,
        # "client_id": email_client_key,
    }

    df_compaign = pd.DataFrame(data_campaign)
    df_model = pd.DataFrame(data_model)
    df_client = pd.DataFrame(data_client)
    df_model_by_campaign = pd.DataFrame(data_model_by_campaign)
    # df_email = pd.DataFrame(data_email)

    # Display the DataFrame
    print("\n### Total Models registers generated: " + str(len(df_compaign)))
    print("\n")
    print(df_compaign.head(10))
    print("\n### Total Models registers generated: " + str(len(df_model)))
    print("\n")
    print(df_model.head(10))
    print("\n### Total Clients registers generated: " + str(len(df_client)))
    print("\n")
    print(df_client.head(10))
    print("\n### Total Models by Campaign registers generated: " + str(len(df_model_by_campaign)))
    print("\n")
    print(df_model_by_campaign.head(10))
    # print("\n### Total Emails registers generated: " + str(len(df_email)))
    # print("\n")
    # print(df_email.head(10))
    # print("\n\n")

    # Save the dataframe to CSV
    df_compaign.to_csv(campaign_output_file, index=False)
    df_model.to_csv(model_output_file, index=False)
    df_client.to_csv(client_output_file, index=False)
    df_model_by_campaign.to_csv(model_by_campaign_output_file, index=False)
    # df_email.to_csv(email_output_file, index=False)

    return {
        "compaign": df_compaign,
        "model": df_model,
        "client": df_client,
        "campaign_model": df_model_by_campaign,
        # "email": df_email,
    }


if __name__ == "__main__":
    generate_data()
