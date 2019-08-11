from tools import *
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np

# make figure and assign axis objects
fig = plt.figure(figsize=(9, 5.0625))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
fig.subplots_adjust(wspace=0)
    
while True:
    data = current_production()

    production = []
    # get all production types. name and amount
    domestic_production = data["responseBody"]["responseList"]["item"]
    for prod_type in domestic_production:
        fuel = prod_type["fuelType"]
        MW = float(prod_type["currentMW"])
        #percent = float(prod_type["currentPercentage"])
        production.append((fuel,MW))#,percent))

    # convert to pie chart params
    labels = []
    values = []
    INT_vals = []
    INT_labels = []

    # sort by output
    production = sorted(production, key=lambda x: x[1])[::-1]
    print_columns([["FUEL","OUTPUT MW"]]+production,15)
    for row in production:
        if row[1] != 0:
            label = row[0]
            if label[:3] == "INT":
                INT_vals.append(row[1])
                INT_labels.append(label)
            else:
                values.append(row[1])
                labels.append(label)

    labels.insert(0,"IMPORTED")
    values.insert(0,sum(INT_vals))

    # scale values to sum to 100
    ratios = []
    for value in values:
        ratios.append(100*value/float(sum(values)))

    # clear graph
    ax1.clear()
    ax2.clear()
    # pie chart parameters
    explode = [0 for _ in values]
    explode[0] = 0.1
    # rotate so that first wedge is split by the x-axis
    angle = -180*ratios[0]/100
    ax1.pie(ratios, startangle=angle,
            labels=labels, explode=explode)

    # bar chart parameters
    ratios = []
    for value in INT_vals:
        ratios.append(100*value/float(sum(INT_vals)))

    xpos = 0
    bottom = 0
    width = .2
    colors = [[.1, .3, i/len(INT_vals)] for i in range(len(INT_vals))]
    for j in range(len(ratios)):
        height = ratios[j]
        ax2.bar(xpos, height, width, bottom=bottom, color=colors[j])
        ypos = bottom + ax2.patches[j].get_height() / 2
        bottom += height
        ax2.text(xpos, ypos, f"{INT_vals[j]}MW",
                 ha='center')

    ax2.set_title('INTERCONNECTORS')
    ax2.legend(INT_labels)
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    # get the wedge data
    theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
    center, r = ax1.patches[0].center, ax1.patches[0].r
    bar_height = sum([item.get_height() for item in ax2.patches])

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, bar_height), xyB=(x, y),
                          coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    con.set_linewidth(1)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, 0), xyB=(x, y), coordsA="data",
                          coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(1)
    plt.draw()
    plt.pause(60)

