import random
import itertools
import sys
from moves_parser import MovesParser

def replay(game_board, color, count, timeout, start_at):
    l = MovesParser()
    l.parse()  
    return l.get_move(1, count)    
    