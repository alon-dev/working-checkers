from datetime import datetime
import time

class Results:
    GAMES = 'results.txt'
    MOVES = 'moves.txt'

    def __init__(self, file):
        self.__file = file

    def append(self, content):
        success_write = False
        while (not success_write):
            try:   
                file_object = open(self.__file, 'a')
                file_object.write(content)
                file_object.close()
                success_write = True
            except: 
                time.sleep(1)
                print(datetime.now().strftime("%H:%M:%S"), 'cant open ' + self.__file + ' file')
                continue

    def read(self):
        success_read = False
        lines = []
        while (not success_read):
            try:   
                file1 = open(self.__file, 'r')
                lines = file1.readlines()
                file1.close()
                success_read = True
            except Exception as e: 
                time.sleep(1)
                print(datetime.now().strftime("%H:%M:%S"), 'cant open ' + self.__file + ' file')
                continue

        return lines