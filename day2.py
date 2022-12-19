mapping = {
    'A': 'R',
    'B': 'P',
    'C': 'S',
    'X': 'LOSE',
    'Y': 'DRAW',
    'Z': 'WIN',
    'RLOSE': 'S',
    'PLOSE': 'R',
    'SLOSE': 'P',
    'RDRAW': 'R',
    'PDRAW': 'P',
    'SDRAW': 'S',
    'RWIN': 'P',
    'PWIN': 'S',
    'SWIN': 'R',
}

scores = {
    'R': 1,
    'P': 2,
    'S': 3,
    'WIN': 6,
    'LOSE': 0,
    'DRAW': 3
}

outcomes = {
    # win
    'RS': 'LOSE',
    'SP': 'LOSE',
    'PR': 'LOSE',
    'RR': 'DRAW',
    'PP': 'DRAW',
    'SS': 'DRAW',
    'SR': 'WIN',
    'PS': 'WIN',
    'RP': 'WIN'
}


def get_score(outcome):
    outcome_score = scores[outcomes[outcome]]
    choice_score = scores[outcome[1]]

    print("{} Choice score: {}, outcome score: {}".format(outcome, outcome_score, choice_score))
    return outcome_score + choice_score


def get_score_strategy(original_outcome):
    strategy = {
        'R': 'P',
        'P': 'R',
        'S': 'S',
    }

    strategy_outcome = original_outcome[0] + strategy[original_outcome[0]]
    strategy_score = get_score(strategy_outcome)

    return strategy_outcome, strategy_score,


f = open("day2-input.txt", "r")

data = f.read().strip()

games = data.split("\n")

games = ["{}{}".format(mapping[game.split()[0]], mapping[game.split()[1]]) for game in games]
games = [game[0] + mapping[game] for game in games]

game_scores = [
    {
        'OUTCOME': game,
        'SCORE': get_score(game)
    } for game in games
]

total_score = sum([game['SCORE'] for game in game_scores])
print(total_score)
