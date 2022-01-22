from icalendar import Calendar
from datetime import datetime
import recurring_ical_events
import requests
import pytz

MO = datetime(2022,1,10)
TU = datetime(2022,1,11)
WE = datetime(2022,1,12)
TR = datetime(2022,1,13)
FR = datetime(2022,1,14)

url = "https://timetable.mypurdue.purdue.edu/Timetabling/export?x=qn4erbfu7ahb4m4177ksu0x1kypechmu"
c = requests.get(url).text

cal = Calendar.from_ical(c)

week_start = pytz.UTC.localize(datetime(2022,1,10))
week_end = pytz.UTC.localize(datetime(2022,1,14))

events = recurring_ical_events.of(cal).between(week_start, week_end)

for event in events:

    start = event["DTSTART"].dt.time()
    end = event["DTEND"].dt.time()
    duration = event["DTEND"].dt - event["DTSTART"].dt
    summary = event['SUMMARY'].split()
    cid = summary[0] + " " + summary[1]

    print(cid)
    print("start: {} end: {} duration: {}".format(start, end, duration))
    