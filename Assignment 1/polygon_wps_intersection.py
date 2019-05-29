# ---------------------
# Polygon intersection function using WPS specification
# ---------------------
from osgeo import ogr
from osgeo import osr

def title():
    return "Polygon Intersection" # title of the function

def abstract():
    return "A function that compute the intersection of two polygons." # short description of the function

def inputs():
    return [
        ['polygonx', 'Input polygon x','The first polygon input(JSON format) for intersection.','application/json', True],
        ['polygony', 'Input polygon y', 'The second polygon input(JSON format) for intersection.', 'application/json', True]
    ]

def outputs():
    return [['result', 'Intersection feature','The intersection of polygon x and y','application/json']]

def execute(parameters):
    feature_x = parameters.get('polygonx')
    feature_y = parameters.get('polygony')
    if (feature_x is not None) and (feature_y is not None):
        feature_x = feature_x['value']
        feature_y = feature_y['value']

    inputfeature1 = ogr.CreateGeometryFromJson(feature_x)
    inputfeature2 = ogr.CreateGeometryFromJson(feature_y)
    # print(inputfeature1)
    intersection = inputfeature1.Intersection(inputfeature2)
    print("Content-type: application/json")
    print()
    print(intersection.ExportToJson())