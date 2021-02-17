import requests


def deleteFromServer():
    URL = "http://127.0.0.1:3030/kbe/update"

    PARAMS = {'update':
                'PREFIX kbe:<http://www.my-kbe.com/shapes.owl#> '
                'DELETE {'
                '   ?block kbe:hasLength ?length. '
                '   ?block kbe:hasWidth ?width. '
                '   ?block kbe:hasHeight ?height. '
                '} '
                'WHERE {'
                '   ?block kbe:hasLength ?length. '
                '   ?block kbe:hasWidth ?width. '
                '   ?block kbe:hasHeight ?height. '
                '}'
    }

    # sending get request and saving the response as response object
    r = requests.post(url=URL, data=PARAMS)
    # Checking the result
    print("Result for DELETE query:", r.text)


def updateServer(topL, topW, topH, legL, legW, legH):
    URL = "http://127.0.0.1:3030/kbe/update"

    legPARAMS = {'update':
                    'PREFIX kbe:<http://www.my-kbe.com/shapes.owl#> '
                    'PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>'
                    'INSERT { '
                    '   kbe:leg kbe:hasLength "' + str(legL) + '"^^xsd:int. '
                    '   kbe:leg kbe:hasWidth "' + str(legW) + '"^^xsd:int. '
                    '   kbe:leg kbe:hasHeight "' + str(legH) + '"^^xsd:int. '
                    '} '
                    'WHERE {kbe:leg ?pred ?obj}'
    }

    topPARAMS = {'update':
                    'PREFIX kbe:<http://www.my-kbe.com/shapes.owl#> '
                    'PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>'
                    'INSERT { '
                    '   kbe:topPlate kbe:hasLength "' + str(topL) + '"^^xsd:int. '
                    '   kbe:topPlate kbe:hasWidth "' + str(topW) + '"^^xsd:int. '
                    '   kbe:topPlate kbe:hasHeight "' + str(topH) + '"^^xsd:int. '
                    '} '
                    'WHERE {kbe:topPlate ?pred ?obj}'
    }

    # sending post request and saving the response
    r = requests.post(url=URL, data=legPARAMS)
    # Checking the result
    print("Result for INSERT leg query:", r.text)
    # sending post request and saving the response
    r = requests.post(url=URL, data=topPARAMS)
    # Checking the result
    print("Result for INSERT topPlate query:", r.text)


def getFromServer():
    URL = "http://127.0.0.1:3030/kbe"

    # defining a query params
    PARAMS = {'query':
                'PREFIX kbe:<http://www.my-kbe.com/shapes.owl#> '
                'SELECT ?length ?width ?height '
                'WHERE {'
                '   ?block a kbe:Block.?block kbe:hasLength ?length. '
                '   ?block a kbe:Block.?block kbe:hasWidth ?width. '
                '   ?block a kbe:Block.?block kbe:hasHeight ?height.'
                '}'
    }

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # Checking the result
    # print("Result:", r.text)
    data = r.json()
    # print("JSON:", data)

    # Checking the value of the parameter
    legL = data['results']['bindings'][0]['length']['value']
    legW = data['results']['bindings'][0]['width']['value']
    legH = data['results']['bindings'][0]['height']['value']
    topL = data['results']['bindings'][1]['length']['value']
    topW = data['results']['bindings'][1]['width']['value']
    topH = data['results']['bindings'][1]['height']['value']

    return topL, topW, topH, legL, legW, legH
