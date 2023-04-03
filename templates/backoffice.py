"""Backoffice to review the businesses, apps, reports in an Universe
"""

from os import getenv
import logger
from collections import Counter
import json
from typing import List, Dict, Tuple

import datetime as dt
import pandas as pd

import shimoku_api_python as shimoku


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    stream=stdout,
    datefmt='%Y-%m-%d %H:%M',
    format='%(asctime)s | %(levelname)s | %(message)s'
)

api_key: str = getenv('API_TOKEN')
universe_id: str = getenv('UNIVERSE_ID')
environment: str = getenv('ENVIRONMENT')


s = shimoku.Client(
    config={'access_token': api_key},
    universe_id=universe_id,
    environment=environment,
)
menu_path: str = 'Backoffice'


def set_overview_page(
    businesses: List[Dict],
    app_types: List[Dict],
    apps: List[Dict],
    reports: List[Dict],
):
    menu_path_: str = f'{menu_path}/overview'
    data_overview_alert_indicator: List[Dict] = [
        {
            "description": "Number of Businesses",
            "title": "Businesses",
            "value": len(businesses),
            "color": "warning-background",
            "targetPath": f"/{menu_path_seed}/business-detail",
        },
        {
            "description": "Number of different apps",
            "title": "Apps types",
            "value": len(app_types),
            "color": "warning-background",
            "targetPath": f"/{menu_path_seed}/app-type-detail",
        },
        {
            "description": "Number of Apps",
            "title": "Apps",
            "value": len(apps),
            "color": "warning-background",
            "targetPath": f"/{menu_path_seed}/apps-detail",
        },
        {
            "description": "Number of Reports",
            "title": "Reports",
            "value": len(reports),
            "color": "warning-background",
            "targetPath": f"/{menu_path_seed}/reports-detail",
        },
    ]

    s.plt.alert_indicator(
        data=data_overview_alert_indicator,
        menu_path=menu_path_,
        order=0,
        value='value',
        header='title',
        footer='description',
        color='color',
        target_path='targetPath',
    )

    data_overview_indicator = [
        {
            "description": "Average apps per business",
            "title": "Average apps per business",
            "value": f'{round(len(apps) / len(businesses), 2)}',
        },
        {
            "description": "Average reports per app",
            "title": "Average reports per app",
            "value": f'{round(len(reports) / len(apps), 2)}',
        },
        {
            "description": "Average reports per business",
            "title": "Average reports per business",
            "value": f'{round(len(reports) / len(businesses), 2)}',
        },
    ]

    s.plt.indicator(
        data=data_overview_indicator,
        menu_path=menu_path_,
        order=1,
        value='value',
        header='title',
        footer='description',
    )


def set_business_detail(
    businesses: List[Dict],
    apps: List[Dict],
):
    menu_path_: str = f'{menu_path}/business-detail'
    df_ = pd.DataFrame(apps)
    apps_by_business = df_.groupby('appBusinessId')['id'].count().to_dict()
    for business_ in businesses:
        try:
            business_['apps number'] = apps_by_business[business_['id']]
        except KeyError:
            business_['apps number'] = 0
        business_['universe_id'] = business_['universe']['id']

    cols_to_keep: List[str] = [
        'id',
        'name',
        'apps number',
        'universe_id',
    ]
    business_df = pd.DataFrame(businesses)
    business_df = business_df[cols_to_keep]

    filter_columns: List[str] = []
    s.plt.table(
        data=business_df,
        menu_path=menu_path_,
        order=0,
        filter_columns=filter_columns,
    )


def set_app_type_detail(
    app_types: List[Dict],
    apps: List[Dict],
):
    menu_path_: str = f'{menu_path}/app-type-detail'
    for app_ in apps:
        app_['app_type_id'] = app_['type']['id']
    df_ = pd.DataFrame(apps)
    apps_by_type = df_.groupby('app_type_id')['id'].count().to_dict()
    for app_type in app_types:
        try:
            app_type['apps number'] = apps_by_type[app_type['id']]
        except KeyError:
            app_type['apps number'] = 0
        app_type['universe_id'] = app_type['universe']['id']

    cols_to_keep: List[str] = [
        'id',
        'name',
        'apps number',
        'universe_id',
    ]
    app_types_df = pd.DataFrame(app_types)
    app_types_df = app_types_df[cols_to_keep]

    filter_columns: List[str] = []
    s.plt.table(
        data=app_types_df,
        menu_path=menu_path_,
        order=0,
        filter_columns=filter_columns,
    )


