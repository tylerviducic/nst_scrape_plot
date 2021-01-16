import nst_scraper
import constants
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import datetime
import os

todays_date = datetime.date.today()
directory = constants.plot_directory + '{}/'.format(todays_date)
if not os.path.exists(directory):
    os.makedirs(directory)
else:
    print("directory " + directory + " exists")


def split_name_for_label(name):
    split_name = str.split(name, "\xa0")
    return split_name[0] + "\n" + split_name[1]


def scatter_with_marker(xData, yData, marker, zoom=1.0, ax=None):
    my_image = ''
    if ax is None:
        ax = plt.gca()
    try:
        my_image = plt.imread(marker)
    except TypeError:
        pass
    im = OffsetImage(my_image, zoom=zoom)
    artists = []
    x0, y0 = np.atleast_1d(xData, yData)
    for x, y in zip(x0, y0):
        ab = AnnotationBbox(im, (x, y), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists


def plot_cf_vs_xg(roster_stat_list):
    my_marker_path = 'New-Jersey-Devils-Logo.png'

    xg_list = []
    cf_list = []
    names = []

    for index in range(len(roster_stat_list)):
        xg_list.append(roster_stat_list[index]["xGF%"])
        cf_list.append(roster_stat_list[index]["CF%"])
        names.append(roster_stat_list[index]["Player"])
    xg = np.array(xg_list)
    cf = np.array(cf_list)

    fig, ax = plt.subplots(figsize=(10, 8))
    scatter_with_marker(xg_list, cf_list, my_marker_path, ax=ax, zoom=0.02)
    ax.scatter(xg, cf)

    for i in range(len(xg)):
        label = names[i]
        ax.annotate(label, (xg[i], cf[i]), textcoords="offset points", xytext=(0, 12), ha='center')

    plt.xlabel("xGF%")
    plt.ylabel("CF%")
    plt.title("Quality vs. Quantity", fontweight="bold", y=1.09)

    ax.axvline(x=50, color='black')
    ax.axhline(y=50, color='black')

    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    plt.text(xmin, ymax + 1, 'Just get it to the net?')
    plt.text(xmax - 17, ymax + 1, 'Sickest player in the world')
    plt.text(xmin, ymin - 3, 'Terrible, go home')
    plt.text(xmax - 15, ymin - 3, 'Lemonade from lemons')

    plt.savefig(directory + 'xGvsCFPercentages.png')


def plot_xg_bar(roster_stat_list):
    bar_width = 0.45

    xg_list = []
    cf_list = []
    names = []
    name_labels = []
    player_numbers = []

    for index in range(len(roster_stat_list)):
        xg_list.append(roster_stat_list[index]["xGF%"])
        cf_list.append(roster_stat_list[index]["CF%"])
        names.append(roster_stat_list[index]["Player"])
    xg = np.array(xg_list)
    cf = np.array(cf_list)
    name_index = np.arange(len(names))

    for name in names:
        player_numbers.append(constants.player_numbers[name.replace("\xa0", " ")])
        name_labels.append(split_name_for_label(name))

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(name_index, xg - 50, bar_width, label='xG%', align='edge')
    ax.bar(name_index, cf - 50, -bar_width, label='CF%', align='edge')

    ax.set_ylabel('xG% differential')
    ax.set_title('xG% differential for the New Jersey Devils on [Date]')
    ax.set_xticks(name_index)
    ax.set_xticklabels(player_numbers)
    ax.legend()

    fig.tight_layout()
    plt.savefig(directory + 'xGandCFPercentageDifferential.png')


def get_names(roster_stat_list):
    names = []
    for index in range(len(roster_stat_list)):
        names.append(roster_stat_list[index]["Player"])
    return names


def get_per_60(stat_array, toi_array):
    stat_list = []
    for i in range(len(stat_array)):
        stat_list.append(stat_array[i] * 60 / toi_array[i])
    return np.array(stat_list)


def plot_xg_per_60(roster_stat_list):
    bar_width = 0.75

    xg_list = []
    toi_list = []
    names = get_names(roster_stat_list)
    name_labels = []
    player_numbers = []

    for index in range(len(roster_stat_list)):
        xg_list.append(roster_stat_list[index]["xGF"])
        toi_list.append(roster_stat_list[index]["TOI"])
    xg = np.array(xg_list)
    name_index = np.arange(len(names))
    toi = np.array(toi_list)

    for name in names:
        player_numbers.append(constants.player_numbers[name.replace("\xa0", " ")])
        name_labels.append(split_name_for_label(name))

    xg60 = get_per_60(xg, toi)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(name_index, xg60, bar_width, label='xG/60')

    ax.set_ylabel('xG per 60 minutes')
    ax.set_title('xG per 60 minutes for the New Jersey Devils on [Date]')
    ax.set_xticks(name_index)
    ax.set_xticklabels(player_numbers)
    ax.legend()

    fig.tight_layout()
    plt.savefig(directory + 'xGper60.png')


def plot_cf_per_60(roster_stat_list):
    bar_width = 0.75

    cf_list = []
    toi_list = []
    names = get_names(roster_stat_list)
    name_labels = []
    player_numbers = []

    for index in range(len(roster_stat_list)):
        cf_list.append(roster_stat_list[index]["CF"])
        toi_list.append(roster_stat_list[index]["TOI"])
    cf = np.array(cf_list)
    name_index = np.arange(len(names))
    toi = np.array(toi_list)

    for name in names:
        player_numbers.append(constants.player_numbers[name.replace("\xa0", " ")])
        name_labels.append(split_name_for_label(name))

    cf60 = get_per_60(cf, toi)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(name_index, cf60, bar_width, label='CF/60')

    ax.set_ylabel('CF per 60 minutes')
    ax.set_title('CF per 60 minutes for the New Jersey Devils on [Date]')
    ax.set_xticks(name_index)
    ax.set_xticklabels(player_numbers)
    ax.legend()

    fig.tight_layout()
    plt.savefig(directory + 'CFper60.png')


def plot_xg_per_ff(roster_stat_list):
    bar_width = 0.75
    xg_per_ff_list = []
    player_numbers = []
    name_labels = []
    names = get_names(roster_stat_list)
    for index in range(len(roster_stat_list)):
        xg_per_ff_list.append(roster_stat_list[index]["xGF"] / roster_stat_list[index]["FF"])

    xg_per_ff = np.array(xg_per_ff_list)
    name_index = np.arange(len(names))

    for name in names:
        player_numbers.append(constants.player_numbers[name.replace("\xa0", " ")])
        name_labels.append(split_name_for_label(name))

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(name_index, xg_per_ff, bar_width, label='xG/FF')

    ax.set_ylabel('xG per unblocked shot attempt')
    ax.set_title('xG per unblocked shot attempt for the New Jersey Devils on [Date]')
    ax.set_xticks(name_index)
    ax.set_xticklabels(player_numbers)
    ax.legend()

    fig.tight_layout()
    plt.savefig(directory + 'xGPerFenwick.png')


def plot_shots(roster_stat_list):
    bar_width = 0.75
    player_numbers = []
    name_labels = []
    names = get_names(roster_stat_list)
    shot_list = []

    for index in range(len(roster_stat_list)):
        shot_list.append(roster_stat_list[index]["SF"])

    for name in names:
        player_numbers.append(constants.player_numbers[name.replace("\xa0", " ")])
        name_labels.append(split_name_for_label(name))

    name_index = np.arange(len(names))
    shots = np.array(shot_list)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(name_index, shots, bar_width, label='Team Shots')

    ax.set_ylabel('Shots while player is on ice')
    ax.set_title('Team Shots for the New Jersey Devils on [Date] when Player is on Ice')
    ax.set_xticks(name_index)
    ax.set_xticklabels(player_numbers)
    ax.legend()

    fig.tight_layout()
    plt.savefig(directory + 'shots.png')


def plot_toi(roster_stat_list):
    bar_width = 0.75
    player_numbers = []
    name_labels = []
    names = get_names(roster_stat_list)
    toi_list = []

    for index in range(len(roster_stat_list)):
        toi_list.append(roster_stat_list[index]["TOI"])

    for name in names:
        player_numbers.append(constants.player_numbers[name.replace("\xa0", " ")])
        name_labels.append(split_name_for_label(name))

    name_index = np.arange(len(names))
    toi = np.array(toi_list)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(name_index, toi, bar_width, label='TOI')

    ax.set_ylabel('TOI (minutes)')
    ax.set_title('TOI in minutes for the New Jersey Devils on [Date]')
    ax.set_xticks(name_index)
    ax.set_xticklabels(player_numbers)
    ax.legend()

    fig.tight_layout()
    plt.savefig(directory + 'toi.png')


# get_on_ice_5v5('Devils')
scraped_game = nst_scraper.get_on_ice_5v5('Devils')
plot_cf_vs_xg(scraped_game)
plot_xg_bar(scraped_game)
plot_xg_per_60(scraped_game)
plot_cf_per_60(scraped_game)
plot_xg_per_ff(scraped_game)
plot_shots(scraped_game)
plot_toi(scraped_game)


