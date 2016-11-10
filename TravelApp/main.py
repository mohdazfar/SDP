import flask
import requests
from flask import Flask, flash, redirect, render_template, request, session, abort
import json
from Vaccination import *
from Attraction import *
from flight import *
from hotel import *
from trade_off import *
from package import *
from combine import *

app = Flask(__name__)
@app.errorhandler(404)
def custom404(error):
	response = flask.jsonify({'message':error.description})
	response.status_code = 404
	response.status = 'error:Resource not found'
	return response
@app.errorhandler(400)
def custom400(error):
	response = flask.jsonify({'message':error.description})
	response.status_code = 400
	response.status = 'error:Bad Request'
	return response

@app.route('/')
def greetThem():
    return "Hi guys"

@app.route('/sdp',methods=['GET'])
def package():
    try:
        originplace= request.args.get('originplace')
        destinationplace = request.args.get('destinationplace')
        outbounddate= request.args.get('outbounddate')#mm/dd/yyyy format
        inbounddate = request.args.get('inbounddate')#mm/dd/yyyy format
        attractionStr=request.args.get('attractions')
        tfDuration=request.args.get('tfd')
        tfPrice = request.args.get('tfp')
        tfTransfer = request.args.get('tft')
        thRanking = request.args.get('thr')
        thPrice = request.args.get('thp')

        originplace = cityEncoder(originplace)
        destinationplace = cityEncoder(destinationplace)
    except:
        flask.abort(400, "Invalid arguments in the parameter")

    print(originplace)
    print(destinationplace)
    print(outbounddate)
    print(inbounddate)

    try:
        attractionList=attractionStr.split(',')
        attraction=getAttractions(destinationplace,attractionList)
        vaccination=getVaccination(destinationplace)
        av = attraction.copy()
        av.update(vaccination)

        data_f=getFlightData(originplace, destinationplace, outbounddate, inbounddate)
        # data_f = getFlightData('Helsinki', 'Paris', '2016-11-08', '2016-11-9')
        data_h = getHotelsForDestinationCity(destinationplace, outbounddate, inbounddate)

        options = combine(data_f, data_h)
        dic = trade_off(options,tfPrice,tfDuration,tfTransfer,thPrice,thRanking)
        print(dic)
        front = analysis(dic)
        results=packages(options,front,data_f,data_h,av)
        print(results)
        response={'results':results}

        return flask.jsonify(response)
    except:
        flask.abort(400, "Sorry, an error has occured. ")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)