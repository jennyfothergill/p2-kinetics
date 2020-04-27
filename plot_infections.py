import matplotlib.pyplot as plt
import numpy as np
import requests
import csv

from kinetics import solve_sir, N


def rmse(y1, y2):
    """Get the root mean squared error between the y-value of two datasets

    Parameters
    ----------
    y1, y2 : array_like
        Input arrays to be compared

    Returns
    -------
    float
        Root mean squared error between y1 and y2
    """
    return np.sqrt(np.mean(np.square(np.subtract(y1, y2))))


if __name__ == "__main__":
    # For making the plot nicer
    plt.rcParams["figure.figsize"] = [18, 7]
    plt.rcParams["font.size"] = 12
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

    fig, ax = plt.subplots(1,2)
    ax1 = ax[0]
    ax2 = ax[1]

    ax1.plot(idaho[weekend_inds, 0], idaho[weekend_inds, 2], "r.", label="infected")
    ax1.plot(idaho[weekend_inds, 0], idaho[weekend_inds, 3], "k.", label="dead")
    ax1.plot(idaho[weekday_inds, 0], idaho[weekday_inds, 2], "ro")
    ax1.plot(idaho[weekday_inds, 0], idaho[weekday_inds, 3], "ko")

    event_inds = np.argwhere(idaho[:, 4] != "")
    maxcase = max(idaho[:, 2])
    colors = ["aquamarine", "thistle", "lightblue", "pink"]
    for i,ind in enumerate(event_inds):
        ax1.plot((idaho[ind, 0], idaho[ind, 0]), (0, maxcase), "--", label=idaho[ind, 4][0], color=colors[i])
    ax1.legend(
        title="small dots indicate weekend\nlarger dots are weekdays",
        loc="upper left",
    )
    ax1.set_title("Idaho COVID-19 data shown with relevant events")
    locs = list(idaho[:, 0])[::5]
    labels = ["/".join(i.split("-")[1:]) for i in list(idaho[:, 1])[::5]]
    ax1.set_xticks(locs)
    ax1.set_xticklabels(labels)
    ax1.set_xlabel("date")
    ax1.set_ylabel("people")
    ax1.set_ylim((-10, maxcase * 1.5))

    # rmses = []
    # k1_start = 0
    # k1_stop = 1
    # k2_start = 0
    # k2_stop = 1

    # k1s = np.linspace(k1_start,k1_stop)
    # k2s = np.linspace(k2_start,k2_stop)
    # for k1 in k1s:
    #    for k2 in k2s:
    #        model = solve_sir(k1, k2, N - 2, 2, 0, maxday=max(idaho[:,0]))
    #        rmses.append((rmse(model.y[1],idaho[:, 2]), k1, k2))

    # rmses = np.array(rmses)
    # rmse_best = rmses[:,0].min()
    # best_row = np.argwhere(rmses[:,0]==rmse_best)[0][0]
    # k1_best, k2_best = rmses[best_row,1:]

    # model = solve_sir(k1_best, k2_best, N - 2, 2, 0, maxday=max(idaho[:,0]))

    k1_1 = 1.3
    k2_1 = 1

    model1 = solve_sir(k1_1, k2_1, N - 2, 2, 0)
    # k1 = 1.3, k2 = 1 fits really well for beginning

    switchday = 21  # this value was chosen simply by looking at the graph

    k1_2 = 1.06
    k2_2 = 1.025

    model2 = solve_sir(k1_2, k2_2, N - idaho[switchday, 2], idaho[switchday, 2], 0)

    print("The stats below relate to the rightmost plot.\n")
    print(f"The day that the model parameters switch is day {switchday}.\n")
    print("Predicted maximum number of infected people:")
    print(f"\tmodel 1: {max(model1.y[1]):.0f}")
    print(f"\tmodel 2: {max(model2.y[1]):.0f}")

    mean = np.mean(idaho[:,2])
    rmse1 = rmse(model1.y[1][:switchday], idaho[:switchday, 0])
    nrmse1 = rmse1/np.mean(idaho[:switchday,2])
    maxday = idaho[-1, 0]
    rmse2 = rmse(model2.y[1][switchday : maxday + 1], idaho[switchday:, 0])/mean
    nrmse2 = rmse2/np.mean(idaho[switchday:,2])

    print("\nNormalized RMSE:")
    print(f"\tmodel 1: {nrmse1:.3f}\n\tmodel 2: {nrmse2:.3f}")

    ax2.plot(idaho[:, 0], idaho[:, 2], "r.", label="(data) infected")

    ax2.plot(
        model1.t[:switchday],
        model1.y[1][:switchday],
        "--",
        label=f"(model) infected\nk1 = {k1_1} k2={k2_1}",
    )

    ax2.plot(
        model2.t + switchday,
        model2.y[1],
        "--",
        label=f"(model) infected\nk1 = {k1_2} k2={k2_2}",
    )

    ax2.set_xlabel("days")
    ax2.set_ylabel("people")
    ax2.legend()
    ax2.set_ylim((-10, maxcase * 1.5))
    ax2.set_title("Idaho COVID-19 cases alongside SIR model")

    plt.show()
