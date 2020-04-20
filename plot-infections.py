import matplotlib.pyplot as plt
import numpy as np
import requests
import csv

# For making the plot nicer
plt.rcParams['figure.figsize'] = [9, 9]
plt.rcParams['font.size'] = 18
plt.rcParams['lines.linewidth'] = 4
plt.rcParams['lines.markersize'] = 10


# csv format is date,state,fips,cases,deaths
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

with requests.Session() as s:
    download = s.get(url)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=",")
    my_list = list(cr)

d_date = np.dtype([("date", np.unicode, 11), ("event", np.unicode, 256)])

important_dates = np.loadtxt(
        "data/important_dates.csv", skiprows=1, delimiter=", ", dtype=d_date
        )

# idaho format is days_since_first_infection,date,cases,deaths,event
idaho = []
days = 0
event_i = 0
for row in my_list:
    if row[1] == "Idaho":
        try:
            if row[0] == important_dates[event_i]["date"]:
                #print(row[0])
                event = important_dates[event_i]["event"]
                event_i += 1
            else:
                event = ""
        except IndexError:
            event = ""
        # 3/13 (day 0) was a Friday
        # so Sat/Sun will be days 1 and 2 of the "week"
        # weekend --> 1, weekday --> 0
        weekend = int(days % 7 == 1 or days % 7 == 2)

        add_row = [days, row[0], int(row[3]), int(row[4]), event, weekend]
        idaho.append(np.array(add_row, dtype=object))
        days += 1

# idaho format is days_since_first_infection,date,cases,deaths,event,weekend?
idaho = np.array(idaho)
weekend_inds = np.argwhere(idaho[:,5]==1)
weekday_inds = np.argwhere(idaho[:,5]==0)

plt.plot(idaho[weekend_inds,0],idaho[weekend_inds,2], "r.", label="infected")
plt.plot(idaho[weekend_inds,0],idaho[weekend_inds,3], "k.", label="dead")
plt.plot(idaho[weekday_inds,0],idaho[weekday_inds,2], "ro")
plt.plot(idaho[weekday_inds,0],idaho[weekday_inds,3], "ko")

event_inds = np.argwhere(idaho[:,4] != "")
maxcase = max(idaho[:,2])
for i in event_inds:
    plt.plot((idaho[i,0],idaho[i,0]), (0,maxcase), "--", label=idaho[i,4][0])

plt.legend(
        title="small dots indicate weekend\nlarger dots are weekdays",
        loc="upper left",
        fontsize=14
        )
locs = list(idaho[:,0])[::5]
labels = ["/".join(i.split("-")[1:]) for i in list(idaho[:,1])[::5]]
plt.xticks(locs, labels)
plt.xlabel("date")
plt.ylabel("people")
plt.ylim((-10,maxcase*1.5))
plt.show()
