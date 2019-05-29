import os
import requests
import sys
import json
import xml.etree.ElementTree as xml
import urllib
from importlib.machinery import SourceFileLoader
import glob


def cgierror(message):
    print("Content-type: text/html")
    print()
    print(message)

def nonamespace(tag):
    i = tag.find('}')
    if i >= 0:
        tag = tag[i+1:]
    return tag

def printGetCapabilities():
    print("Content-type: text/xml")
    print()
    print('<?xml version="1.0" encoding="utf-8"?> \
           <wps:Capabilities service="WPS" version="1.0.0" xml:lang="en" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:wps="http://www.opengis.net/wps/1.0.0" \
           xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 \
           http://schemas.opengis.net/wps/1.0.0/wpsGetCapabilities_response.xsd" updateSequence="1">')
    print('<wps:ProcessOfferings>')
    curpath = os.path.dirname(os.path.realpath( __file__ ))
    curfile = os.path.realpath( __file__ )
    curfile = curfile[1+len(curpath):-3]
    for identifier in glob.glob(curpath + '/*_wps_*.py'):
        identifier = identifier[1+len(curpath):-3]
        if identifier == curfile:
            continue # skip ourselves
        processor = SourceFileLoader(identifier, curpath + '/' + identifier + '.py').load_module()
        funcs = dir(processor)
        if not 'title' in funcs or not 'abstract' in funcs:
            continue
        implemented = 'true' if 'process' in funcs else 'false'
        print('<wps:Process wps:processVersion="1.1">')
        print('<ows:Identifier>' + identifier + '</ows:Identifier>')
        print('<ows:Title>' + processor.title() + '</ows:Title>')
        print('<ows:Abstract>' + processor.abstract() + '</ows:Abstract>')
        print('</wps:Process>')
    print('</wps:ProcessOfferings>')
    print('</wps:Capabilities>')
    sys.stdout.flush()

def printDescribeProcess(identifier):
    curpath = os.path.dirname(os.path.realpath(__file__))
    if identifier is None:
        cgierror("DescribeProcess: bad identifier: None")
    elif not os.path.exists(curpath + "\\" + identifier + ".py"):
        cgierror("DescribeProcess: identifier does not exist: '" + identifier + "'")
    else:
        processor = SourceFileLoader(identifier, curpath + "\\" +identifier + ".py").load_module()
        print("Content-type: text/xml")
        print()
        print('<?xml version="1.0" encoding="utf-8"?> \
               <wps:ProcessDescriptions xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:xlink="http://www.w3.org/1999/xlink" \
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 \
               http://schemas.opengis.net/wps/1.0.0/wpsDescribeProcess_response.xsd" service="WPS" version="1.0.0" xml:lang="en-CA"> \
               <ProcessDescription wps:processVersion="1.1" storeSupported="true" statusSupported="true">')
        print('<ows:Identifier>'+identifier+'</ows:Identifier>')
        funcs = dir(processor)
        if 'title' in funcs:
            print('<ows:Title>'+processor.title()+'</ows:Title>')
        else:
            print('<ows:Title></ows:Title>')
        if 'abstract' in funcs:
            print('<ows:Abstract>'+processor.abstract()+'</ows:Abstract>')
        else:
            print('<ows:Abstract></ows:Abstract>')
        print('<DataInputs>')
        if 'inputs' in funcs:
            for inparameter in processor.inputs():
                if inparameter[4] == True:
                    print('<Input minOccurs="1" maxOccurs="1">')
                else:
                    print('<Input minOccurs="0" maxOccurs="1">')
                print('<ows:Identifier>' + inparameter[0] + '</ows:Identifier>')
                print('<ows:Title>' + inparameter[1] + '</ows:Title>')
                print('<ows:Abstract>' + inparameter[2] + '</ows:Abstract>')
                if "image/tif" in inparameter[3] or "application/json" in inparameter[3]:
                    print('<ComplexData><Default><Format><MimeType>' + inparameter[3] + '</MimeType></Format></Default></ComplexData>')
                else:
                    print('<LiteralData><ows:DataType>' + inparameter[3] + '</ows:DataType></LiteralData>')
                print('</Input>')
        print('</DataInputs>')
        print('<ProcessOutputs>')
        if 'outputs' in funcs:
            for outparameter in processor.outputs():
                print('<Output>')
                print('<ows:Identifier>' + outparameter[0] + '</ows:Identifier>')
                print('<ows:Title>' + outparameter[1] + '</ows:Title>')
                print('<ows:Abstract>' + outparameter[2] + '</ows:Abstract>')
                if "image/tif" in outparameter[3] or "application/json" in outparameter[3]:
                    print('<ComplexOutput><Default><Format><MimeType>' + outparameter[3] + '</MimeType></Format></Default></ComplexOutput>')
                else:
                    print('<LiteralOutput><ows:DataType>' + outparameter[3] + '</ows:DataType></LiteralOutput>')
                print('</Output>')
        print('</ProcessOutputs>')
        print('</ProcessDescription> \
               </wps:ProcessDescriptions>')
        sys.stdout.flush()

