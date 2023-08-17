"""Backoffice to review the workspaces, menu_paths, components in an Universe
"""

from os import getenv
import logging
from collections import Counter
from typing import List, Dict, Tuple
from tenacity import RetryError
from copy import copy

import datetime as dt
import pandas as pd

import shimoku_api_python as shimoku

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    datefmt='%Y-%m-%d %H:%M',
    format='%(asctime)s | %(levelname)s | %(message)s'
)


def set_overview_page(
    s: shimoku.Client, workspaces: List[Dict], menu_paths: List[Dict], components: List[Dict], dashboard_id: str
):
    s.plt.change_path('Overview')
    data_overview_alert_indicator: List[Dict] = [
        {
            "description": "Number of Workspaces",
            "title": "Workspaces",
            "value": len(workspaces),
            "color": "warning-background",
            "targetPath": f"{dashboard_id}/backoffice/workspaces-detail",
        },
        {
            "description": "Number of Menu paths",
            "title": "Menu paths",
            "value": len(menu_paths),
            "color": "warning-background",
            "targetPath": f"{dashboard_id}/backoffice/menu-paths-detail",
        },
        {
            "description": "Number of Components",
            "title": "Components",
            "value": len(components),
            "color": "warning-background",
            "targetPath": f"{dashboard_id}/backoffice/components-detail",
        },
    ]

    s.plt.indicator(data=data_overview_alert_indicator, order=0)

    data_overview_indicator = [
        {
            "description": "Average menu paths per workspace",
            "title": "Average menu_paths per workspace",
            "value": f'{round(len(menu_paths) / len(workspaces), 2)}',
        },
        {
            "description": "Average components per menu path",
            "title": "Average components per menu_path",
            "value": f'{round(len(components) / len(menu_paths), 2)}',
        },
        {
            "description": "Average components per workspace",
            "title": "Average components per workspace",
            "value": f'{round(len(components) / len(workspaces), 2)}',
        },
    ]

    s.plt.indicator(data=data_overview_indicator, order=3)


def set_workspace_detail(s: shimoku.Client, workspaces: List[Dict]):
    s.plt.change_path('Workspaces Detail')
    for workspace_ in workspaces:
        workspace_['menu_paths number'] = len(s.workspaces.get_workspace_menu_paths(workspace_['id']))

    cols_to_keep: List[str] = ['id', 'name', 'menu_paths number']
    workspace_df = pd.DataFrame(workspaces)
    workspace_df = workspace_df[cols_to_keep]

    s.plt.table(data=workspace_df, order=0)


def set_menu_paths_detail(s: shimoku.Client, menu_paths: List[Dict]):
    s.plt.change_path('Menu Paths Detail')

    menu_paths_df: pd.DataFrame = pd.DataFrame(menu_paths)
    cols_to_keep: List[str] = [
        'id', 'name', 'order', 'hidePath', 'showBreadcrumb', 'showHistoryNavigation',
    ]
    menu_paths_df = menu_paths_df[cols_to_keep]
    s.plt.table(data=menu_paths_df, order=0)


def set_component_detail(s: shimoku.Client, components: List[Dict]):
    if not components:
        return

    s.plt.change_path('Components Detail')

    component_types: List[str] = [
        component['dataFields']['type'].capitalize()
        if component["reportType"] == 'ECHARTS'
        else component["reportType"].lower().capitalize()
        if component["reportType"]
        else 'Table'
        for component in components
    ]

    data = dict(Counter(component_types))
    df = pd.DataFrame(data, index=[0]).T.reset_index()
    df.columns = ['component_type', 'count']
    s.plt.bar(
        data=df,
        title='Total number of components by type in your menu_paths',
        x='component_type', y=['count'],
        x_axis_name='Component Type', y_axis_name='Count',
        order=0,
    )

    components_df: pd.DataFrame = pd.DataFrame(components)
    cols_to_keep: List[str] = [
        'id', 'order', 'path', 'reportType',
    ]
    components_df = components_df[cols_to_keep]
    components_df = components_df.fillna('-')
    s.plt.table(data=components_df, order=1, title='All components detail')


def get_data(s: shimoku.Client) -> Tuple[List[dict], List[dict], List[dict]]:
    non_permitted_workspaces = open('non_permitted_workspaces.txt', 'a+')
    read_non_permitted_workspaces = open('non_permitted_workspaces.txt', 'r')
    npw_l = read_non_permitted_workspaces.readlines()
    read_non_permitted_workspaces.close()
    new_non_permitted_workspaces = []
    workspaces: List[Dict] = s.universes.get_universe_workspaces(uuid=s.universe_id)
    menu_paths: List[Dict] = []
    components: List[Dict] = []

    for workspace in copy(workspaces):
        if workspace['id'] + '\n' in npw_l:
            workspaces.remove(workspace)
            continue
        try:
            menu_paths_temp: List[Dict] = s.workspaces.get_workspace_menu_paths(uuid=workspace['id'])
            menu_paths.extend(menu_paths_temp)
        except RetryError as e:
            new_non_permitted_workspaces.append(workspace['id'])
            logger.warning(f"No access permission to workspace {workspace['id']}")
            continue

        s.set_workspace(workspace['id'])
        for menu_path in menu_paths_temp:
            try:
                components_temp = s.menu_paths.get_menu_path_components(uuid=menu_path['id'])
            except RetryError as e:
                new_non_permitted_workspaces.append(workspace['id'])
                workspaces.remove(workspace)
                logger.warning(f"No access permission to menu_path {menu_path['id']}")
                continue
            components.extend(components_temp)

    if new_non_permitted_workspaces:
        new_non_permitted_workspaces = [f'{workspace}\n' for workspace in new_non_permitted_workspaces]
        non_permitted_workspaces.writelines(new_non_permitted_workspaces)

    non_permitted_workspaces.close()

    return workspaces, menu_paths, components


def main():
    logger.info('Shimoku Backoffice - It takes about 5 minutes to be processed')

    access_token: str = getenv('API_TOKEN')
    universe_id: str = getenv('UNIVERSE_ID')
    environment: str = getenv('ENVIRONMENT')
    workspace_id: str = getenv('WORKSPACE_ID')

    s = shimoku.Client(
        access_token=access_token,
        universe_id=universe_id,
        environment=environment,
        verbosity='INFO',
        async_execution=True,
    )
    s.reuse_data_sets()
    start_time = dt.datetime.now()

    workspaces, menu_paths, components = get_data(s)
    logger.info('Data retrieved')

    s.set_workspace(workspace_id)
    if not s.boards.get_board(name='Default Name'):
        s.boards.create_board(name='Default Name')
    dashboard_id = s.boards.get_board(name='Default Name')['id']

    s.set_menu_path('Backoffice')
    s.plt.clear_menu_path()

    set_overview_page(s, workspaces, menu_paths, components, dashboard_id)
    logger.info('Page "Overview" created')

    set_workspace_detail(s, workspaces)
    logger.info('Page "Workspace detail" created')

    set_menu_paths_detail(s, menu_paths)
    logger.info('Page "Menu paths detail" created')

    set_component_detail(s, components)
    logger.info('Page "Component detail" created')

    end_time = dt.datetime.now()
    logger.info(f'Execution time: {end_time - start_time}')

    s.run()


if __name__ == '__main__':
    main()
