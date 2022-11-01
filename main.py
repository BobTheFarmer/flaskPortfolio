# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries
# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from api import app_api # Blueprint import api definition
from bp_projects.projects import app_projects # Blueprint directory import projects definition
from flask import jsonify # used for weather data
import requests

app.register_blueprint(app_api) # register api routes
app.register_blueprint(app_projects) # register api routes

def makeSummary():
    url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
    querystring = {"aggregateHours":"24","location":"Washington,DC,USA","contentType":"json","unitGroup":"us","shortColumnNames":"0"}
    headers = {
    	"X-RapidAPI-Key": "eb0bbc6cc0msh085b254f1761bc2p154cf4jsne59a8dbdbaa0",
	    "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    weatherData=response.text
    return weatherData

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
    weatherData = makeSummary()
    return jsonify(weatherData)

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
