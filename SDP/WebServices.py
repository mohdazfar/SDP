from urllib.request import urlopen
import requests
import json
import pandas as pd
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from WatsonCloud import WatsonCloud

class WebServices:

    HotelAPIKey = '3644ac54270d20d577ae19a86c698d1f'
    FlightAPIKey = 'AIzaSyBRE0XB8Z_6AOvcBd0Ia1xlFOxnhnIt2cE'
    iataAPIKey = '5276c2c4-0d42-4423-b758-733794c23f1e'

    def ManageCitie(self):
        domainName = 'https://iatacodes.org/api/v6/cities?api_key='
        url = domainName + self.iataAPIKey
        response = urlopen(url).read()
        jsonList = json.loads(response.decode('utf-8'))
        jsonList  = jsonList['response']
        parseData = []
        for i in range(len(jsonList)):
            parseData.append([jsonList[i]['country_code'], jsonList[i]['code'], jsonList[i]['name']])
        toFrame = pd.DataFrame(parseData, columns=['Country_code', 'Code', 'Name'] )
        toFrame.to_csv('Cities.csv', sep = ',', encoding='utf-8', index=False)



    def getFlightData(self, origin, destination, dateOfDeparture, possibleflights):
        domainName = "https://www.googleapis.com/qpxExpress/v1/trips/search?key="
        url = domainName + self.FlightAPIKey
        headers = {'content-type': 'application/json'}
        flightInfo = {'origin':origin, 'destination':destination, 'date':dateOfDeparture}
        params = {'request':{'slice': [flightInfo],'passengers':{'adultCount':1},'solutions':possibleflights,'refundable':False}}
        request = requests.post(url, data=json.dumps(params),  headers=headers)
        data = json.loads(request.text)
        print(data)
        options = data['trips']['tripOption']
        carriers = data['trips']['data']['carrier']
        carrierInfo = {}
        for carrier in carriers:
            carrierInfo[carrier['code']] = carrier['name']

        airportName = {}
        airports= data['trips']['data']['airport']
        for airport in airports:
            airportName[airport['code']]=airport['name']

        jsonResult ={}
        routeNumber = 0
        for option in options:
            routeNumber += 1
            price = {'Currency': option['saleTotal'][:3], 'Price': option['saleTotal'][3:]}
            slicesOfTrips = option['slice']
            singleFlightInfo = []

            for singleSlice in slicesOfTrips:
                midResult = []
                for singleFlight in singleSlice['segment']:
                    flightNumber = singleFlight['flight']['number']
                    carrierCode = singleFlight['flight']['carrier']

                    for leg in singleFlight['leg']:
                        singleFlightInfo.append( {'FlightNumber':flightNumber,'Airline':carrierInfo[carrierCode],
                                                 'DepartureTime': leg['departureTime'], 'ArrivalTime':leg['arrivalTime'],
                                                 'OriginCity':airportName[leg['origin']], 'DestinationCity':airportName[leg['destination']]})
                    midResult.append(singleFlightInfo)

            jsonResult.update({'RouteNumber ' + str(routeNumber) : [price, singleFlightInfo]})
        return jsonResult


    def getHotelsDestinationIDData(self):
        domainName = 'http://api.tripexpert.com/v1/destinations?api_key='
        url = domainName + self.HotelAPIKey
        data = urlopen(url).read().decode('utf-8')
        jsonData = json.loads(data)
        jsonData = jsonData['response']['destinations']
        parseData = []
        for info in jsonData:
            destinationID = info['id']
            cityName = info['name']
            countryName = info['country_name']
            parseData.append([destinationID, cityName, countryName])
        toFrame = pd.DataFrame(parseData, columns=['DestinationID', 'CityName', 'countryName'])
        toFrame.to_csv('DestinationForHotelsAPI.csv', sep = ',', encoding='utf-8', index=False)


    def getHotelData(self, destinationCity, ArrivalDatetoDestination, numberOfDays):
        df = pd.read_csv('DestinationForHotelsAPI.csv', encoding = 'latin-1')
        destinationID = df['DestinationID'].tolist()
        cityName = df['CityName'].tolist()

        # DATE PARSING
        parseDate = str(parser.parse(str(ArrivalDatetoDestination)))
        date = parseDate.split(' ')[0]
        checkInDate = datetime.strptime(date, '%Y-%m-%d')
        checkInDate = checkInDate.strftime('%m/%d/%Y')
        toDate = datetime.strptime(checkInDate,'%m/%d/%Y').date()
        checkOutDate  = toDate + timedelta(days = numberOfDays)
        checkOutDate = checkOutDate.strftime('%m/%d/%Y')

        try:
            index = cityName.index(destinationCity)
            cityID = str(destinationID[index])
        except:
            print('City name mentioned is not in the hotel API list')

        url = 'http://api.tripexpert.com/v1/venues?destination_id=' + cityID +'&limit=10&check_in=' + checkInDate + '&check_out=' + checkOutDate +'&api_key=' + self.HotelAPIKey
        response = urlopen(url).read().decode('utf-8')
        response = json.loads(response)
        totalVenues = response['response']['venues']
        venueList = []
        for venue in totalVenues:
            hotelGeoLat =  venue['latitude']
            hotelGeoLong = venue['longitude']
            hotelName = venue['name']
            pricePerDay = venue['low_rate']
            ranking = venue['tripexpert_score']
            Currency = 'US Dollars ($)'
            venueList.append({'Hotel_Name':hotelName, 'Price_Per_Day':pricePerDay, 'Currency':Currency, 'Hotel_Ranking':ranking, 'Latitude':hotelGeoLat, 'Longitude':hotelGeoLong})

        hotelMap = {}
        for i in range (len(venueList)):
            hotelMap.update({'Hotel'+str(i):venueList[i]})
        return hotelMap

    def cityCodeToCityName(self, city):
        df = pd.read_csv('Cities.csv', encoding = 'latin-1')
        cityNames = df['Name'].tolist()
        cityCodes = df['Code'].tolist()

        try:
            index = cityCodes.index(city)
            cityAbbreviation = cityNames[index]
        except Exception as e:
            print(str(e))
        return cityAbbreviation


    def SetUpDataForTradeOffAnalytics(self, data):
        # data = open('FlightsAndHotelsData.json', 'r', encoding='utf-8')
        # print(data.read())
        data = json.loads(data)
        print(data)
        flightPriceData = data['FlightData']
        flightKeys = list(flightPriceData.keys())
        flightsData = {}
        for i in range(len(flightPriceData)):
            price = flightPriceData[flightKeys[i]][0]['Price']
            flightsData.update({flightKeys[i] : float(price)})

        hotelsPriceData = data['HotelsData']
        hotelsKeys = list(hotelsPriceData.keys())
        hotelsData = {}
        hotelsRankingData = []

        for j in range (len(hotelsKeys)):
            prices = hotelsPriceData[hotelsKeys[j]]['Price_Per_Day']
            rankingScore = hotelsPriceData[hotelsKeys[j]]['Hotel_Ranking']
            hotelsData.update({hotelsKeys[j]:[prices, rankingScore]})
            hotelsRankingData.append(rankingScore)

        routes = list(flightsData.keys())
        hotelsAndRankings = list(hotelsData.keys())

        dataForTradeOff = []
        index = 0
        for i in routes:
            for j in hotelsAndRankings:
                if (flightsData[i] == None or hotelsData[j][0] == None or hotelsData[j][1] == None or
                            flightsData[i] <= 0.0 or hotelsData[j][0]  <= 0.0 or hotelsData[j][1] <= 0.0 ): continue
                index += 1
                concatenatedKey = i + '-' + j
                concatenatedValue = {'flightPrice': flightsData[i], 'hotelPrice': hotelsData[j][0], 'hotelRanking': hotelsData[j][1]}
                dataForTradeOff.append({'key': str(index),'name': concatenatedKey ,'values':concatenatedValue})

        columnsInfo = [{'key':'flightPrice', 'type': 'numeric', 'goal':'min', 'is_objective': True, 'range':{'low':0,'high':2000}},
                       {'key':'hotelPrice', 'type': 'numeric', 'goal':'min', 'is_objective': True, 'range':{'low':0,'high':500}},
                       {'key':'hotelRanking', 'type': 'numeric', 'goal':'max', 'is_objective': False}]
        #

        completeData = {'columns': columnsInfo, 'options':dataForTradeOff}
        # completeData = json.dumps(completeData, ensure_ascii=False)

        # writeToFile = open('DataFile.json', 'w')
        dataToJson = json.dumps(completeData,ensure_ascii=False)
        return dataToJson


def Main():
    service = WebServices()
    origin ='BER'
    destination = 'PAR'
    departureDate = '2016-12-15'
    possibleFlights = 10
    numberOfDaysToVisit = 3
    hotelCheckInDate = datetime.strptime(departureDate,'%Y-%m-%d').date()
    hotelCheckInDate  = hotelCheckInDate + timedelta(days = 1) # Currently using logic of a 1 day ahead booking of hotel

    flightData = service.getFlightData(origin, destination,departureDate, possibleFlights)
    cityName = service.cityCodeToCityName(destination)
    hotelsData = service.getHotelData(cityName, hotelCheckInDate, numberOfDaysToVisit)
    mergeData = {'FlightData':flightData, 'HotelsData':hotelsData}
    writeToFile = open('FlightsAndHotelsData.json', 'w')
    json.dump(mergeData,writeToFile)

    dataToJson = json.dumps(mergeData, ensure_ascii=False)
    dataForTradeOff = service.SetUpDataForTradeOffAnalytics(dataToJson)

    watson = WatsonCloud()
    tradeOffResult = watson.getTradeOffAnalyticsResult(dataForTradeOff)
    return tradeOffResult

if __name__ == '__main__':
    Main()

