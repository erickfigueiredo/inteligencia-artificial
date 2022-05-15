# UNIVERSIDADE FEDERAL DE VIÇOSA
# Autor: Erick Lima Figueiredo MA: ES98898
# Disc: Inteligência Artificial
# Professor: Júlio Reis

from os import access
import sys
from random import randint
import math

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.


def rand_goal_y():
    return randint(2800, 4200)


def get_min_distance_by_wizard(d):
    return d[f'distance_{curr}']


def rand_coord():
    return (randint(0, 15878), randint(0, 7409))


def euclidian_distance(s, w):
    return math.sqrt((s[0]-w[0])**2 + (s[1]-w[1])**2)


# Goal direction according team identifier
# Y is in an acceptable range drawn on each call
goal_direction = [
    {'x': 15981, 'y': rand_goal_y},
    {'x': 12, 'y': rand_goal_y}
]

# if 0 you need to score on the right of the map, if 1 you need to score on the left
my_team_id = int(input())
other_team_id = 0 if my_team_id else 1
curr = 0

while True:
    wizards = []  # Saves wizards positions
    opponents = []  # Saves opponents with snaffles positions
    opponents_general = []  # Saves others opponents positions
    accessible_snaffles = []  # Saves available Snaffles

    my_score, my_magic = [int(i) for i in input().split()]
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    entities = int(input())  # number of entities still in game

    for i in range(entities):
        inputs = input().split()

        entity_id = int(inputs[0])  # entity identifier
        # "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        entity_type = inputs[1]

        x = int(inputs[2])  # position
        y = int(inputs[3])  # position

        vx = int(inputs[4])  # velocity
        vy = int(inputs[5])  # velocity

        # 1 if the wizard is holding a Snaffle, 0 otherwise
        state = int(inputs[6])

        if entity_type == 'WIZARD':
            wizards.append(
                {'x': x, 'y': y, 'gotcha': True if state else False})

        if entity_type == 'SNAFFLE' and not state:
            accessible_snaffles.append({'x': x, 'y': y})

        if entity_type == 'OPPONENT_WIZARD':
            if state:
                opponents.append({'x': x, 'y': y})
            else:
                opponents_general.append({'x': x, 'y': y})

    # Calc distance between snaffle and each wizard
    for s in accessible_snaffles:
        s['distance_0'] = euclidian_distance(
            (s['x'], s['y']), (wizards[0]['x'], wizards[0]['y']))

        s['distance_1'] = euclidian_distance(
            (s['x'], s['y']), (wizards[1]['x'], wizards[1]['y']))

    # Calc distance between opponent with snaffle and each wizard
    for op in opponents:
        op['distance_0'] = euclidian_distance(
            (op['x'], op['y']), (wizards[0]['x'], wizards[0]['y']))

        op['distance_1'] = euclidian_distance(
            (op['x'], op['y']), (wizards[1]['x'], wizards[1]['y']))

    # Calc distance between opponent and each wizard
    for op in opponents_general:
        op['distance_0'] = euclidian_distance(
            (op['x'], op['y']), (wizards[0]['x'], wizards[0]['y']))

        op['distance_1'] = euclidian_distance(
            (op['x'], op['y']), (wizards[1]['x'], wizards[1]['y']))

    # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 400)
    # i.e.: "MOVE x y thrust" or "THROW x y power"
    for i in range(2):
        curr = i

        # If Wizard has got a snaffle try to throw to goal
        if wizards[i]['gotcha']:
            print(
                f"THROW {goal_direction[my_team_id]['x']} {goal_direction[my_team_id]['y']()} 500")

        # Else if there are any snaffle go to it
        elif len(accessible_snaffles):
            # Sorting in ascending distance
            if len(accessible_snaffles) > 1:
                accessible_snaffles.sort(key=get_min_distance_by_wizard)

            print(
                f"MOVE {accessible_snaffles[0]['x']} {accessible_snaffles[0]['y']} 150")
            del accessible_snaffles[0]

        # Else if there is an opponent with a snaffle, go to him
        elif len(opponents):
            if len(opponents) > 1:
                opponents.sort(key=get_min_distance_by_wizard)

            print(f"MOVE {opponents[0]['x']} {opponents[0]['y']} 150")
            del opponents[0]

        # Else go to an opponent
        else:
            if len(opponents_general) > 1:
                opponents_general.sort(key=get_min_distance_by_wizard)

            print(
                f"MOVE {opponents_general[0]['x']} {opponents_general[0]['y']} 150")
