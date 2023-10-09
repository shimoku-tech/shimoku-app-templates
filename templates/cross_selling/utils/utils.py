import pandas as pd
from functools import cached_property

from utils.settings import data_file, data_folder


def format_number(number):
    """
    Format a number with thousands separator used in SPAIN.

    Args:
        number: The number to format.

    Returns:
        str: The formatted number as a string.
    """
    return "{0:,}".format(number).replace(",", ".")


def read_csv(name: str, **kwargs) -> pd.DataFrame:
    """
    Read a CSV file and return its content as a DataFrame.

    Args:
        name (str): The name of the CSV file to read.
        **kwargs: Additional keyword arguments to pass to pd.read_csv().

    Returns:
        pd.DataFrame: The DataFrame containing the CSV data.
    """
    return pd.read_csv(f"utils/{data_folder}/{name}.csv", **kwargs)


class DFs:
    """
    Collection of DataFrames.

    This class represents a collection of DataFrames used for data analysis.
    """

    @cached_property
    def df(self) -> pd.DataFrame:
        """
        Get the primary DataFrame.

        Returns:
            pd.DataFrame: The primary DataFrame containing data.
        """
        x = read_csv(data_file)
        return x
