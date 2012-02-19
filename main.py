import random
import itertools

# Symbols
BRAIN = 1
SHOTGUN = 2
FOOTPRINTS = 3

SYMBOLS = {
    BRAIN: 'Brain',
    SHOTGUN: 'Shotgun',
    FOOTPRINTS: 'Footprints',
}

# Colors
GREEN = 1
YELLOW = 2
RED = 3

COLORS = {
    GREEN: 'Green',
    YELLOW: 'Yellow',
    RED: 'Red',
}

# Faces
GREEN_FACES = tuple([BRAIN] * 3 + [SHOTGUN] * 1 + [FOOTPRINTS] * 2)
YELLOW_FACES = tuple([BRAIN] * 2 + [SHOTGUN] * 2 + [FOOTPRINTS] * 2)
RED_FACES = tuple([BRAIN] * 1 + [SHOTGUN] * 3 + [FOOTPRINTS] * 2)

FACES = {
    GREEN: GREEN_FACES,
    YELLOW: YELLOW_FACES,
    RED: RED_FACES,
}

# Dice
DICE = tuple([GREEN] * 6 + [YELLOW] * 4 + [RED] * 3)

class Data(object):
    pass

def print_rolled_dice(dice):
    result = []
    for color, face in dice:
        result.append('%s %s' % (COLORS[color], SYMBOLS[face]))
    print ', '.join(result)

def do_roll(reroll):
    n = 3 - len(reroll)
    bag = list(DICE)
    for die in reroll:
        bag.remove(die)
    dice = reroll + random.sample(bag, n)
    result = []
    for die in dice:
        face = random.choice(FACES[die])
        result.append((die, face))
    return tuple(result)

def run(players):
    scores = [0] * len(players)
    active = [True] * len(players)
    round = 0
    gen = itertools.cycle(enumerate(players))
    # make a random player go first
    first = random.choice(range(len(players)))
    for _ in range(first):
        gen.next()
    for index, player in gen:
        if index == first:
            round += 1
            max_score = max(scores)
            if max_score >= 13:
                indexes = [i for i, x in enumerate(scores) if x == max_score]
                if len(indexes) == 1:
                    winner = indexes[0]
                    print 'Player %d wins! %s' % (winner + 1, scores)
                    return winner
                else:
                    active = [x and (i in indexes) for i, x in enumerate(active)]
        if not active[index]:
            continue
        roll = 0
        brains = 0
        shotguns = 0
        reroll = []
        while True:
            roll += 1
            print 'Round %d, Player %d, Roll %d' % (round, index + 1, roll)
            dice = do_roll(reroll)
            print_rolled_dice(dice)
            reroll = []
            for color, face in dice:
                if face == BRAIN:
                    brains += 1
                elif face == SHOTGUN:
                    shotguns += 1
                else:
                    reroll.append(color)
            print 'Brains %d, Shotguns %d' % (brains, shotguns)
            data = Data()
            data.round = round
            data.roll = roll
            data.brains = brains
            data.shotguns = shotguns
            data.reroll = tuple(sorted(reroll))
            if shotguns >= 3: # lose round
                print 'Killed by shotguns!'
                break
            elif player(data): # roll again
                print 'Rolling again!'
                continue
            else: # cash out
                print 'Taking %d brains!' % brains
                scores[index] += brains
                break
        print scores
        print

def run_many(players):
    wins = [0] * len(players)
    while True:
        winner = run(players)
        wins[winner] += 1
        print
        print '--> Wins:', wins
        print

def f(data):
    return data.roll < 2

def g(data):
    return data.roll < 2 or data.brains == 0

if __name__ == '__main__':
    run_many([f, g])
