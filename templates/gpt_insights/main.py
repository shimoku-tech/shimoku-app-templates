
from io import StringIO
import os
import time

import pandas as pd

import shimoku_api_python as Shimoku  # shimoku-api-python==1.6
from utils import drivers_barriers as db
from utils import partial_dependence as pdp


# Global variables
WORKSPACE = 'classification-insights'
BOARD = 'gpt-insights'
TARGET = 'Churn'
CLASS = 'True'
ID_COLUMNS = ['Customer']
TIMEOUT = 15*60


# Generic functions
def invoke_shimoku(menu_path: str) -> Shimoku.Client:
    """
    Initialize Shimoku client
    """
    s = Shimoku.Client(
        access_token=os.getenv("SHIMOKU_TOKEN"),
        universe_id=os.getenv("UNIVERSE_ID"),
        # environment='develop',
    )
    # s.disable_caching()

    # s.workspaces.create_workspace(name=WORKSPACE)
    # s.workspaces.delete_workspace(name=WORKSPACE)
    s.set_workspace(name=WORKSPACE)

    s.set_board(BOARD)

    s.set_menu_path(menu_path)

    return s


def wait_execution(run_id, menu_path):
    """
    Wait until the execution run_id is finished
    """
    start_time = time.time()
    while True:

        if time.time() - start_time > TIMEOUT:
            raise TimeoutError("The execution of the function has exceeded the timeout")

        # Restart session to get access to new generated files
        s = invoke_shimoku(menu_path=menu_path)

        # Check if the execution is finished
        list_executions = s.ai.get_output_files_by_ai_function(ai_function='generate_insights')
        if any(exe['run_id'] == run_id for exe in list_executions):
            break

    return s


# Paths functions
def partial_dependence_insights(
        menu_path: str, openai_api_key: str, openai_org_id: str):
    """
    Partial dependence with insights generation page
    """

    #----------------- INITIALIZE CLIENT ----------------#
    s = invoke_shimoku(menu_path=menu_path)
    s.plt.clear_menu_path()

    #--------------- GET THE INPUT DATA ----------------#

    # input data extracted from train_classification function.
    # See https://app.gitbook.com/o/X8cW9XXRSJZA1OtcVKh6/s/UlHTfmIZY46Z1EDfyGMz/~/changes/405/getting-started/artificial-intelligence/classification/train-classification
    df_pd = pd.read_csv('./data/df_pdp.csv')

    #--------------- TRANSFORM DATA ----------------#

    # Filter
    df_pd = pdp.format_data(
        list_df=[df_pd], output_target=TARGET, output_class=CLASS)[0]

    # Get list of features
    # input_features = df_pd['name_feature'].unique()

    # Warning: dataframe must be truncated to avoid 15 minutes limit
    input_features = df_pd['name_feature'].unique()[:8]
    df_pd = df_pd[df_pd['name_feature'].isin(input_features)]

    #--------------- GENERATE INSIGHTS ----------------#
    # https://app.gitbook.com/o/X8cW9XXRSJZA1OtcVKh6/s/UlHTfmIZY46Z1EDfyGMz/~/changes/405/getting-started/artificial-intelligence/generate-insights

    # Upload files to Shimoku
    s.ai.create_input_files(
        input_files={'pd_data': df_pd.to_csv(index=False).encode()},
        force_overwrite=True
    )

    run_id = s.ai.generic_execute(
        ai_function='generate_insights',
        task='partial_dependence',
        data='pd_data',
        openai_api_key=openai_api_key,
        openai_org_id=openai_org_id,
    )

    # Waiting until the execution is finished
    s = wait_execution(run_id, menu_path)

    # Accessing the gpt insights
    output_files = s.ai.get_output_file_objects(run_id=run_id)
    df_insights = pd.read_csv(StringIO(output_files['df_insights.csv'][0].decode('utf-8')))

    # --------------- CREATE DASHBOARD TASKS ----------------#
    order = 0
    order = pdp.page_header(s, order)
    order = pdp.pd_tabs(s, order, pdp.rename_columns(df_pd), df_insights, input_features)
    s.run()

    return True


def drivers_barriers_insights(
        menu_path: str, nrows: int,
        openai_api_key: str, openai_org_id: str):
    """
    Drivers & barriers with insights generation page
    """

    #----------------- INITIALIZE CLIENT ----------------#

    s = invoke_shimoku(menu_path=menu_path)
    s.plt.clear_menu_path()

    #--------------- GET THE INPUT DATA ----------------#

    # input data extracted from train_classification function.
    # See https://app.gitbook.com/o/X8cW9XXRSJZA1OtcVKh6/s/UlHTfmIZY46Z1EDfyGMz/~/changes/405/getting-started/artificial-intelligence/classification/train-classification
    df_input = pd.read_csv('./data/df_input.csv')
    df_predicted = pd.read_csv('./data/df_predicted.csv')
    df_shap = pd.read_csv('./data/df_shap.csv')
    df_db = pd.read_csv('./data/df_db.csv')

    #--------------- TRANSFORM DATA ----------------#

    # Get customers prone to churn
    df_top, (df_shap, df_db) = db.format_data(
        df_predicted=df_predicted,
        list_df=[df_shap, df_db],
        nrows=nrows, id_columns=ID_COLUMNS,
        output_target=TARGET, output_class=CLASS)

    #--------------- GENERATE INSIGHTS ----------------#
    # https://app.gitbook.com/o/X8cW9XXRSJZA1OtcVKh6/s/UlHTfmIZY46Z1EDfyGMz/~/changes/405/getting-started/artificial-intelligence/generate-insights

    # Upload files to Shimoku
    s.ai.create_input_files(
        input_files={'input_data': df_input.to_csv(index=False).encode(),
                     'db_data': df_db.to_csv(index=False).encode()},
        force_overwrite=True
    )

    # Execute the generate insight function
    run_id = s.ai.generic_execute(
        ai_function='generate_insights',
        task='drivers_barriers',
        data='db_data',
        context_data='input_data',
        openai_api_key=openai_api_key,
        openai_org_id=openai_org_id,
    )

    # Waiting until the execution is finished
    s = wait_execution(run_id, menu_path)

    # Accessing the gpt insights
    output_files = s.ai.get_output_file_objects(run_id=run_id)
    df_insights = pd.read_csv(StringIO(output_files['df_insights.csv'][0].decode('utf-8')))

    # --------------- CREATE DASHBOARD TASKS ----------------#

    order = 0
    order = db.page_header(s, order)
    order = db.table_header(s, order, TARGET, nrows)
    order = db.table(s, order, df_db, menu_path, ID_COLUMNS)
    order = db.users_insights(s, order, df_top, df_shap, df_insights, ID_COLUMNS)
    s.run()

    return True


def generic_insights():
    pass


if __name__ == "__main__":

    #----------------- OPENAI CREDENTIALS ----------------#
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_org_id = os.getenv("OPENAI_ORG_ID")

    #----------------- PARTIAL DEPENDENCE INSIGHTS ----------------#
    partial_dependence_insights(
        menu_path='partial_dependence', openai_api_key=openai_api_key,
        openai_org_id=openai_org_id)

    #----------------- DRIVERS & DRIVERS INSIGHTS ----------------#
    drivers_barriers_insights(
        menu_path='drivers_barriers', nrows=10,
        openai_api_key=openai_api_key, openai_org_id=openai_org_id)

    #----------------- GENERIC INSIGHTS ----------------#
    # generic_insights(
    #     menu_path='drivers_barriers', openai_api_key=openai_api_key,
    #     openai_org_id=openai_org_id)
