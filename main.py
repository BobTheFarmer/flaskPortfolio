# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries
# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from api import app_api # Blueprint import api definition
from bp_projects.projects import app_projects # Blueprint directory import projects definition
from flask import jsonify # used for weather data
import requests
import time

app.register_blueprint(app_api) # register api routes
app.register_blueprint(app_projects) # register api routes

def timeRefresh():
    global last_run  # the last_run global is preserved between calls to function
    try: last_run
    except: last_run = None
    
    # initialize last_run data
    if last_run is None:
        last_run = time.time()
        return True
    
    # calculate time since last update
    elapsed = time.time() - last_run
    if elapsed > 86400:  # update every 24 hours
        last_run = time.time()
        return True
    
    return False


def makeSummary(location):
    global sanDiegoDataSave
    try: sanDiegoDataSave
    except: sanDiegoDataSave = None

    global washingtonDCDataSave
    try: washingtonDCDataSave
    except: washingtonDCDataSave = None

    global newYorkDataSave
    try: newYorkDataSave
    except: newYorkDataSave = None

    global singaporeDataSave
    try: singaporeDataSave
    except: singaporeDataSave = None

    if timeRefresh():
        url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
        headers = {
	        "X-RapidAPI-Key": "c87ee363dfmsh4fb6fcceafe4c22p1bcd5bjsnbc99e32cc17c",
	        "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
        }
        querystring = {"aggregateHours":"24","location":"San,Diego,USA","contentType":"json","unitGroup":"us","shortColumnNames":"0"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        sanDiegoData=response.json()
        sanDiegoDataSave = sanDiegoData

        querystring = {"aggregateHours":"24","location":"Washington,DC,USA","contentType":"json","unitGroup":"us","shortColumnNames":"0"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        washingtonDCData=response.json()
        washingtonDCDataSave = washingtonDCData

        querystring = {"aggregateHours":"24","location":"New,York,New,York,USA","contentType":"json","unitGroup":"us","shortColumnNames":"0"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        newYorkData=response.json()
        newYorkDataSave = newYorkData

        querystring = {"aggregateHours":"24","location":"Singapore,Singapore","contentType":"json","unitGroup":"us","shortColumnNames":"0"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        singaporeData=response.json()
        singaporeDataSave = singaporeData
        print("[i] requested")
    else:
        sanDiegoData = sanDiegoDataSave
        washingtonDCData = washingtonDCDataSave
        newYorkData = newYorkDataSave
        singaporeData = singaporeDataSave
        if location == "San,Diego,USA":
            return sanDiegoData
        elif location == "Washington,DC,USA":
            return washingtonDCData
        elif location == "New,York,New,York,USA":
            return newYorkData
        elif location == "Singapore,Singapore":
            return singaporeData

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/stub/')  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")

@app.route('/functionAndPurpose/')  # connects /functionAndPurpose/ URL to functionAndPurpose() function
def functionAndPurpose():
    return render_template("functionAndPurpose.html")

@app.route('/weatherDataSD/')  # allows access to weather data 
def weatherDataSD():
    weatherDataSD = makeSummary("San,Diego,USA")
    return weatherDataSD
    
@app.route('/weatherDataDC/')  # allows access to weather data 
def weatherDataDC():
    weatherDataDC = makeSummary("Washington,DC,USA")
    return weatherDataDC
    
@app.route('/weatherDataNY/')  # allows access to weather data 
def weatherDataNY():
    weatherDataNY = makeSummary("New,York,New,York,USA")
    return weatherDataNY
    
@app.route('/weatherDataSG/')  # allows access to weather data 
def weatherDataSG():
    weatherDataSG = makeSummary("Singapore,Singapore")
    return weatherDataSG

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
