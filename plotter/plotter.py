import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sqrt_n_in_csv_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

def draw_performance_graph(display_order_for_sqrt_n, title, filename):
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
    #figure = plt.gcf()
    #axes = figure.axes
    #print(axes[0])
    plt.title(title)
    plt.gca().set_xlabel("number (0-65535)")
    plt.gca().set_ylabel("cycles")
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
    plt.savefig(filename)

draw_performance_graph([0, 8, 16, 4, 12, 2, 5, 6, 7, 13, 1, 10, 14, 11, 3, 9, 15], "Integer SQRT performance on 6502 (all solutions)", "result_all.svg")
draw_performance_graph([0, 12, 2, 5, 6, 7, 13, 1, 10, 14, 11, 3, 9, 15], "Integer SQRT performance on 6502 (ok solutions)", "result_ok.svg")
draw_performance_graph([0, 3, 9, 15], "Integer SQRT performance on 6502 (table based solutions only)", "result_table_based.svg")

def draw_memory_vs_speed(data, title, filename):
    # check which solutions are 'good'
    for i in range(0, len(data)):
        for j in range(0, len(data)):
            if i == j:
                continue

            # If data[j] beats data[i] in both memory and speed, then data[i] is not good
            if (data[i][1] > data[j][1]) and (data[i][2] > data[j][2]):
                data[i][3] = False

    good_data = filter(lambda e: e[3], data)
    bad_data = filter(lambda e: not e[3], data)

    good_data = list(good_data)
    bad_data = list(bad_data)

    good_x = [cycles for (name,mem,cycles, good) in good_data]
    good_y = [mem for (name,mem,cycles, good) in good_data]
    bad_x = [cycles for (name,mem,cycles, good) in bad_data]
    bad_y = [mem for (name,mem,cycles, good) in bad_data]

    # plot
    fig, ax = plt.subplots(figsize=(10.5, 7))

    plt.gca().set_xlabel("average time taken (cycles)") #, fontweight='bold')
    plt.gca().set_ylabel("memory (bytes)") #, fontweight='bold')

    ax.scatter(bad_x, bad_y, color="gray")
    ax.scatter(good_x, good_y, color="orange")

    # Annotate each point with text
    for entry in data:
        if entry[3]:
            color = "black"
        else:
            color = "gray"

        if entry[0] == "sqrt7":
            ax.annotate(entry[0], xy=(entry[2] + 10, entry[1] - 20), color=color)
        elif entry[0] == "sqrt12":
            ax.annotate(entry[0], xy=(entry[2] - 30, entry[1] + 25), color=color)
        else:
            ax.annotate(entry[0], xy=(entry[2] + 10, entry[1] + 10), color=color)

    #ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
    #       ylim=(0, 8), yticks=np.arange(1, 8))

    plt.title(title)
    plt.savefig(filename)

# Memory vs speed
#
data = [
    # name, memory, ave. cycles, good
    ["sqrt1",   59,  317.7, True],
    ["sqrt2",   73,  846.5, True],
    ["sqrt3",  796,   43.8, True],
    ["sqrt4",   36, 4989.0, True],
    ["sqrt5",   67,  731.0, True],
    ["sqrt6",   55,  522.9, True],
    ["sqrt7",   42,  501.5, True],
    ["sqrt8",   37, 6342.4, True],
    ["sqrt9",  847,   39.8, True],
    ["sqrt10", 168,  227.4, True],
    ["sqrt11", 595,  268.8, True],
    ["sqrt12",  79, 1198.5, True],
    ["sqrt13", 140,  264.4, True],
    ["sqrt14", 205,  194.1, True],
    ["sqrt15", 476,   35.7, True],
    ["sqrt16",  33, 5488.6, True],
]

draw_memory_vs_speed(data, "memory vs speed (all solutions)", "memory_vs_speed_all.svg")
del data[16-1]
del data[8-1]
del data[4-1]
draw_memory_vs_speed(data, "memory vs speed (non-slow solutions)", "memory_vs_speed_ok.svg")
