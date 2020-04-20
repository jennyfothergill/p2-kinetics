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

        add_row = [days, row[0], int(row[3]), int(row[4]), event]
        idaho.append(np.array(add_row, dtype=object))
        days += 1

# idaho format is days_since_first_infection,date,cases,deaths,event
idaho = np.array(idaho)

plt.plot(idaho[:,0],idaho[:,2], label="infected people")
plt.plot(idaho[:,0],idaho[:,3], label="deaths")

event_inds = np.argwhere(idaho[:,4] != "")
maxcase = max(idaho[:,2])
for i in event_inds:
    plt.plot((idaho[i,0],idaho[i,0]), (0,maxcase), "--", label=idaho[i,4][0])

plt.legend(loc="upper left")
locs = list(idaho[:,0])[::5]
labels = ["/".join(i.split("-")[1:]) for i in list(idaho[:,1])[::5]]
plt.xticks(locs, labels)
plt.xlabel("date")
plt.ylabel("people")
plt.ylim((0,maxcase*1.5))
plt.show()
