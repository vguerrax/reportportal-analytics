#!/usr/local/bin/python3

import sys
import optparse
import datetime
import xml.etree.ElementTree as ET

from flask import Flask, Response
from flask_restful import Resource, Api, reqparse

import launches
import subtypes
import utils

app = Flask(__name__)
api = Api(app)

_reqparse = reqparse.RequestParser(bundle_errors=True)
_reqparse.add_argument('apiToken', type=str, location='args', required=True, trim=True, help='{error_msg}, pass the api token.')
_reqparse.add_argument('project', type=str, location='args', required=True, trim=True, help='{error_msg}, pass the project name')
_reqparse.add_argument('url', type=str, location='args', required=True, trim=True, help='{error_msg}, pass the URL of the application.')
_reqparse.add_argument('startTime', type=str, location='args', trim=True, help='Data e hora do inicio das execuções, formato DD/MM/YYYY HH:MM:SS')
_reqparse.add_argument('endTime', type=str, location='args', trim=True, help='Data e hora do fim das execuções, formato DD/MM/YYYY HH:MM:SS')

def mountArgs(args):
    params = {}
    params['apiToken'] = args['apiToken']
    params['project'] = args['project']
    params['url'] = args['url']
    queryParams = {'page.size':'100', 'page.page': '1', 'page.sort':'start_time,number,DESC', 'filter.cnt.name':'TestRun'}
    startTime = args['startTime']
    endTime = args['endTime']

    if startTime != None:
        if utils.validateDateTime(startTime):
            params['startTime'] = str(startTime)
            startTime = utils.convertDateTimeToTimestamp(startTime)
            queryParams['filter.btw.start_time'] = str(startTime)
            if endTime == None:
                queryParams['filter.btw.start_time'] += ',' + utils.actualTimestamp()
                params['endTime'] = utils.actualDatetime()
        else:
            return ('Error', {'startTime': 'Incorrect datetime format, use \'DD/MM/YYYY HH:MM\'.'}, 406)

    if endTime != None:
        if utils.validateDateTime(endTime):
            params['endTime'] = str(endTime)
            endTime = utils.convertDateTimeToTimestamp(endTime)
            queryParams['filter.btw.start_time'] += ',' + str(endTime)
        else:
            return ('Error', {'endTime': 'Incorrect datetime format, use \'DD/MM/YYYY HH:MM\'.'}, 406)
    params['queryParams'] = queryParams
    return ('Success', params)

def data_to_xml(data):
    return ET.fromstring(str(data))

def xml(data, code, headers):
    return 

class Home(Resource):
    def get(self):
        return {'Lauches': '/reportportal-analytics/launches',
                'Lauches Analytics': '/reportportal-analytics/launches/analytics',
                'Lauches Analytics Consoldated': '/reportportal-analytics/launches/analytics/consolidated',
                'Lauches Analytics Consoldated in junit xml format': '/reportportal-analytics/launches/analytics/consolidated/xml'}

class Lauches(Resource):
    def get(self):
        args = _reqparse.parse_args()
        params = mountArgs(args)
        if params[0] != 'Success':
             return params[1], params[2]
        return launches.get_launches(params[1]), 200

class LauchesAnalytics(Resource):
    def get(self):
        args = _reqparse.parse_args()
        params = mountArgs(args)
        if params[0] != 'Success':
             return params[1], params[2]
        return launches.get_launches_analytics(params[1]), 200

class LauchesAnalyticsConsolidated(Resource):
    def get(self):
        args = _reqparse.parse_args()
        params = mountArgs(args)
        if params[0] != 'Success':
             return params[1], params[2]
        return launches.get_launches_analytics_consolidated(params[1]), 200

class LauchesAnalyticsConsolidatedXml(Resource):
    def get(self):
        args = _reqparse.parse_args()
        params = mountArgs(args)
        if params[0] != 'Success':
             return params[1], params[2]
        return Response(launches.get_launches_analytics_consolidated_xml(params[1]), status=200, mimetype='application/xml',)

class SubTypes(Resource):
    def get(self):
        args = _reqparse.parse_args()
        params = mountArgs(args)
        if params[0] != 'Success':
             return params[1], params[2]
        return subtypes.get_subtypes(params[1])


api.add_resource(Home, '/')
api.add_resource(Lauches, '/reportportal-analytics/launches')
api.add_resource(LauchesAnalytics, '/reportportal-analytics/launches/analytics')
api.add_resource(LauchesAnalyticsConsolidated, '/reportportal-analytics/launches/analytics/consolidated')
api.add_resource(LauchesAnalyticsConsolidatedXml, '/reportportal-analytics/launches/analytics/consolidated/xml')
api.add_resource(SubTypes, '/reportportal/subtypes')

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python app.py -p -d")
    parser.add_option('-p', '--port', action='store', dest='port', help='A porta para monitorar.')
    parser.add_option('-d', '--debug', action='store_true', default=False, dest='debug', help='Iniciar em modo debug.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print("Argumento obrigatório ausente: -p/--port")
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(args.port), debug=args.debug)