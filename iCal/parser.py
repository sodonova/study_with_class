from icalendar import Calendar
from datetime import datetime
import requests
import pytz

url = "https://timetable.mypurdue.purdue.edu/Timetabling/export?x=qn4erbfu7ahb4m4177ksu0x1kypechmu"
c = requests.get(url).text

cal = Calendar.from_ical(c)

now = pytz.UTC.localize(datetime(2022,1,10))

for event in cal.walk('VEVENT'):

    start = event.decoded('DTSTART')
    end = event.decoded('DTEND')
    summary = event['SUMMARY']

    if event['dtstart'].dt >= now:
        print(summary)
        print(start)
        print(end)
        print(event['RRULE'])
    