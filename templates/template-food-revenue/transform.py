import pandas as pd

def human_format(num):
    """
    Format long nombers with letter exponentials
    Ex: 999999 -> 999K
    """

    # https://stackoverflow.com/a/45846841
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def filter_by_origin(data: pd.DataFrame, origin=""):
    """
    Filter by origin
    - origin: web, app_mobile, store, all
    """

    if origin == "web":
        return data.query(f"origin == 'web'")
    if origin == "app_mobile":
        return data.query(f"origin == 'app_mobile'")
    if origin == "store":
        return data.query(f"origin == 'store'")

    # origin == all
    return data
