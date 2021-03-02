from ics import Calendar, Event
from bs4 import BeautifulSoup
from sys import argv
import arrow

# Create main calendar to be exported
cal = Calendar()

# Get key dates for calendar
print("Key dates :")
firstDate = input("\twhen is the first monday of the semester? [YYYY-MM-DD]: ")
firstDate = arrow.get(firstDate, "YYYY-MM-DD")
firstDate = firstDate.shift(weekday=0) # make sure monday
firstDate = firstDate.replace(tzinfo='Australia/Sydney') # make timezone Sydney 
breakWeek = int(input("\twhat week is the break? [1-14]: "))

with open(argv[1], 'r', encoding="ISO-8859-1") as solsCalInput:
    solsCal = solsCalInput.read() # read in file to  raw HTML
    solsCal = BeautifulSoup(solsCal, 'lxml') # convert raw HTML to soup object
    solsCal = solsCal.find("div", {"id": "content"}) # trim soup object to find just calendar content
    
    timetable = [] # create blank timetable 

    dayIndex = -1 # index of day of week

    for calEvent in solsCal.find_all("li", {"class": "list-group-item"}): 
        # parse header and context 
        solsEventHeader = calEvent.find("h4").text.split(" - ")
        solsEventCtx = [BeautifulSoup(eventSplitStr, 'lxml').text.split() for eventSplitStr in str(calEvent.find("p")).split("<br/>")]
        
        # skip if was just week title e.g. "Monday"
        if solsEventCtx == [['None']]: # context is "None" arr if week title
            dayIndex += 1 # increment index of day
            continue

        # get data from header and context
        eventHeader = "{} : {}".format(solsEventHeader[1], solsEventCtx[0][-1]) 
        eventTime = [dayIndex, solsEventCtx[1][2], solsEventCtx[1][4]]

        print("Event : \n\t name : {}  \n\t time : {} \n\t ".format(eventHeader, eventTime))
        timetable.append({ "name" : eventHeader, "time" : eventTime})
    
    for timetableItem in timetable:
        templateEvent = Event()
        templateEvent.name = timetableItem["name"]
        dayTime = firstDate.shift(weekday=int(timetableItem["time"][0])) 
        timeSplit = timetableItem["time"][1].split(":")
        templateEvent.begin = dayTime.replace(hour=int(timeSplit[0]), minute=int(timeSplit[1])) 
        timeSplit = timetableItem["time"][2].split(":")
        templateEvent.end = dayTime.replace(hour=int(timeSplit[0]), minute=int(timeSplit[1]))
        for week in range(0,14):
            if week != (breakWeek-1): # skip break week
                event = Event() # hard clone template
                event.name = templateEvent.name
                event.begin = templateEvent.begin
                event.end = templateEvent.end
                cal.events.add(event) # save new event to calendar
            templateEvent.end = templateEvent.end.shift(weeks=+1) # shift end first because end must always be before
            templateEvent.begin = templateEvent.begin.shift(weeks=+1)

    
    with open('sols.ics', 'w') as solsCalOutput:
        solsCalOutput.writelines(cal)
        print("sols.ics written successfully!")
            
            
