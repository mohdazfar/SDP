import json
import requests
from city_code import *

# def ManageCity(city):
#     link = "https://iatacodes.org/api/v6/cities?api_key=5276c2c4-0d42-4423-b758-733794c23f1e"
#     r = requests.get(link)
#     data = json.loads(r.text)
#     result_list = data['response']
#     for result in result_list:
#         if (result['name'] == city):
#             return result['code']

def getFlightData(origin, destination, dateOfDeparture, dateOfreturn):
    api_key = "AIzaSyCFe4aroUT5mXbLx450-AvAQYC5GLPBwYk"
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
    headers = {'content-type': 'application/json'}
    flight_From = {'origin': city(origin), 'destination': city(destination), 'date': dateOfDeparture}
    flight_Return={'origin': city(destination), 'destination': city(origin), 'date': dateOfreturn}
    flightInfo=[flight_From,flight_Return]

    params = {'request': {'slice': flightInfo, 'passengers': {'adultCount': 1}, 'solutions': 3, 'refundable': False}}
    print(params)
    request = requests.post(url, data=json.dumps(params), headers=headers)
    data = json.loads(request.text)
    # print(data)
    options = data['trips']['tripOption']

    airportName = {}
    airports = data['trips']['data']['airport']
    for airport in airports:
        airportName[airport['code']] = airport['name']

    flightList = []
    count=1
    for option in options:
        flight_package={}
        price = {'Currency': option['saleTotal'][:3], 'Price': option['saleTotal'][3:]}
        flight = {}
        flight['price']=price
        slices = option['slice']
        twoWay=[]
        for slice in slices:
            oneWay_package={}
            segments = slice['segment']
            duration=slice['duration']
            oneWay_package['duration']=duration
            oneWay = []
            for segment in segments:
                detail={}
                flight_Number=segment['flight']['number']
                legs = segment['leg']
                for leg in legs:

                    detail['departureTime']=leg['departureTime']
                    detail['arrivalTime'] = leg['arrivalTime']
                    detail['origin']=airportName[leg['origin']]
                    detail['destination'] = airportName[leg['destination']]
                oneWay.append(detail)
            oneWay_package['info']=oneWay
            twoWay.append(oneWay_package)
        flight['flight_info']=twoWay

        flight_package['flight'+str(count)]=flight
        count=count+1
        flightList.append(flight_package)

    return flightList

# def getTradeOff(flightList):
#     trade_f = []
#     for i in range(len(flightList)):
#         package={}
#         result={}
#         flight = flightList[i]['flight' + str(i + 1)]
#         price = flight['price']['Price']
#
#         durations = flight['flight_info']
#         durationList = []
#         for duration in durations:
#             durationList.append(duration['duration'])
#
#         time = 0
#         for j in range(len(durationList)):
#             time += durationList[j]
#
#         package['flight_price']=price
#         package['duration']=time
#         result['flight'+str(i+1)]=package
#         trade_f.append(result)
#     print(trade_f)
# data=getFlightData('Helsinki','Paris','2016-11-08','2016-11-9')
# print(data)
# getTradeOff(data)



