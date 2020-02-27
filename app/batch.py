__version__ = "1.0.0"

import argparse

import launches
import subtypes
import utils

infos = ['launches', 'launches-analytics', 'launches-analytics-consolidated',
      'launches-analytics-consolidated-xml', 'subtypes']

# Define the command-line arguments
parser = argparse.ArgumentParser(
    description='Extract information about test executions by the ReportPortal APIs')
parser.add_argument('-i', choices=infos, default=infos[0], help='the desired information. The default is ' + infos[0])
parser.add_argument('--apiToken', action='store', required=True, help='the API Token from ReportPortal')
parser.add_argument('--project', action='store', required=True, help='the project from ReportPortal')
parser.add_argument('--url', action='store', required=True, help='the URL from ReportPortal')
parser.add_argument('--startTime', action='store', required=True, help='the start time to the query filter. use te format "DD/MM/YYYY HH:MM"')
parser.add_argument('--endTime', action='store', help='the end time to the query filter. use te format "DD/MM/YYYY HH:MM"')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s ' + __version__)

def mountArgs(args):
    params = {}
    params['apiToken'] = args.apiToken
    params['project'] = args.project
    params['url'] = args.url
    queryParams = {'page.size':'100', 'page.page': '1', 'page.sort':'start_time,number,DESC', 'filter.cnt.name':'TestRun'}
    startTime = args.startTime
    endTime = args.endTime

    if startTime != None:
        if utils.validateDateTime(startTime):
            params['startTime'] = str(startTime)
            startTime = utils.convertDateTimeToTimestamp(startTime)
            queryParams['filter.btw.start_time'] = str(startTime)
            if endTime == None:
                queryParams['filter.btw.start_time'] += ',' + utils.actualTimestamp()
                params['endTime'] = utils.actualDatetime()
        else:
            return ('Error', {'startTime': 'Incorrect datetime format, use \'DD/MM/YYYY HH:MM\'.'})

    if endTime != None:
        if utils.validateDateTime(endTime):
            params['endTime'] = str(endTime)
            endTime = utils.convertDateTimeToTimestamp(endTime)
            queryParams['filter.btw.start_time'] += ',' + str(endTime)
        else:
            return ('Error', {'endTime': 'Incorrect datetime format, use \'DD/MM/YYYY HH:MM\'.'})
    params['queryParams'] = queryParams
    return ('Success', params)

def getLaunches(args):
    params = mountArgs(args)
    if params[0] != 'Success':
            return params[1]
    return launches.get_launches(params[1])

def getLaunchesAnalytics(args):
    params = mountArgs(args)
    if params[0] != 'Success':
            return params[1]
    return launches.get_launches_analytics(params[1])

def getLaunchesAnalyticsConsolidated(args):
    params = mountArgs(args)
    if params[0] != 'Success':
            return params[1]
    return launches.get_launches_analytics_consolidated(params[1])

def getLaunchesAnalyticsConsolidatedXml(args):
    params = mountArgs(args)
    if params[0] != 'Success':
            return params[1]
    return launches.get_launches_analytics_consolidated_xml(params[1])

def getSubtypes(args):
    params = mountArgs(args)
    if params[0] != 'Success':
            return params[1]
    return subtypes.get_subtypes(params[1])

if __name__ == '__main__':
    # Parse the command-line args
    args = parser.parse_args()
    option = args.i
    if option == infos[0]:
        print(getLaunches(args))
    elif option == infos[1]:
        print(getLaunchesAnalytics(args))
    elif option == infos[2]:
        print(getLaunchesAnalyticsConsolidated(args))
    elif option == infos[3]:
        print(getLaunchesAnalyticsConsolidatedXml(args))
    elif option == infos[4]:
        print(getSubtypes(args))