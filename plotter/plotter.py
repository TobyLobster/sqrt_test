import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sqrt_n_in_csv_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,17,18]
#sqrt_n_in_csv_order = [0, 18]
fast_list = [3, 9, 15]
slow_list = [4, 8, 16]
log_plots = False

def draw_performance_graph(display_order_for_sqrt_n, title, filename):
    global log_plots

    # Set the random number generator
    mpl.rcParams['svg.hashsalt'] = 'hello'

    order = []
    for i in display_order_for_sqrt_n:
        ind = sqrt_n_in_csv_order.index(i)
        order.append(int(ind))

    # Load the columns we want
    df = pd.read_csv(r'results.csv', na_values=' ', index_col = 0, usecols=order)

    # Re-order the columns in the order we want (z-order)
    order.remove(0)
    sorted_order = sorted(order)
    ordered_column_names = []
    for i in order:
        index = sorted_order.index(i)
        ordered_column_names.append(df.columns[index])

    df = df[ordered_column_names]

    df.plot(figsize=(10.5, 7))
    #print(df.values)
    figure = plt.gcf()
    axes = figure.axes
    #print(axes[0].xaxis)
    plt.title(title)
    plt.gca().set_xlabel("input (0-65535)")
    plt.gca().set_ylabel("cycles")
    if log_plots:
        plt.yscale("log",subs=[1.5,2,3,4,5,6,8])
    from matplotlib.ticker import ScalarFormatter, LinearLocator
    axes[0].yaxis.set_major_formatter(ScalarFormatter())
    axes[0].yaxis.set_minor_formatter(ScalarFormatter())

    major_ticks = [*range(0, 65536, 10000)]
    #major_ticks.append(65535)
    plt.gca().set_xticks(major_ticks)
    plt.gca().set_xticks(range(2000, 65535, 2000), minor=True)

    # Reorder labels
    handles, labels = plt.gca().get_legend_handles_labels()
    one_word_labels = [x.split()[0] for x in labels]

    # Specify order of items in legend
    order = []
    for i in range(0,len(display_order_for_sqrt_n)-1):
        order.append(i)

    #add legend to plot
    plt.subplots_adjust(right=0.8)
    plt.legend([handles[idx] for idx in order],[one_word_labels[idx] for idx in order],bbox_to_anchor=(1.05, 1.0), loc='upper left')

    #save image
    plt.savefig(filename, metadata={'Date': None})

draw_performance_graph([0, 8, 16, 4, 12, 2, 5, 6, 7, 13, 1, 10, 14, 11, 18, 17, 3, 9, 15], "Integer SQRT performance on 6502 (all routines)", "result_all.svg")
draw_performance_graph([0, 12, 2, 5, 6, 7, 13, 1, 10, 14, 11, 18, 17, 3, 9, 15], "Integer SQRT performance on 6502 (the non-slow routines)", "result_useful.svg")
#draw_performance_graph([0, 18], "Integer SQRT performance on 6502", "result_18.svg")
draw_performance_graph([0] + fast_list, "Integer SQRT performance on 6502 (fastest routines only)", "result_fastest.svg")

# Memory vs speed
#
sizes_df = pd.read_csv(r'sizes.csv')

# add 'good' column
sizes_df['good'] = [True] * len(sizes_df.index)

# Make the test_name the first word only
sizes_df['test_name'] = [x.split()[0] for x in sizes_df['test_name']]

# name, memory, good
data = sizes_df.values.tolist()

df = pd.read_csv(r'results.csv', na_values=' ', index_col = 0)
max=df.max()
min=df.min()
avg=df.mean()

for i in range(0, len(data)):
    data[i].append(max[i])
    data[i].append(min[i])
    data[i].append(avg[i])

# Remove the slow ones by index, in reverse order so the indices don't change as we delete
for i in sorted(slow_list, reverse=True):
    del data[i-1]

