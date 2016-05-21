#Pre-Reqs:
#Jython 2.7
#	pip install flask
#	pip install Flask-JSON
#
from __future__ import print_function
import json

from flask import Flask, Response, request
import sys

app = Flask(__name__)
app.debug = True

import time
import math

now=int(time.mktime(time.localtime()))
hourago = now*1000 - 7200*1000

upper_25_datapoints = "["
upper_50_datapoints = "["
upper_75_datapoints = "["
upper_90_datapoints = "["
upper_95_datapoints = "["

i = 1
while i < 3600:
    sinwave = int(math.sin(math.radians(i/10))* 1000)
    coswave = int(math.cos(math.radians(i/10))* 1000)
    hourago = hourago + 1000
    upper_25_datapoints = upper_25_datapoints + "[" + str(sinwave) + ", " + str(hourago) + "]"
    upper_50_datapoints = upper_50_datapoints + "[" + str(sinwave*2) + ", " + str(hourago) + "]"
    upper_75_datapoints = upper_75_datapoints + "[" + str(sinwave/4) + ", " + str(hourago) + "]"
    upper_90_datapoints = upper_90_datapoints + "[" + str(coswave) + ", " + str(hourago) + "]"
    upper_95_datapoints = upper_95_datapoints + "[" + str(coswave/2) + ", " + str(hourago) + "]"
    if i<3599:
        upper_25_datapoints = upper_25_datapoints + ","
        upper_50_datapoints = upper_50_datapoints + ","
        upper_75_datapoints = upper_75_datapoints + ","
        upper_90_datapoints = upper_90_datapoints + ","
        upper_95_datapoints = upper_95_datapoints + ","
    else:
        upper_25_datapoints = upper_25_datapoints + "]"
        upper_50_datapoints = upper_50_datapoints + "]"
        upper_75_datapoints = upper_75_datapoints + "]"
        upper_90_datapoints = upper_90_datapoints + "]"
        upper_95_datapoints = upper_95_datapoints + "]"
        
    i = i + 1


timeseries = [
  {"target": "upper_25", "datapoints": upper_25_datapoints },
  {"target": "upper_50", "datapoints": upper_50_datapoints },
  {"target": "upper_75", "datapoints": upper_75_datapoints },
  {"target": "upper_90", "datapoints": upper_90_datapoints },
  {"target": "upper_95", "datapoints": upper_95_datapoints }
]
    
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
  return response

# Show unique metric options on query tab in panels
#,provide_automatic_options=['False']
@app.route("/search", methods=['POST','GET'])
def search():
    return_json = []

    print(request.get_json(),file=sys.stderr)
    
    for item in timeseries:
        return_json.append(item["target"])

    print(json.dumps(return_json),file=sys.stderr)
    myResponse = Response(response=json.dumps(return_json),status=200, headers={'Content-Type': 'application/json'})
    return(myResponse)
    
@app.route("/query", methods=['POST','GET'])
def query():
    print(request.get_json(),file=sys.stderr)
    json_string = """[
  {"target": "upper_25", "datapoints": """ + upper_25_datapoints + """ },
  {"target": "upper_50", "datapoints": """ + upper_50_datapoints + """ },
  {"target": "upper_75", "datapoints": """ + upper_75_datapoints + """ },
  {"target": "upper_90", "datapoints": """ + upper_90_datapoints + """ },
  {"target": "upper_95", "datapoints": """ + upper_95_datapoints + """}
]
"""

#    json.dumps(json_obj)
    myResponse = Response(response=json_string,status=200, headers={'Content-Type': 'application/json'})
    return(myResponse)
    
    
#Grafana expects following format for annotations
#[
#  {
#    annotation: annotation, // The original annotation sent from Grafana.
#    time: time, // Time since UNIX Epoch in milliseconds. (required)
#    title: title, // The title for the annotation tooltip. (required)
#    tags: tags, // Tags for the annotation. (optional)
#    text: text // Text for the annotation. (optional)
#  }
#]	
@app.route("/annotation", methods=['POST'])
def annotation():
    data = request.get_json()
    return "blah"

@app.route("/", methods=['GET'])
def hello():
    json_string = """
    {
    "status":"success",
    "message":"Data source is working",
    "title":"Success"
    }
"""
#, 'Access-Control-Allow-Origin': '*'
    myResponse = Response(response=json_string,status=200, headers={'Content-Type': 'application/json'})
    return(myResponse)
     
if __name__ == "__main__":
    app.run()
