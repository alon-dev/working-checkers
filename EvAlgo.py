from copy import copy
import numpy as np
from plugs.fishkel_bot import Model
# returns true if bot1 wins bot2, else its false


def algo():
    best_arr = [30,1,2,3,4,5,6,7]
    learning_val = 5
    lerning_curve = 0.8
    for _ in range(5):
        weigths = [best_arr.copy()]
        for i in range(3):
            copy = best_arr.copy()
            copy[i] += learning_val
            weigths.append(copy)
            copy = best_arr.copy()
            copy[i] -=learning_val
            weigths.append(copy)
        for i in weigths:
            best_arr = check_winner(weigths, best_arr)
            print(best_arr + " is winner")
        learning_val *= lerning_curve
    return best_arr

def check_winner(weights1, weights2):
    print(weights1 + " vs " + weights2)
    bot = 1
    model = Model(None, weights1)
    while model.score() < 100000 and model.score() > -100000:
        if bot == 1:
            model.weights = weights1
            move = model.minimax(4, False, None)
        else:
            model.weights = weights2
            move = model.minimax(4, True, None)
        model.make_move(move[0], move[1])
        bot *= -1

    if model.score <= -100000:
        return weights1
    return weights2
print(algo())