def printExecute(identifier, parameters):
    curpath = os.path.dirname(os.path.realpath(__file__))
    if identifier is None:
        cgierror("Execute: bad identifier: None")
    elif not os.path.exists(curpath + "\\" + identifier + ".py"):
        cgierror("Execute: identifier does not exist: '" + identifier + "'")
    else:
        processor = SourceFileLoader(identifier, curpath + "\\" +identifier + ".py").load_module()
        funcs = dir(processor)
        if not 'execute' in funcs:
            cgierror("Execute: function '" + identifier + "' not implemented.")
        else:
            processor.execute(parameters)
            sys.stdout.flush()

# main()

# GET/POST
querystring = os.environ.get('QUERY_STRING')
#querystring = "https://gisedu.itc.utwente.nl/student/s1906240/wps/wps.py?service=WPS&request=GetCapabilities"
querystring = querystring.split('&')
query = {}
for qs in querystring:
    qs = qs.split('=')
    if len(qs) > 1:
        query[qs[0].lower()] = qs[1]

request = query.get('request')

identifier = ''
parameters = {}
operation = {}
if request is None: # POST
    contentlength = os.environ.get('CONTENT_LENGTH', 0)
    contentlength = int(contentlength)
    if contentlength > 0:
        root = sys.stdin.read(contentlength)
        root = xml.fromstring(root)
        request = nonamespace(root.tag)
        if request != 'GetCapabilities':
            identifier = root.find('{http://www.opengis.net/ows/1.1}Identifier').text
            operation["metadata"] = {
                "longname" : identifier
            }
            if request == 'Execute':
                wpsInputs = []
                inputs = root.findall('{http://www.opengis.net/wps/1.0.0}DataInputs/{http://www.opengis.net/wps/1.0.0}Input')
                for input in inputs:
                    id = input.find('{http://www.opengis.net/ows/1.1}Identifier').text
                    wpsInput = {}
                    wpsInput["identifier"] = id
                    parameter = {}
                    parameter['title'] = input.find('{http://www.opengis.net/ows/1.1}Identifier').text
                    wpsInput["name"] = input.find('{http://www.opengis.net/ows/1.1}Identifier').text
                    if input.find('{http://www.opengis.net/wps/1.0.0}Data/{http://www.opengis.net/wps/1.0.0}LiteralData') != None:
                        parameter['value'] = input[1][0].text
                        wpsInput["value"] = input[1][0].text
                    elif input.find('{http://www.opengis.net/wps/1.0.0}Data/{http://www.opengis.net/wps/1.0.0}ComplexData') != None:
                        parameter['value'] = input[1][0].text
                        wpsInput["value"] = input[1][0].text
                    else:
                        parameter['value'] = input.find('{http://www.opengis.net/wps/1.0.0}Reference').attrib['{http://www.w3.org/1999/xlink}href']
                        wpsInput["value"] = input.find('{http://www.opengis.net/wps/1.0.0}Reference').attrib['{http://www.w3.org/1999/xlink}href']
                    parameters[id] = parameter
                    wpsInputs.append(wpsInput)
                operation["inputs"] = wpsInputs
else: # GET
    if request != 'GetCapabilities':
        identifier = query.get('identifier')
        if request == 'Execute':
            inputs = query.get('datainputs')
            if not inputs is None:
                inputs = urllib.parse.unquote(inputs)
                inputs = inputs.split('&')
                for input in inputs:
                    input = input.split('=')
                    parameter = {}
                    id = input[0]
                    parameter['value'] = input[1]
                    parameters[id] = parameter
            else:
                 cgierror("No inputs")

if not request is None:
    if request.lower() == 'getcapabilities':
        printGetCapabilities()
    elif request.lower() == 'describeprocess':
        printDescribeProcess(identifier)
    elif request.lower() == 'execute':
        printExecute(identifier, parameters)
    else:
        cgierror("Bad request: '" + request + "'")
else:
    printGetCapabilities()
