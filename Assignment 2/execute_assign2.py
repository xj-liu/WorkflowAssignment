# WPS Execute Operation
import requests, json, os

buur_params = {
    'request':'GetFeature','service':'WFS',
    'version':'2.0.0',
    'typeNames':'neighbourhood',
    'outputFormat':'geojson',
    'srsname':'EPSG:3857'    
}
# Get Eindhoven boundaries (FeatureCollection)
buur = requests.get("https://gisedu.itc.utwente.nl/cgi-bin/mapserv.exe?map=d:/iishome/exercise/data/afrialiance/layers.map&", 
                    params=buur_params).json()
buur_feas = buur["features"]
buname = [fea["properties"]["bu_name"] for fea in buur_feas]
for i, n in enumerate(buname):
    buname[i] = n.replace(" ","%20")
# buname = "Boddenkamp"

for n in buname[0:3]:
    payload = open(os.path.dirname(os.path.abspath(__file__)) +"\\assignment2.xml").read()
    payload = payload.format(n)
    wpsServerUrl = "http://130.89.221.193:85/geoserver/ows?"
    response = requests.post(wpsServerUrl, data=payload)
    # print("Content-type: application/json")
    print()
    print(n, response.text)