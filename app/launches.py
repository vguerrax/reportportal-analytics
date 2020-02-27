#!/usr/local/bin/python3

import requests
from utils import getHeaders

def get_launches(params={}):
    project_name = params['project']
    reportportal_url = params['url']

    headers = getHeaders(params['apiToken'])
    base_url = reportportal_url + '/api/v1/' + project_name + '/launch'

    response = requests.get(base_url, headers=headers,
                            params=params['queryParams'])

    results = response.json()['content']
    totalPages = response.json()['page']['totalPages']

    if int(totalPages) > 1:
        for page in range(2, int(totalPages)+1):
            params['queryParams']['page.page'] = str(page)
            response = requests.get(
                base_url, headers=headers, params=params['queryParams'])
            results.extend(response.json()['content'])
    return results

def get_launches_analytics(params={}):
    results = get_launches(params)
    launches = []
    for result in results:
        launch = {}
        launch['name'] = result['name']
        launch['number'] = result['number']
        launch['statistics'] = result['statistics']['executions']
        defectsTypes = result['statistics']['defects']
        defects = {}
        for defectType in defectsTypes:
            jsonKeys = list(result['statistics']['defects'][defectType])
            for key in jsonKeys:
                if key != 'total':
                    defects[key] = result['statistics']['defects'][defectType][key]
        launch['defects'] = defects
        launches.append(launch)
    return {'launches': launches, 'total_launches': len(launches)}

def get_launches_analytics_consolidated(params={}):
    results = get_launches_analytics(params)
    totalCTExec = 0
    totalCTPass = 0
    totalCTFail = 0
    totalCTSkip = 0
    totalDefects = {}
    for result in results['launches']:
        totalCTExec += int(result['statistics']['total'])
        totalCTPass += int(result['statistics']['passed'])
        totalCTFail += int(result['statistics']['failed'])
        totalCTSkip += int(result['statistics']['skipped'])

        defectKeys = list(result['defects'])
        
        for key in defectKeys:
            if key in totalDefects.keys():
                totalDefects[key] += int(result['defects'][key])
            else:
                totalDefects[key] = int(result['defects'][key])

    r = {'total_executed_cts': totalCTExec,
         'total_passed_cts': totalCTPass,
         'total_failed_cts': totalCTFail,
         'total_skipped_cts': totalCTSkip,
         'defects': totalDefects
        }
    if 'startTime' in list(params):
        r['startTime'] = params['startTime']
    if 'endTime' in list(params):
        r['endTime'] = params['endTime']
    return r

def get_launches_analytics_consolidated_xml(params={}):
    results = get_launches_analytics_consolidated(params)

    totalCTExec = int(results['total_executed_cts'])
    totalCTPass = int(results['total_passed_cts'])
    totalCTFail = int(results['total_failed_cts'])
    totalCTSkip = totalCTExec - (totalCTPass + totalCTFail)

    if totalCTExec == 0:
        return None

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'

    xml += '<testsuite name="Casos de Teste Executados'
    if 'startTime' in list(params):
        xml += ' entre ' + params['startTime']
    if 'endTime' in list(params):
        xml += ' e ' + params['endTime']

    xml += '" tests="' + str(totalCTExec) + '"'

    if totalCTFail > 0:
        xml += ' failures="' + str(totalCTFail) + '"'
    if totalCTSkip > 0:
        xml += ' skipped="' + str(totalCTSkip) + '"'
    xml += '>\n'

    for i in range(0, totalCTPass):
        xml += '\t<testcase name="Pass ' + str(i) + '"/>\n'

    for i in range(0, totalCTFail):
        xml += '\t<testcase name="Fail ' + str(i) + '"><failure message="Fail"></failure></testcase>\n'

    for i in range(0, totalCTSkip):
        xml += '\t<testcase name="Skip ' + str(i) + '"><skipped/></testcase>\n'
    
    xml += '</testsuite>'

    return xml
