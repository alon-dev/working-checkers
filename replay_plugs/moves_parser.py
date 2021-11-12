from results import Results

class MovesParser:

    def parse(self):
        games = []
        result = Results(Results.MOVES)
        lines = result.read()
        current_game = []
        for line in lines:
            line = line.strip()
            if line == "DONE":
                games.append(current_game)
                current_game = []
                continue
            move = line.split(',')
            move_tuple = (int(move[0]),int(move[1]), int(move[2]), int(move[3]))
            current_game.append(move_tuple)
        self.__games = games

    def get_move(self,game, move):
        return self.__games[game][move-1]
