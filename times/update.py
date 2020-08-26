from bs4 import BeautifulSoup
import os
import datetime
import csv

# Initialise currentDay to be start of week
today = datetime.date.today()
currentDay = today - datetime.timedelta(days=today.weekday())

# Parse times.html
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
address = os.path.join(THIS_FOLDER, '..\\times.html')
soup = BeautifulSoup(open(address), features="lxml")
calDates = soup.find_all("td")

# Parse events.csv
events = list()
with open(os.path.join(THIS_FOLDER, 'events.csv')) as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        event = soup.new_tag("div", **{"class": row["College"]})
        event.string = f"{row['Time']} {row['Who']} {row['What']}"
        events.append((row['Month'], row['Day'],  event))

# Loop through td tags and edit each one in soup object
for calDate in calDates:
    calDate.clear()
    calDate.append(currentDay.strftime("%b %d"))
    # if currentDay < today:
    #     calDate = calDate.string.wrap(soup.new_tag('del'))

    for date in events:
        if (currentDay.month, currentDay.day) == (int(date[0]), int(date[1])):
            calDate.append(date[2])
    currentDay += datetime.timedelta(days=1)

footer = soup.find('footer')
footer_text = today.strftime('Last updated: %d/%m/%Y')
footer.string = footer_text


# Write completed soup back into html file
fh = open(address, "w")
fh.write(str(soup))
fh.close()
