import math
import os
import importlib
import sys

class Players:
    player1=None
    player2=None
    base1=None
    base2=None
    @staticmethod
    def load(file1, file2):
        Players.base1 = file1
        Players.base2 = file2
        try:
                mod1 = importlib.import_module(Players.base1)
                mod2 = importlib.import_module(Players.base2)
                Players.player1 = getattr(mod1, Players.base1)
                Players.player2 = getattr(mod2, Players.base2)
#                result = method_to_call(5)
        except (RuntimeError, TypeError, NameError,Exception):
                print(NameError) 
                return False
        
        return True


    def find_all(directory):
        sys.path.insert(0, directory)
        counter = 0
        cands = []
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if os.path.isdir(path):
                continue
            cands.append(os.path.splitext(file)[0])
        return cands       
