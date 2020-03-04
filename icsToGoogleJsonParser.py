import re
import datetime as dt
from os import listdir
import updateDB

# .ics date format
DATE_READ_FORMAT = r'%Y%m%dT%H%M%SZ'
# custom event types
EVENT_TYPE = { 
    'P.Col' : 'PROJECT',
    'Rome A2' : 'CUEFEE',
    'CM' : 'LECTURE',
    'TD' : 'TUTORIAL',
    'TP' : 'LABS',
    'ET' : 'EXAM',
    'CC' : 'EXAM',
    }


def parseTime(timeStr):
    '''Parses the date to iso format and applies UTC+1 offset'''
    dateTimeObj = dt.datetime.strptime(timeStr, DATE_READ_FORMAT)
    dateTimeObj = dateTimeObj.replace(hour=(dateTimeObj.hour + 1))
    return dateTimeObj.isoformat()


def parseType(summary):
    """Parses "summary" event field and returns a mapping to EVENT_TYPE"""
    for k, t in EVENT_TYPE.items():
        if (k in summary):
            return t
    

def parseFile(file):
    """Parses raw .ics file into Google Calendar compatibile objects"""
    # read the text and split it into lines
    o = file.read().splitlines()
    # recombine all the lines together
    i = len(o) - 1
    while i > -1:
        if (o[i][0] == ' '):
            # assuming the case there cannot be a space at the very beginning of the file
            o[i - 1] =  o[i - 1] + o[i]
            del o[i]
        i-=1
    # split each entry of the list to key-value pair
    o = [e.split(':') for e in o]
    # parse each event to dict
    d = []
    for i in range(len(o)):
        if (o[i] == ['BEGIN', 'VEVENT']):
            d.append({e[0]: e[1] for e in o[i+2:i+7]})

    # modify time formats and edit description
    for event in d:
        # parse time
        event["DTSTART"] = parseTime(event["DTSTART"])
        event["DTEND"] = parseTime(event["DTEND"])
        # format description
        event["DESCRIPTION"] = event["DESCRIPTION"].split('(')[0]
        event["DESCRIPTION"] = event["DESCRIPTION"].replace(r'\n', ' ')
        # add type
        event["TYPE"] = parseType(event["SUMMARY"])
        
    return d


def filterEvents(events):
    """Filters provided events according to register (data/courseRegister.json) configuration"""
    courseRegister = updateDB.getCourseRegister()
    isNew = False
    delList = []
    for e in events:
        if (e["SUMMARY"] in courseRegister["followedCourses"]):
            pass
        else:
            for key in courseRegister["keywords"]:
                if re.search(re.escape(key), e["SUMMARY"]):
                    courseRegister["followedCourses"].append(e["SUMMARY"])
                    isNew = True

            if (not isNew):
                delList.append(e)
      
    events = [d for d in events if d not in delList]

    if (isNew):
        updateDB.setCourseRegister(courseRegister)

    return events


def main():
    print("Parsing files...")
    events = []
    for ics in listdir("downloads"):
        with open("downloads/" + ics, "r") as f:
            events = [*events, *parseFile(f)]
    updateDB.setCourses(filterEvents(events))
    print("Finished")


if __name__ == "__main__":
    main()