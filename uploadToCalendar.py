from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import updateDB


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
# french calendar ID
FRENCH_CALENDAR_ID = "npbp5cmdtlq7afnr0uutoiats8@group.calendar.google.com"
# google event color IDs'
COLOR_ID = {
    'YELLOW' : '5',
    'ORANGE' : '6',
    'BLUE' : '9',
    'GREEN' : '10',
    'RED' : '11',
    None : None,
    }
# type to color translation dict
TYPE_COLOR = {
    'PROJECT' : 'BLUE',
    'CUEFEE' : "GREEN",
    'LECTURE' : "YELLOW",
    'TUTORIAL' : None,
    'LABS' : "ORANGE",
    'EXAM' : "RED",
}

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials/credentialsGoogle.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

def createEvents(events):
    """Takes list as parameter and returns the number of created events"""
    eventsNum = 0
    for e in events:
        if (createEvent(e)): 
            eventsNum+=1

    return eventsNum


def createEvent(eventDict):
    event = {
        'summary': eventDict["SUMMARY"],
        'location': eventDict["LOCATION"],
        'description': eventDict["DESCRIPTION"],
        'start': {
            'dateTime': eventDict["DTSTART"],
            'timeZone': 'Europe/Warsaw',
        },
        'end': {
            'dateTime': eventDict["DTEND"],
            'timeZone': 'Europe/Warsaw',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ],
        },
        'colorId': COLOR_ID[TYPE_COLOR[eventDict["TYPE"]]],
    }
        
    return service.events().insert(calendarId=FRENCH_CALENDAR_ID, body=event, sendNotifications=True).execute()


def deleteEvents(events):
    """Takes list as parameter and returns the number of deleted events"""
    eventsNum = 0
    for event in events:
        resp = service.events().delete(calendarId=FRENCH_CALENDAR_ID, eventId=event['id']).execute()
        if (resp == ''):
            eventsNum += 1
        else:
            raise Exception("Delete operation failed:\n" + resp)

    return eventsNum

def clearWeek(fromThisDay):
    """Takes a date as a parameter and deletes all events from the week the day belongs to"""
    thisWeek = weekRange(fromThisDay)
    weekStart = datetime.datetime(thisWeek[0].year, thisWeek[0].month, thisWeek[0].day).isoformat() + 'Z'
    weekEnd = datetime.datetime(thisWeek[1].year, thisWeek[1].month, thisWeek[1].day).isoformat() + 'Z'

    response = service.events().list(calendarId=FRENCH_CALENDAR_ID, timeMin=weekStart, timeMax=weekEnd).execute()
    return deleteEvents(response["items"])


def clearThisWeek():
    """Deletes all events of ongoing week"""
    print("Clearing current week...")
    num = clearWeek(datetime.date.today())
    print("Successfully deleted {} events".format(num))


def uploadDB():
    """Uploads all the events from the database"""
    print("Uploading courses...")
    courses = updateDB.getCourses()
    num = createEvents(courses)
    print("Successfully created {} events".format(num))

def weekRange(date):
    """Find the first/last day of the week for the given day.
    Assuming weeks start on Sunday and end on Saturday.

    Returns a tuple of ``(start_date, end_date)``.

    """
    # isocalendar calculates the year, week of the year, and day of the week.
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = date.isocalendar()

    # Find the first day of the week.
    if dow == 1:
        # Since we want to start with Sunday, let's test for that condition.
        start_date = date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        start_date = date - datetime.timedelta(dow - 1)

    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    end_date = start_date + datetime.timedelta(6)

    return (start_date, end_date)


def main():
    print("UploadToCalendar running...")
    courses = updateDB.getCourses()
    print(createEvent(courses[6]))
 

if __name__ == '__main__':
    main()