# check which solutions are 'good'
for i in range(0, len(data)):
    for j in range(0, len(data)):
        if i == j:
            continue

        # If data[j] beats data[i] in both memory and speed, then data[i] is not good
        if (data[i][1] > data[j][1]) and (data[i][5] > data[j][5]):
            data[i][2] = False

#print (data)
good_data = filter(lambda e: e[2], data)
bad_data = filter(lambda e: not e[2], data)

good_data = list(good_data)
bad_data = list(bad_data)

good_x = [mem for (name,mem, good,max,min,avg) in good_data]
good_y = [avg for (name,mem, good,max,min,avg) in good_data]
good_err = [[avg-min for (name,mem, good,max,min,avg) in good_data],
            [max-avg for (name,mem, good,max,min,avg) in good_data]]
bad_x = [mem for (name,mem, good,max,min,avg) in bad_data]
bad_y = [avg for (name,mem, good,max,min,avg) in bad_data]
bad_err = [[avg-min for (name,mem, good,max,min,avg) in bad_data],
           [max-avg for (name,mem, good,max,min,avg) in bad_data]]
#print (good_data,good_err)
# plot
mpl.rcParams['svg.hashsalt'] = 'hello'
fig, ax = plt.subplots(figsize=(10.5, 7))
if log_plots:
    plt.xscale("log",subs=[1.5,2,3,4,5,6,8])
    plt.yscale("log",subs=[1.5,2,3,4,5,6,8])
    plt.xlim([25,1100])
else:
    plt.ylim([0, 1350])
from matplotlib.ticker import ScalarFormatter #,NullFormatter,LinearLocator
if log_plots:
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_minor_formatter(ScalarFormatter())
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.xaxis.set_minor_formatter(ScalarFormatter())
ax.xaxis.get_ticklocs(minor=True)
ax.yaxis.get_ticklocs(minor=True)
ax.minorticks_on()

#locmin = LinearLocator(numticks=100)
#ax.xaxis.set_minor_locator(locmin)

plt.gca().set_xlabel("memory (bytes)") #, fontweight='bold')
plt.gca().set_ylabel("average time taken (cycles)") #, fontweight='bold')

ax.scatter(bad_x, bad_y, color="lightgrey")
ax.errorbar(bad_x, bad_y, xerr=None, capsize=3,yerr=bad_err, fmt="none", color="lightgrey")
ax.scatter(good_x, good_y, color="orange")
plt.errorbar(good_x, good_y, yerr=good_err, capsize=3, fmt="none", color="orange")

# Annotate each point with text
for entry in data:
    if entry[2]:
        color = "black"
    else:
        color = "lightgrey"

    if entry[0] == "sqrt3":
        ax.annotate(entry[0], xy=(entry[1], entry[5]), xytext=(-32,-2), textcoords="offset points", color=color)
    elif entry[0] == "sqrt5":
        ax.annotate(entry[0], xy=(entry[1], entry[5]), xytext=(5,-4), textcoords="offset points", color=color)
    elif entry[0] == "sqrt7":
        ax.annotate(entry[0], xy=(entry[1], entry[5]), xytext=(4,-8), textcoords="offset points", color=color)
    elif entry[0] == "sqrt10":
        ax.annotate(entry[0], xy=(entry[1], entry[5]), xytext=(4,0), textcoords="offset points", color=color)
    elif entry[0] == "sqrt13":
        ax.annotate(entry[0], xy=(entry[1], entry[5]), xytext=(4,3), textcoords="offset points", color=color)
    elif entry[0] == "sqrt16":
        ax.annotate(entry[0], xy=(entry[1], entry[5]), xytext=(-35,1), textcoords="offset points", color=color)
    else:
        ax.annotate(entry[0], xy=(entry[1], entry[5]), xytext=(5,-3), textcoords="offset points", color=color)


#ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#       ylim=(0, 8), yticks=np.arange(1, 8))

plt.title("Memory vs speed (the non-slow routines)")
plt.savefig("memory_vs_speed.svg", metadata={'Date': None})
