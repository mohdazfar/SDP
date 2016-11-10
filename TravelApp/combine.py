#from flight import *
#from hotel import *
#from trade_off import *
#from package import *
#from Vaccination import *
#from Attraction import *
def combine(flightList,myDestVenues):
    trade_f = []
    for i in range(len(flightList)):
        package={}
        result={}
        flight = flightList[i]['flight' + str(i + 1)]
        price = flight['price']['Price']

        durations = flight['flight_info']
        durationList = []
        for duration in durations:
            durationList.append(duration['duration'])

        time = 0
        for j in range(len(durationList)):
            time += durationList[j]

        transfers = flight['flight_info']
        trans_c = 0
        for transfer in transfers:
            trans_c += len(transfer['info']) - 1

        package['flight_price']=float(price)
        package['duration']=time
        package['transfer_count'] = trans_c
        result['flight'+str(i+1)]=package
        trade_f.append(result)
    print(trade_f)

    trade_h = []
    for venue in myDestVenues:
        hotel={}
        hotel['hotel' + str(venue["id"])] = {"ranking": venue["ranking"], "room_price": venue["room_price"]}
        trade_h.append(hotel)
    print(trade_h)

    options=[]
    count=1
    for i in range(len(trade_f)):
        for j in range(len(trade_h)):
            input={}
            input['key']=count
            input['name']='flight'+str(i+1)+','+'hotel'+str(j+1)
            x=trade_f[i]['flight'+str(i+1)]
            y=trade_h[j]['hotel'+str(j+1)]
            z = x.copy()
            z.update(y)
            input['values']=z
            options.append(input)
            count=count+1
    return options

# attraction = getAttractions('paris', ["gym", "shop", "bar"])
# vaccination = getVaccination('paris')
# av = attraction.copy()
# av.update(vaccination)
#
# data_f=getFlightData('Helsinki','Paris','2016-11-09','2016-11-11')
# data_h=getHotelsForDestinationCity('paris', "2016-11-11", "2016-11-13")
#
# options=combine(data_f,data_h)
# dic=trade_off(options)
# front=analysis(dic)
#
# package(options,front,data_f,data_h,av)
# print(front)