def set_apps_detail(
    apps: List[Dict],
    reports: List[Dict],
):
    menu_path_: str = f'{menu_path}/apps-detail'
    df_ = pd.DataFrame(reports)
    reports_by_apps = df_.groupby('appId')['id'].count().to_dict()
    data_error: List[str] = []
    for app_ in apps:
        try:
            app_['apps number'] = reports_by_apps[app_['id']]
        except KeyError:
            # TODO this is to make an indicator
            data_error: List[str] = data_error + [app_['id']]

    filter_columns: List[str] = []
    apps_df: pd.DataFrame = pd.DataFrame(apps)
    cols_to_keep: List[str] = [
        'id', 'appBusinessId', 'createdAt',
    ]
    apps_df = apps_df[cols_to_keep]
    s.plt.table(
        data=apps_df,
        menu_path=menu_path_,
        order=0,
        filter_columns=filter_columns,
    )


def set_report_detail(reports: List[Dict]):
    if not reports:
        return

    menu_path_: str = f'{menu_path}/reports-detail'
    report_types: List[str] = [
        json.loads(report['dataFields'])['type'].capitalize()
        if report["reportType"] == 'ECHARTS'
        else report["reportType"].lower().capitalize()
        if report["reportType"]
        else 'Table'
        for report in reports
    ]

    data = dict(Counter(report_types))
    df = pd.DataFrame(data, index=[0]).T.reset_index()
    df.columns = ['report_type', 'count']
    s.plt.bar(
        data=df,
        title='Total number of reports by type in your apps',
        x='report_type', y=['count'],
        x_axis_name='Report Type', y_axis_name='Count',
        menu_path=menu_path_,
        order=0,
    )

    filter_columns: List[str] = []
    reports_df: pd.DataFrame = pd.DataFrame(reports)
    cols_to_keep: List[str] = [
        'id', 'appId', 'path', 'grid', 'createdAt', 'reportType',
    ]
    reports_df = reports_df[cols_to_keep]
    reports_df = reports_df.fillna('-')
    s.plt.table(
        data=reports_df,
        menu_path=menu_path_,
        order=1,
        title='All reports detail',
        filter_columns=filter_columns,
    )


def get_data() -> Tuple[List[str]]:
    businesses: List[Dict] = self.universe.get_universe_businesses()

    bo_business = [
        business for business in businesses
        if business['name'] == menu_path_seed
    ]
    if not bo_business:
        bo_business = self.business.create_business(name=menu_path_seed)
    else:
        bo_business = bo_business[0]
    business_id: str = bo_business['id']
    s.plt.set_business(business_id)

    app_types: List[Dict] = self.universe.get_universe_app_types()

    apps: List[Dict] = []
    for business in businesses:
        apps_temp: List[Dict] = self.business.get_business_apps(business['id'])
        apps = apps + apps_temp

    reports: List[Dict] = []
    for app in apps:
        try:
            reports_temp = self.app.get_app_reports(
                business_id=app['appBusinessId'],
                app_id=app['id'],
            )
        except Exception as e:
            continue
        reports = reports + reports_temp

    return businesses, app_types, apps, reports


def main():
    logger.info('Shimoku Backoffice - It takes about 5 minutes to be processed')
    start_time = dt.datetime.now()

    businesses, app_types, apps, reports = get_data()
    logger.info('Data retrieved')

    set_overview_page(
        businesses=businesses,
        app_types=app_types,
        apps=apps,
        reports=reports,
    )
    logger.info('Page "Overview" created')

    set_business_detail(
        businesses=businesses,
        apps=apps,
    )
    logger.info('Page "Business detail" created')

    set_app_type_detail(
        app_types=app_types,
        apps=apps,
    )
    logger.info('Page "Apptype detail" created')

    set_apps_detail(
        apps=apps,
        reports=reports,
    )
    logger.info('Page "Apps detail" created')

    set_report_detail(reports=reports)
    logger.info('Page "Report detail" created')

    end_time = dt.datetime.now()
    logger.info(f'Execution time: {end_time - start_time}')
