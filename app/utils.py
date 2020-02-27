import re
import datetime

def getHeaders(apiToken):
    return {'Content-Type': 'Application/json',
            'Accept': 'application/json',
            'Authorization': 'bearer ' + apiToken}

def validateDateTime(dateTime):
    pattern = re.compile(r"^\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2}$")
    if pattern.match(dateTime):
        return True
    return False

def convertDateTimeToTimestamp(dateTime):
    day = int(dateTime[0:2])
    month = int(dateTime[3:5])
    year = int(dateTime[6:10])
    hour = int(dateTime[11:13])
    minute = int(dateTime[14:16])
    return str(int(datetime.datetime(year, month, day, hour, minute).timestamp())) + '000'

def actualTimestamp():
    return str(int(datetime.datetime.now().timestamp())) + '000'

def actualDatetime():
    return datetime.datetime.now().strftime('%d/%m/%Y %H:%M')