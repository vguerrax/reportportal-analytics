#!/usr/local/bin/python3

import requests
from utils import getHeaders

typeRefs = ('TO_INVESTIGATE', 'NO_DEFECT', 'AUTOMATION_BUG', 'PRODUCT_BUG', 'SYSTEM_ISSUE')

def get_subtypes(params={}):
    global typeRefs

    project_name = params['project']
    reportportal_url = params['url']

    headers = getHeaders(params['apiToken'])
    base_url = reportportal_url + '/api/v1/project/' + project_name

    response = requests.get(base_url, headers=headers,
                            params=params['queryParams'])

    results = response.json()['configuration']['subTypes']
    subtypes = []

    for typeRef in typeRefs:
        subTypesAux = results[typeRef]
        for subtype in subTypesAux:
            subtypes.append({'locator': subtype['locator'], 'description': subtype['longName'], 'color': subtype['color']})
    return subtypes