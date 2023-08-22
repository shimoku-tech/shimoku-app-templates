"""SDK v.0.18
"""

from os import getenv

import shimoku_api_python as shimoku


def indicators_group(s: shimoku.Client) -> int:
    """Returns the order"""
    indicators_groups = [
        [
            {
                "description": "Previous period 17.200 €",
                "title": "Ad Cost",
                "value": "15.400€",
                "align": "left",
                "color": "success",
                "icon": 'Line/arrow-down',
            },
            {
                "description": "previous period 2.25€",
                "title": " CPC",
                "value": "2.29€",
                "align": "left",
                "color": "success",
                "icon": 'Line/arrow-up',
            },
            {
                "description": "Previous period 0.64%",
                "title": "CTR",
                "value": "0.62%",
                "align": "left",
                "color": "error",
                "icon": 'Line/arrow-down',
            },
            {
                "description": "Previous period ROI 103.6%",
                "title": "Expected ROI",
                "value": "104.1%",
                "align": "left",
                "color": "success",
                "variant": "contained",
                "icon": 'Line/arrow-up',
            }
        ]
    ]

    return s.plt.indicators_with_header(
        order=0, title='KPIs', subtitle='Month to date & comparison with previous period',
        indicators_groups=indicators_groups,
        indicators_parameters=dict(
            padding='0,0,0,1',
            cols_size=24,
        )
    )


def scatter_with_effect(s: shimoku.Client, order: int) -> None:
    main_scatter_points = [
        [1, 0.61], [2, 0.69], [4, 0.59], [5, .66], [7, .65],
        [8, 0.61], [9, 0.69], [10, 0.59], [11, .66], [12, .65],
        [13, 0.61], [14, 0.69], [15, 0.59], [16, .66], [17, .65],
        [18, 0.61], [19, 0.69], [20, 0.59], [21, .66], [22, .65],
        [23, 0.61], [24, 0.69], [25, 0.59], [27, .65],
    ]

    effect_points = [
        [3, 0.83], [6, 0.22], [26, .79],
    ]

    dataframed_scatter_points = [
        {'x': point[0], 'y': point[1]} for point in main_scatter_points
    ]

    s.plt.scatter_with_effect(
        data=dataframed_scatter_points,
        effect_points=effect_points,
        order=order,
        title='CTR anomalies',
        x_axis_name='Campaign day',
        y_axis_name='CTR (%)',
    )


def set_theme(s: shimoku.Client, workspace_id: str):
    theme = {
        "custom": {
            "dimensions": {
                "drawerWidth": 0
            }
        }
    }
    s.workspaces.update_workspace(workspace_id, theme=theme)


def main():
    async_exec: bool = getenv('ASYNC') == 'True'
    workspace_id: str = getenv('WORKSPACE_ID')
    menu_path = 'Ads Performance'
    api_key: str = getenv('API_TOKEN')
    universe_id: str = getenv('UNIVERSE_ID')

    s = shimoku.Client(
        access_token=api_key,
        universe_id=universe_id,
        verbosity='INFO',
        async_execution=async_exec,
    )
    s.set_workspace(workspace_id)
    s.set_menu_path(menu_path)

    order: int = indicators_group(s)
    scatter_with_effect(s, order)
    set_theme(s, workspace_id)

    if async_exec:
        s.run()


if __name__ == '__main__':
    main()
