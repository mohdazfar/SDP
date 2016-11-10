import requests
import json

def getVaccination(city):
	countryUrl = "http://maps.googleapis.com/maps/api/geocode/json?address="
	vaccineUrl = 'https://api.tugo.com/v1/travelsafe/countries/'
	headers = {'X-Auth-Api-Key': 'ky36nz872hpbggma7jc8624u'}
	mycity = city
	if mycity =="":
		return {"Error":"City can not be empty"}

	try:
		countryUrl = countryUrl + mycity
		# print("Url: {}".format(countryUrl))
		r = requests.get(countryUrl)
		resultset = json.loads(r.text)
		results = resultset["results"][0]["address_components"]
		for i in range(len(results)):
			typeList = results[i].get("types")
		if "country" in typeList:
			longName = results[i].get("long_name")
			shortName = results[i].get("short_name")
			# print("Long Name: {} Short Name: {}".format(longName,shortName))
	except:
		return {"Error":"Invalid city name"}

	try:
		vaccineUrl = vaccineUrl + shortName
		r = requests.get(vaccineUrl, headers = headers)
		data = json.loads(r.text)
		#print(data)
		dic = {'Vaccinations':data['health']['diseasesAndVaccinesInfo']['Vaccines']}


		return dic

	except:
		return {"Error":"Vaccination data can not be retrieved"}



# data=getVaccination('Jyvaskyla')
# print(data)