import random
import itertools
from moves_parser import MovesParser

def replay2(game_board, color, count, timeout, start_at):
    l = MovesParser()
    l.parse()  
    return l.get_move(1, count)    
    