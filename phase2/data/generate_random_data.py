import os
import csv
import random

OUTPUT_DIR  = "output"
DICT_DIR    = "dicts"

ADJECTIVE_DICT  = os.path.join(DICT_DIR,"adjectives.txt")
ARENAS_DICT     = os.path.join(DICT_DIR,"arenas.txt")
NAMES_DICT      = os.path.join(DICT_DIR,"names.txt")
NOUNS_DICT      = os.path.join(DICT_DIR,"nouns.txt")

NUM_TEAMS   = 500
NUM_VENUES  = 100

NUM_PLAYERS_SMALL   = 100000
NUM_PLAYERS_MEDIUM  = 150000
NUM_PLAYERS_LARGE   = 250000

NUM_GAMES_SMALL     = 150000
NUM_GAMES_MEDIUM    = 250000
NUM_GAMES_LARGE     = 300000

NUM_PLAYS_SMALL     = 250000
NUM_PLAYS_MEDIUM    = 300000
NUM_PLAYS_LARGE     = 350000

MIN_TOUCHDOWNS = 0
MAX_TOUCHDOWNS = 1000

MIN_TOTALYARDS = -1000
MAX_TOTALYARDS = 10000

MIN_SALARY = 10000
MAX_SALARY = 60000000

MIN_ATTENDANCE = 0
MAX_ATTENDANCE = 500000

MIN_REVENUE = 0
MAX_REVENUE = 10000000

POSITIONS   = ['QB', 'RB', 'WR']
RESULTS     = ['W', 'L', 'T']

MIN_GAMES_PER_PLAYER = 3
MAX_GAMES_PER_PLAYER = 20

def list_from_file(path):
    ls = []
    with open(path, "r") as f:
        ls = [line.rstrip() for line in f]
    return ls

adjectives  = list_from_file(ADJECTIVE_DICT)
arenas      = list_from_file(ARENAS_DICT)
nouns       = list_from_file(NOUNS_DICT)
names       = list_from_file(NAMES_DICT)

def random_team_name():
    return random.choice(adjectives)+' '+random.choice(nouns)

def random_name():
    return random.choice(names)+' '+random.choice(names)

def random_venue():
    return random.choice(adjectives)+' '+random.choice(nouns)+' '+random.choice(arenas)

def random_date():
    return str(random.randint(1970,2018))+'-'+str(random.randint(0,12))+'-'+str(random.randint(1,28))

teams   = [random_team_name()   for x in range(NUM_TEAMS) ]
venues  = [random_venue()       for x in range(NUM_VENUES)]

def random_player(index):
    return [
        random_name(),
        index,
        random.choice(teams),
        random.choice(POSITIONS),
        random.randint(MIN_TOUCHDOWNS, MAX_TOUCHDOWNS),
        random.randint(MIN_TOTALYARDS, MAX_TOTALYARDS),
        random.randint(MIN_SALARY, MAX_SALARY)
    ]

def random_game(index):
    return [
        index,
        random_date(),
        random.choice(venues),
        random.choice(RESULTS),
        random.randint(MIN_ATTENDANCE, MAX_ATTENDANCE),
        random.randint(MIN_REVENUE, MAX_REVENUE)
    ]

players_small   = [random_player(x) for x in range(NUM_PLAYERS_SMALL) ]
players_medium  = [random_player(x) for x in range(NUM_PLAYERS_MEDIUM)]
players_large   = [random_player(x) for x in range(NUM_PLAYERS_LARGE) ]

games_small     = [random_game(x) for x in range(NUM_GAMES_SMALL) ]
games_medium    = [random_game(x) for x in range(NUM_GAMES_MEDIUM)]
games_large     = [random_game(x) for x in range(NUM_GAMES_LARGE) ]

def random_play(player_list, game_list):
    return [random.choice(player_list)[1], random.choice(game_list)[0]]

def random_plays(player_list, game_list, num_rows):
    plays = []
    used_playerids = []
    while len(plays) < num_rows:
        randplayerid = random.choice(player_list)[1]
        while randplayerid in used_playerids:
            randplayerid = random.choice(player_list)[1]
        used_playerids.append(randplayerid)
        
        num_games = random.randint(MIN_GAMES_PER_PLAYER, MAX_GAMES_PER_PLAYER)
        gameids = []
        for _ in range(num_games):
            randgameid = random.choice(game_list)[0]
            while randgameid in gameids:
                randgameid = random.choice(game_list)[0]
            gameids.append(randgameid)
        for gameid in gameids:
            plays.append([randplayerid,gameid])
            if len(plays) == num_rows:
                break
    return plays

plays_small     = random_plays(players_small,   games_small,    NUM_PLAYS_SMALL)
plays_medium    = random_plays(players_medium,  games_medium,   NUM_PLAYS_MEDIUM)
plays_large     = random_plays(players_large,   games_large,    NUM_PLAYS_LARGE)

with open(os.path.join(OUTPUT_DIR,"players_small.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(players_small)

with open(os.path.join(OUTPUT_DIR,"players_medium.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(players_medium)

with open(os.path.join(OUTPUT_DIR,"players_large.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(players_large)

with open(os.path.join(OUTPUT_DIR,"games_small.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(games_small)

with open(os.path.join(OUTPUT_DIR,"games_medium.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(games_medium)

with open(os.path.join(OUTPUT_DIR,"games_large.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(games_large)

with open(os.path.join(OUTPUT_DIR,"plays_small.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(plays_small)

with open(os.path.join(OUTPUT_DIR,"plays_medium.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(plays_medium)

with open(os.path.join(OUTPUT_DIR,"plays_large.csv"), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(plays_large)