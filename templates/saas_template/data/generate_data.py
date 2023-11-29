# DATOS

import pandas as pd
import random
from datetime import datetime, timedelta


def generate_active_users():
    # Función para generar una fecha aleatoria entre dos fechas dadas
    def random_date(start_date, end_date):
        return start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

    # Definición de las reglas
    n = 1000  # Número de registros
    user_ids = [
        "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        for _ in range(n)
    ]
    account_types = (
        ["FREE"] * int(n * 0.6)
        + ["PREMIUM"] * int(n * 0.3)
        + ["ENTERPRISE"] * int(n * 0.1)
    )
    random.shuffle(account_types)

    # Obtén la fecha y hora actual como fecha máxima de eventos
    current_date = datetime.now()

    register_dates = [random_date(datetime(2023, 1, 1), current_date) for _ in range(n)]

    unregister_dates = [
        random_date(register_dates[i], current_date) if random.random() < 0.1 else None
        for i in range(n)
    ]

    last_login_dates = []
    for i in range(n):
        if unregister_dates[i] is not None:
            # Si unregister_dates[i] no es None, elige una fecha entre register_dates[i] y unregister_dates[i]
            last_login_dates.append(random_date(register_dates[i], unregister_dates[i]))
        else:
            # # Si unregister_dates[i] es None, elige una fecha entre register_dates[i] y current_date
            # last_login_dates.append(random_date(register_dates[i], current_date))

            if random.random() < 0.5:
                # Genera una fecha dentro de una ventana de X días hacia atrás desde current_date
                days_to_past = timedelta(days=60)
                start_window = current_date - days_to_past
                last_login_dates.append(random_date(start_window, current_date))
            else:
                # Genera una fecha dentro de la ventana de register_dates[i] a current_date
                last_login_dates.append(random_date(register_dates[i], current_date))

    subscription_dates = []
    for i in range(n):
        if random.random() < 0.35:
            subscription_dates.append(None)
        else:
            if unregister_dates[i] is not None:
                # Si unregister_dates[i] no es None, elige una fecha entre register_dates[i] y unregister_dates[i]
                subscription_dates.append(
                    random_date(register_dates[i], unregister_dates[i])
                )
            else:
                # Si unregister_dates[i] es None, elige una fecha entre register_dates[i] y current_date
                subscription_dates.append(random_date(register_dates[i], current_date))

    unsubscription_dates = []
    for i in range(n):
        if subscription_dates[i] is None:
            unsubscription_dates.append(None)
        else:
            if random.random() > 0.20:
                unsubscription_dates.append(None)
            else:
                if unregister_dates[i] is not None:
                    # Si unregister_dates[i] no es None, elige una fecha entre register_dates[i] y unregister_dates[i]
                    unsubscription_dates.append(
                        random_date(subscription_dates[i], unregister_dates[i])
                    )
                else:
                    # Si unregister_dates[i] es None, asumimos el último día del año 2023
                    unsubscription_dates.append(
                        random_date(subscription_dates[i], current_date)
                    )

    # Crear el DataFrame
    data = {
        "user_id": user_ids,
        "register_date": register_dates,
        "unregister_date": unregister_dates,
        "last_login_date": last_login_dates,
        "subscription_date": subscription_dates,
        "unsubscription_date": unsubscription_dates,
        "account_type": account_types,
    }

    df = pd.DataFrame(data)

    # Mostrar el DataFrame
    print(
        "\n########################  ALL DATA GENERATED: "
        + str(len(df))
        + "###############################################################\n"
    )
    print(df.head())
    print(
        "\n#################################################################################################################"
    )

    # Guardar dataframe en CSV
    df.to_csv(f"data/active_users.csv", index=False)

    #################################################################################################### PREGUNTAS

    # Registered Users
    registered_users = df[df["unregister_date"].isna()]

    # Unsubscribed Users
    unregistered_users = df[~df["unregister_date"].isna()]

    # Active Users in the Last 24 Hours
    today = datetime(2023, 9, 23)  # You can change this date as needed
    active_users_24h = df[
        (df["last_login_date"] >= today - timedelta(days=1))
        & (df["last_login_date"] <= today)
    ]

    # Active Users in the Last Month
    last_month = today - timedelta(days=30)
    active_users_month = df[
        (df["last_login_date"] >= last_month) & (df["last_login_date"] <= today)
    ]

    # New Users in the Last Month
    new_users_month = df[
        (df["register_date"] >= last_month) & (df["register_date"] <= today)
    ]

    # Subscribers
    subscribers = df[
        (df["subscription_date"].notna())
        & (df["unsubscription_date"].isna())
        & (df["unregister_date"].isna())
    ]

    # You can print or work with these DataFrames as needed
    print("\n########################  Registered Users: " + str(len(registered_users)))
    print(registered_users)

    print(
        "\n########################  Unregistered Users: "
        + str(len(unregistered_users))
    )
    print(unregistered_users)

    print(
        "\n######################## Active Users in the Last 24 Hours:"
        + str(len(active_users_24h))
    )
    print(active_users_24h)

    print(
        "\n######################## Active Users in the Last Month:"
        + str(len(active_users_month))
    )
    print(active_users_month)

    print(
        "\n######################## New Users in the Last Month:"
        + str(len(new_users_month))
    )
    print(new_users_month)

    print("\n######################## Subscribers (corrected):" + str(len(subscribers)))
    print(subscribers)

    return df


if __name__ == "__main__":
    generate_active_users()
