# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries
# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from api import app_api # Blueprint import api definition
from bp_projects.projects import app_projects # Blueprint directory import projects definition
from flask import jsonify # used for weather data
import requests
from datetime import datetime

app.register_blueprint(app_api) # register api routes
app.register_blueprint(app_projects) # register api routes
now = datetime.now()
time = now.hour
print(int(time))

def timeRefresh(currentTime):
    lastUpdateTime=1
    if (int(currentTime)-lastUpdateTime) >= 1:
        time = now.hour
        lastUpdateTime = time
        return True
    return False

def makeSummary():
    url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
    querystring = {"aggregateHours":"24","location":"Washington,DC,USA","contentType":"json","unitGroup":"us","shortColumnNames":"0"}
    headers = {
	    "X-RapidAPI-Key": "c87ee363dfmsh4fb6fcceafe4c22p1bcd5bjsnbc99e32cc17c",
	    "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    Data=response.json()
    return Data

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

@app.route('/weatherData/')  # allows access to weather data 
def weatherData():
    time = now.hour
    if timeRefresh(time):
        weatherData = makeSummary()
        print("[i] requested")
    return weatherData

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
