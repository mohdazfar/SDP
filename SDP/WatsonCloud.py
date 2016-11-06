import json
from watson_developer_cloud import TradeoffAnalyticsV1



class WatsonCloud:
    username = '9a513c41-c7ef-4c4b-85fe-78dc3fc02818'
    paasword = '5GyKzkuu547q'

    def getTradeOffAnalyticsResult(self):
        tradeoff_analytics = TradeoffAnalyticsV1(username=self.username ,password= self.paasword)
        jsonFile = open('DataFile.json', 'r')
        problem_data=json.load(jsonFile)
        return json.dumps(tradeoff_analytics.dilemmas(problem_data),indent=3)