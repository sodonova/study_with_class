from icalendar import Calendar
import datetime
import recurring_ical_events
import requests
import pytz
import math

MO = datetime.datetime(2022,1,10).date()
TU = datetime.datetime(2022,1,11).date()
WE = datetime.datetime(2022,1,12).date()
TR = datetime.datetime(2022,1,13).date()
FR = datetime.datetime(2022,1,14).date()
THIRTY = datetime.timedelta(minutes = 30)
FIFTY = datetime.timedelta(hours=0, minutes=50)
HOUR15 = datetime.timedelta(hours=1, minutes=15)

mon = {'700':0, '750':0, '800':0, '850':0, '900':0, '950':0, '1000':0, '1050':0, '1100':0, '1150':0, '1200':0, '1250':0, '1300':0, '1350':0, 
        '1400':0, '1450':0, '1500':0, '1550':0, '1600':0, '1650':0, '1700':0, '1750':0, '1800':0, '1850':0, '1900':0, '1950':0, '2000':0, '2050':0}
tue = {'700':0, '750':0, '800':0, '850':0, '900':0, '950':0, '1000':0, '1050':0, '1100':0, '1150':0, '1200':0, '1250':0, '1300':0, '1350':0, 
        '1400':0, '1450':0, '1500':0, '1550':0, '1600':0, '1650':0, '1700':0, '1750':0, '1800':0, '1850':0, '1900':0, '1950':0, '2000':0, '2050':0}
wed = {'700':0, '750':0, '800':0, '850':0, '900':0, '950':0, '1000':0, '1050':0, '1100':0, '1150':0, '1200':0, '1250':0, '1300':0, '1350':0, 
        '1400':0, '1450':0, '1500':0, '1550':0, '1600':0, '1650':0, '1700':0, '1750':0, '1800':0, '1850':0, '1900':0, '1950':0, '2000':0, '2050':0}
thu = {'700':0, '750':0, '800':0, '850':0, '900':0, '950':0, '1000':0, '1050':0, '1100':0, '1150':0, '1200':0, '1250':0, '1300':0, '1350':0, 
        '1400':0, '1450':0, '1500':0, '1550':0, '1600':0, '1650':0, '1700':0, '1750':0, '1800':0, '1850':0, '1900':0, '1950':0, '2000':0, '2050':0}
fri = {'700':0, '750':0, '800':0, '850':0, '900':0, '950':0, '1000':0, '1050':0, '1100':0, '1150':0, '1200':0, '1250':0, '1300':0, '1350':0, 
        '1400':0, '1450':0, '1500':0, '1550':0, '1600':0, '1650':0, '1700':0, '1750':0, '1800':0, '1850':0, '1900':0, '1950':0, '2000':0, '2050':0}

url = "https://timetable.mypurdue.purdue.edu/Timetabling/export?x=qn4erbfu7ahb4m4177ksu0x1kypechmu"
c = requests.get(url).text

cal = Calendar.from_ical(c)

week_start = pytz.UTC.localize(datetime.datetime(2022,1,10))
week_end = pytz.UTC.localize(datetime.datetime(2022,1,14))

events = recurring_ical_events.of(cal).between(week_start, week_end)


classes = set()

for event in events:

    start_hour = event["DTSTART"].dt.time().hour
    # Modify start tim of classes to always be either 00 or 50
    start_min = math.floor(event["DTSTART"].dt.minute/30) * 50
    #zfill(2) to pad 0 to 00 when classes start on the hour 
    start_time = str(start_hour) + str(start_min).zfill(2)
    day = event["DTSTART"].dt.date()
    end = event["DTEND"].dt.time()

    duration = event["DTEND"].dt - event["DTSTART"].dt
    slots = math.ceil(duration/THIRTY) #Determine how many slots to update
    ctr = int(start_time)

    for i in range(slots):
        start_time = str(ctr)
        if day == MO:
            mon[start_time] = 1
        if day == TU:
            tue[start_time] = 1
        if day == WE:
            wed[start_time] = 1
        if day == TR:
            thu[start_time] = 1
        if day == FR:
            fri[start_time] = 1
        ctr+=50
    summary = event['SUMMARY'].split()
    cid = summary[0] + " " + summary[1]
    classes.add(cid)

    print(cid)
    print("start: {} duration: {}".format(start_time, duration))

print(classes)
print(mon)
print(tue)
    