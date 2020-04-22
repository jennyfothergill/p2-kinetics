import matplotlib.pyplot as plt
import numpy as np
import requests
import csv

from kinetics import solve_sir, N


def mse(y1, y2):
    """Get the mean squared error between the y-value of two datasets

    Parameters
    ----------
    y1, y2 : array_like
        Input arrays to be compared

    Returns
    -------
    float
        Mean squared error between y1 and y2
    """
    return np.mean(np.square(np.subtract(y1, y2)))


if __name__ == "__main__":
    # For making the plot nicer
    plt.rcParams["figure.figsize"] = [9, 9]
    plt.rcParams["font.size"] = 18
    plt.rcParams["lines.linewidth"] = 4
    plt.rcParams["lines.markersize"] = 10

    # csv format is date,state,fips,cases,deaths
    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode("utf-8")

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
                    # print(row[0])
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
    weekend_inds = np.argwhere(idaho[:, 5] == 1)
    weekday_inds = np.argwhere(idaho[:, 5] == 0)

    plt.plot(idaho[weekend_inds, 0], idaho[weekend_inds, 2], "r.", label="infected")
    plt.plot(idaho[weekend_inds, 0], idaho[weekend_inds, 3], "k.", label="dead")
    plt.plot(idaho[weekday_inds, 0], idaho[weekday_inds, 2], "ro")
    plt.plot(idaho[weekday_inds, 0], idaho[weekday_inds, 3], "ko")

    event_inds = np.argwhere(idaho[:, 4] != "")
    maxcase = max(idaho[:, 2])
    for i in event_inds:
        plt.plot((idaho[i, 0], idaho[i, 0]), (0, maxcase), "--", label=idaho[i, 4][0])

    plt.legend(
        title="small dots indicate weekend\nlarger dots are weekdays",
        loc="upper left",
        fontsize=14,
    )
    locs = list(idaho[:, 0])[::5]
    labels = ["/".join(i.split("-")[1:]) for i in list(idaho[:, 1])[::5]]
    plt.xticks(locs, labels)
    plt.xlabel("date")
    plt.ylabel("people")
    plt.ylim((-10, maxcase * 1.5))
    plt.show()

    # mses = []
    # k1_start = 0
    # k1_stop = 1
    # k2_start = 0
    # k2_stop = 1

    # k1s = np.linspace(k1_start,k1_stop)
    # k2s = np.linspace(k2_start,k2_stop)
    # for k1 in k1s:
    #    for k2 in k2s:
    #        model = solve_sir(k1, k2, N - 2, 2, 0, maxday=max(idaho[:,0]))
    #        mses.append((mse(model.y[1],idaho[:, 2]), k1, k2))

    # mses = np.array(mses)
    # mse_best = mses[:,0].min()
    # best_row = np.argwhere(mses[:,0]==mse_best)[0][0]
    # k1_best, k2_best = mses[best_row,1:]

    # model = solve_sir(k1_best, k2_best, N - 2, 2, 0, maxday=max(idaho[:,0]))

    k1_1 = 1.3
    k2_1 = 1

    model1 = solve_sir(k1_1, k2_1, N - 2, 2, 0)
    # k1 = 1.3, k2 = 1 fits really well for beginning

    switchday = 21  # this value was chosen simply by looking at the graph

    k1_2 = 1.06
    k2_2 = 1.025

    model2 = solve_sir(k1_2, k2_2, N - idaho[switchday, 2], idaho[switchday, 2], 0)

    print("Predicted maximum number of infected people:")
    print(f"\tmodel 1: {max(model1.y[1]):.0f}")
    print(f"\tmodel 2: {max(model2.y[1]):.0f}")

    mse1 = mse(model1.y[1][:switchday], idaho[:switchday, 0])
    maxday = idaho[-1, 0]
    mse2 = mse(model2.y[1][switchday : maxday + 1], idaho[switchday:, 0])

    print("\nMSE")
    print(f"\tmodel 1: {mse1:.3f}\n\tmodel 2: {mse2:.3f}")

    plt.plot(idaho[:, 0], idaho[:, 2], "r.", label="(data) infected")

    plt.plot(
        model1.t[:switchday],
        model1.y[1][:switchday],
        "--",
        label=f"(model) infected\nk1 = {k1_1} k2={k2_1}",
    )

    plt.plot(
        model2.t + switchday,
        model2.y[1],
        "--",
        label=f"(model) infected\nk1 = {k1_2} k2={k2_2}",
    )

    plt.xlabel("days")
    plt.ylabel("people")
    plt.legend()
    plt.ylim((-10, maxcase * 1.5))
    plt.show()
