import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, date
from dataclasses import dataclass, field

holidayList = []
dateList = []
holidays = []
saved = True
leave = False

@dataclass
class Holiday:
    name: str
    date: str

    def __str__(self):
        return (self.name + " (" + self.date + ")")

    def __eq__(self, other):
        return (self.name == other.name)

def weatherForecast():
    urlW = "https://api.tomorrow.io/v4/timelines"

    querystring = {
    "location":"43, 88",
    "fields":["temperature", "cloudCover"],
    "units":"imperial",
    "timesteps":"1d",
    "endTime":"2021-10-11T00:00:00Z",
    "apikey":"vCuqHuKcMjIpYmzQ9OdigBp1Pstjvpb3"}

    response = requests.request("GET", urlW, params=querystring)

    print("Weather Forecast")
    print("================")

    results = response.json()['data']['timelines'][0]['intervals']
    for daily_result in results:
        date = daily_result['startTime'][0:10]
        temp = round(daily_result['values']['temperature'])
        cloud = round(daily_result['values']['cloudCover'])
        print("On",date,"it will be", temp, "F and there will be", cloud, "percent cloud coverage")

def dateFormat(date):
    return datetime.strptime(date, "%b %d, %Y").strftime("%Y-%m-%d")

def addHoliday(name):
    date = input("Date [yyyy-mm-dd]: ")

    if len(date) != 10:
        print("Error:")
        print("Invalid date. Please try again.")
        addHoliday(name)
    else:
        newHoliday = Holiday(name, date)
        holidays.append(newHoliday)

        print("Success:")
        print(newHoliday, "has been added to the holiday list.")

    holidays.sort(key=lambda r: r.date)    
    return False

def removeHoliday():
    found = False

    print("Remove a holiday")
    print("================")
    name = input("Holiday Name: ")
    nameObj = Holiday(name, "")
    holidaysTemp = list(holidays)

    for i in range(0, len(holidaysTemp)):
        if holidaysTemp[i] == nameObj:
            del holidays[i]
            found = True

    if found == False:
        print("Error:")
        print(name + " not found.")
        return True
    else:
        print("Success:")
        print(name + " has been removed from the holiday list.")
        return False

def saveHolidays(): #error checking not implemented
    print("Saving Holiday List")
    print("===================")

    decision = input("Are you sure you want to save your changes? [y/n]: ").lower()

    if decision == "n":
        print("Canceled:")
        print("Holiday list file save canceled.")
        return 0
    elif decision == "y":
        jsonObjct = json.dumps(holidays, default = lambda x: x.__dict__)
        fout = open("HolidayList.json", "w")
        fout.write(jsonObjct)
        fout.close()
        
        print("Success:")
        print("Your changes have been saved.")
        return True

def viewHolidays(): #error checking not implemented
    dayRange = []
    
    print("View Holidays")
    print("=============")
    yr = input("Which year?: ")
    wk = input("Which week? #[1-52, leave blank for current week]: ")

    if wk == "":
        wk = str(date.today().isocalendar()[1])
        forecast = input("Would you like to see the weather for this week? [y/n]: ").lower()

        if forecast == "y":
            weatherForecast()

    print("\nThese are the holidays for " + yr + " week #" + wk + ":")

    for i in range(1, 8):
        d = str(datetime.fromisocalendar(int(yr), int(wk), i))
        dayRange.append(d[:10])

    results = filter(lambda x: x in dayRange, dateList)

    for i in range(0, 7):
        if dayRange[i] in dateList:
            start = dateList.index(dayRange[i])
            break
    
    for i in range(6, 0, -1):
        if dayRange[i] in dateList:
            end = dateList.index(dayRange[i])
            break
    
    for index in range(start, end):
        print(holidays[index])

with open("holidays.json") as jf:
    data = json.load(jf)
    jf.close()

for i in range(0, len(data["holidays"])):
    holidays.append(Holiday(data["holidays"][i]["name"], data["holidays"][i]["date"]))

for i in range(0, 5):
    year = "202" + str(i)
    tempList = []
    
    url = "https://www.timeanddate.com/holidays/us/202" + str(i)
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    out = [[td.text.strip() for td in tr.select("th, td")] for tr in soup.select("tr[data-mask]")]

    for item in out:
        holidayList.append(item[2])

    for item in out:
        oldDate = (item[0] + ", " + year)
        tempList.append(oldDate)

    for dt in tempList:
        newDate = dateFormat(dt)
        dateList.append(newDate)
    
for i in range(0, len(holidayList)):
    holidays.append(Holiday(holidayList[i], dateList[i]))

holidays.sort(key=lambda r: r.date)

print("Holiday Management")
print("==================")
print("There are " + str(len(holidays)) + " holidays in the system.")

while leave == False:
    decision = input("""\nHoliday Menu
    ============
    1. Add a holiday
    2. Remove a holiday
    3. Save holiday list
    4. View holidays
    5. Exit\n""")

    if decision.isnumeric() == False:
        continue
    elif int(decision) == 1:
        print("Add a holiday")
        print("=============")
        name = input("Holiday: ")
        saved = addHoliday(name)
    elif int(decision) == 2:
        saved = removeHoliday()
    elif int(decision) == 3:
        temp = saveHolidays()
        if temp == True:
            saved = True
    elif int(decision) == 4:
        viewHolidays()
    elif int(decision) == 5:
        print("Exit")
        print("====")
        
        if saved == True:
            choice = input("Are you sure you want to exit? [y/n]: ").lower()
            if choice == "y":
                print("Goodbye!")
                leave = True
        else:
            print("Are you sure you want to exit?")
            choice = input("Your changes will be lost. [y/n]: ")
            if choice == "y":
                print("Goodbye!")
                leave = True
    else:
        continue