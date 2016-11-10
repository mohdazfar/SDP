import requests
import json

def whatsApp():
    return "what's up Yo"

def getAttractions(city, attractions):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    API_KEY = "AIzaSyDJf6XiNsSQzWe-QXY_gT1yfa01W5PryZs"
    attractionList = attractions
    myCity = city
    queryStr = ""
    if myCity == "" or len(attractionList) == 0:
        return {"Error": "Incomplet argument parameters"}
    try:
        # building multiple attraction names with connective word 'OR'
        queryStr = attractionList[0]
        for i in range(1, len(attractionList)):
            queryStr += " OR " + attractionList[i]

        # attractions only for a single city
        queryStr += " in " + myCity
    except:
        return {"Error": "Invalid arguments in the parameter"}

    url = url + queryStr + "&key=" + API_KEY
    # print("Url: {}".format(url))
    r = requests.get(url)
    resultset = json.loads(r.text)
    results = resultset["results"]
    resultFields = ['index', 'formatted_address', 'name', 'rating', 'types']
    # fields to be filtered from the reslut set
    resultDict = {}
    tempList = []
    count = len(results)
    resultDict["count"] = count
    for i in range(count):
        tempDict = {}
        tempDict[resultFields[0]] = i
        tempDict[resultFields[1]] = results[i].get(resultFields[1])
        tempDict[resultFields[2]] = results[i].get(resultFields[2])
        tempDict[resultFields[3]] = results[i].get(resultFields[3])
        tempDict[resultFields[4]] = results[i].get(resultFields[4])
        tempList.append(tempDict.copy())
    result_List= tempList
    dic={}
    dic['Attractions']=result_List


    return dic



# testDict = getAttractions("Turku", ["gym", "shop", "bar"])
# print(testDict)