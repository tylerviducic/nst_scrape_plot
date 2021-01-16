import requests
from bs4 import BeautifulSoup
import constants
import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def get_games():
    url = 'https://www.naturalstattrick.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    games = []
    nst_links = soup.findAll("a")
    for link in nst_links:
        if link.text.count("\n") > 0:
            games.append(link)
    return games


def get_game_page(team):
    for game in get_games():
        if team in game.text and team in constants.teams:
            return game['href']
    print("game not found")
    return None


def get_team_games(team):
    url = 'https://www.naturalstattrick.com/games.php?team={}'.format(constants.endpoint_abreviations[team])
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup.find("table", attrs={'id': 'teams'})


def get_team_game_for_date(team, game_date):  # this method takes a date object as an argument
    game_table = get_team_games(team)
    dates = game_table.find_all("b")
    full_reports = game_table.find_all('a')[1::2]
    for date in dates:
        if date.text.split(' ')[0] == str(game_date):
            return full_reports[dates.index(date)]['href']
    print('Game for {} not found on {}'.format(team, game_date))
    return None


def get_player_stats_from_list(all_stats):
    roster_list = []
    for i in range(len(all_stats) // 40):
        stat_dict = {}
        for j in range(40):
            stat_key = all_stats[(i * 40) + j].string
            try:
                stat_key = float(stat_key)
            except ValueError:
                pass
            stat_dict[constants.player_dict_cats[j]] = stat_key
        roster_list.append(stat_dict)
    return roster_list


def get_on_ice_5v5(team, date=None):
    if not date:
        end_point = get_game_page(team)
    # url = 'http://www.naturalstattrick.com/game.php?season=20192020&game=20513'
    else:
        end_point = get_team_game_for_date(team, date)
    url = 'https://www.naturalstattrick.com/'+end_point
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    team_abv = constants.abreviations[team]

    table = soup.find("table", attrs={'id': "tb" + team_abv + "oi5v5"})
    table_body = table.find("tbody")
    stats = table_body.find_all("td")
    roster_list = get_player_stats_from_list(stats)
    return roster_list


# def split_name_for_label(name):
#     split_name = str.split(name, "\xa0")
#     return split_name[0] + "\n" + split_name[1]
#
#
# def scatter_with_marker(x_data, y_data, marker, zoom=1.0, ax=None):
#     if ax is None:
#         ax=plt.gca()
#     try:
#         image = plt.imread(marker)
#     except TypeError:
#         pass
#     im = OffsetImage(image, zoom=zoom)
#     artists = []
#     x0, y0 = np.atleast_1d(x_data, y_data)
#     for x, y in zip(x0, y0):
#         ab = AnnotationBbox(im, (x, y), xycoords='data', frameon=False)
#         artists.append(ax.add_artist(ab))
#     ax.update_datalim(np.column_stack([x, y]))
#     ax.autoscale()
#     return artists
#
#
# def plot_cf_vs_xg(roster_stat_list):
#
#     my_marker_path = 'New-Jersey-Devils-Logo.png'
#
#     xg_list = []
#     cf_list = []
#     names = []
#
#     for index in range(len(roster_stat_list)):
#         xg_list.append(roster_stat_list[index]["xGF%"])
#         cf_list.append(roster_stat_list[index]["CF%"])
#         names.append(roster_stat_list[index]["Player"])
#     xg = np.array(xg_list)
#     cf = np.array(cf_list)
#
#     fig, ax = plt.subplots(figsize=(10,8))
#     scatter_with_marker(xg_list, cf_list, my_marker_path, ax=ax, zoom=0.02)
#     ax.scatter(xg, cf)
#
#     for i in range(len(xg)):
#         label = names[i]
#         ax.annotate(label, (xg[i], cf[i]), textcoords="offset points", xytext=(0, 12), ha='center')
#
#     plt.xlabel("xGF%")
#     plt.ylabel("CF%")
#     plt.title("Quality vs. Quantity", fontweight="bold", y=1.09)
#
#     ax.axvline(x=50, color='black')
#     ax.axhline(y=50, color='black')
#
#     xmin,xmax = plt.xlim()
#     ymin,ymax = plt.ylim()
#     plt.text(xmin, ymax + 1, 'Just get it to the net?')
#     plt.text(xmax - 17, ymax + 1, 'Sickest player in the world')
#     plt.text(xmin, ymin - 3, 'Terrible, go home')
#     plt.text(xmax - 15, ymin - 3, 'Lemonade from lemons')
#
#     plt.show()
#
#
# def plot_xg_bar(roster_stat_list):
#
#     bar_width = 0.35
#
#     xg_list = []
#     cf_list = []
#     names = []
#     name_labels = []
#     player_numbers = []
#
#     for index in range(len(roster_stat_list)):
#         xg_list.append(roster_stat_list[index]["xGF%"])
#         cf_list.append(roster_stat_list[index]["CF%"])
#         names.append(roster_stat_list[index]["Player"])
#     xg = np.array(xg_list)
#     cf = np.array(cf_list)
#     name_index = np.arange(len(names))
#
#     for name in names:
#         player_numbers.append(constants.player_numbers[name.replace("\xa0", " ")])
#         name_labels.append(split_name_for_label(name))
#
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.bar(name_index, xg - 50, bar_width, label='xG%', align='edge')
#     ax.bar(name_index, cf - 50, -bar_width, label='CF%', align='edge')
#
#     ax.set_ylabel('xG% differential')
#     ax.set_title('xG% differntial for the New Jersey Devils on [Date]')
#     ax.set_xticks(name_index)
#     ax.set_xticklabels(player_numbers)
#     ax.legend()
#
#     fig.tight_layout()
#     plt.show()


# x = get_on_ice_5v5('Devils')
# for i in range(len(x)):
#     print(x[i]["TOI"])
# plot_cf_vs_xg(get_on_ice_5v5('Devils'))
# plot_xg_bar(get_on_ice_5v5('Devils'))
# print("done")


