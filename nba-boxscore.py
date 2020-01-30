#!/usr/bin/env python3

import pickle
from datetime import date, timedelta
from sportsreference.nba.boxscore import Boxscores
import os

script_dir = os.path.dirname(__file__)
path_index = os.path.join(script_dir, 'lastIndex.pickle')
path_games = os.path.join(script_dir, 'games.pickle')
t_day = date.today()


def latest_box_score(day_minus=0):
    day = date.today() - timedelta(days=day_minus)
    score = Boxscores(day)
    values = score.games.values()
    for v in values:
        if len(v) == 0:
            return latest_box_score(day_minus + 1)
    return {date.today(): score}


try:
    with open(path_index, 'rb') as handle:
        game_index = pickle.load(handle)
except FileNotFoundError:
    game_index = -1
try:
    with open(path_games, 'rb') as handle:
        games_cached = pickle.load(handle)
        if list(games_cached.keys())[0] != t_day:  # if not pulled today try get latest game
            games_cached = latest_box_score(0)
            game_index = -1
except FileNotFoundError:
    games_cached = latest_box_score(0)

for date in games_cached.get(t_day).games:
    index = game_index + 1
    value = games_cached.get(t_day).games[date]
    if len(value) == 0:
        print('NBA BOXSCORE')
        break
    if index >= len(value):
        index = 0  # go back
    game = value[index]
    if game['winning_name'] == game['home_name']:  # check winning team
        home_color = '%{F#ECEFF4}'
        away_color = '%{F#2E3440}'
    else:
        home_color = '%{F#2E3440}'
        away_color = '%{F#ECEFF4}'
    output = '%s | %s%s%s %s%s%s - %s%s%s %s%s%s' % (date,
                                                     home_color, game['home_name'], '%{F-}',
                                                     home_color, game['home_score'], '%{F-}',
                                                     away_color, game['away_score'], '%{F-}',
                                                     away_color, game['away_name'], '%{F-}')
    # save last index
    with open(path_index, 'wb') as handle:
        pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(path_games, 'wb') as handle:
        pickle.dump(games_cached, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(output)
