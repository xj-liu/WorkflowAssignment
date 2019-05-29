# WPS Execute Operation

import requests, os, json

payload = open(os.path.dirname(os.path.abspath(__file__)) +"\\polygon_intersection.xml").read()

wpsServerUrl = "https://gisedu.itc.utwente.nl/student/s6039782/gpw/wps.py?"

response = requests.post(wpsServerUrl, data=payload)
print("Content-type: application/json")
print()
print(response.text)