import json
import os
from os.path import join, dirname
from watson_developer_cloud import TradeoffAnalyticsV1
def trade_off(options,tfPrice,tfDuration,tfTransfer,thPrice,thRanking):
    if tfPrice is None:
        tfPrice='min'
    if tfDuration is None:
        tfDuration='min'
    if tfTransfer is None:
        tfTransfer='min'
    if thPrice is None:
        thPrice='min'
    if thRanking is None:
        thRanking='max'
    dic = {
        "columns": [
            {
                "key": "flight_price",
                "type": "numeric",
                "goal": tfPrice,
                "is_objective": True,
            },
            {
                "key": "duration",
                "type": "numeric",
                "goal": tfDuration,
                "is_objective": True
            },
            {
                "key": "transfer_count",
                "type": "numeric",
                "goal": tfTransfer,
                "is_objective": True
            },
            {
                "key": "room_price",
                "type": "numeric",
                "goal": thPrice,
                "is_objective": True
            },
            {
                "key": "ranking",
                "type": "numeric",
                "goal": thRanking,
                "is_objective": True
            }
        ],
        "options": options,
        "subject": "travel_packages"
    }

    return dic

def analysis(problem_data):
    tradeoff_analytics = TradeoffAnalyticsV1(
        username='4972bbad-c6dd-4e35-a7a8-2128caf813a9',
        password='sCl8MMeZJOM2')
    data=json.dumps(tradeoff_analytics.dilemmas(problem_data), indent=2)
    print(data)
    data = json.loads(data)
    results=data['resolution']['solutions']
    front=[]
    for result in results:
        if result['status']=='FRONT':
            front.append(result['solution_ref'])
    return front

