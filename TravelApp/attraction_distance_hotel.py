import requests
import json
def getDistanceMatrix(sourceLat,sourceLong,destinationLat,destinationLong,mode="driving"):
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metrix&mode="+mode+"&origins="+str(sourceLat)+","+ str(sourceLong) +"&destinations="+str(destinationLat)+","+str(destinationLong)+"&key=AIzaSyBvlM7o47CNPvDdlWi6xPe_KGsPtmoNWLc"
	r = requests.get(url)
	data = json.loads(r.text)
	print(data)
getDistanceMatrix(40.6655101,-73.89188969999998,48.6655101,-73.89188969999998,"walking")