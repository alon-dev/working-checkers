import numpy as np

class Model:
    def __init__(self, board, depth, weights):
        self.board = self.gate_keeper(board)
        self.depth = depth
        self.weights = weights
    
    #The last line of defence
    def gate_keeper(self, board):
        new_board = np.zeros((8,8), dtype=np.int32)
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece.color == 'white':
                    if piece.isQueen:
                        new_board[i][j] = -2
                    else:
                        new_board[i][j] = -1
                elif piece == 'black':
                    if piece.isQueen:
                        new_board[i][j] = 2
                    else:
                        new_board[i][j] = 1
        return new_board

    def is_eat(self, start, end):
        return abs(start[0] - end[0]) != 1
            
    def make_move(self, start, end):
        temp = self.board[start[0]][start[1]]
        if end[0] == 7 and temp == 1:
            temp = 2
        if end[0] == 0 and temp == -1:
            temp = 3
        if self.is_eat(start,end):
            middle = ((start[0]+end[0])//2, (start[1]+end[1])//2)
            self.board[middle[0]][middle[1]] == None
        
        self.board[end[0]][end[1]] = temp
        self.board[start[0]][start[1]] = None
        
    def reverse_move(self, start, end):
        temp = self.board[end[0]][end[1]]
        middle = ((start[0]+end[0])//2, (start[1]+end[1])//2)

        if self.is_eat(start,end):
            self.board[middle[0]][middle[1]] = temp
        self.board[start[0]][start[1]] = temp
        self.board[end[0]][end[1]] = None
        
            
    def score(self):
        piece
        
    def all_possible_for_square(self, start_square, is_eaten):
        all_possible = []
        dir = 1
        if self.board[start_square[0][start_square[1]]] < 0:
            dir = -1
        for i in [-1, 1]:
            if start_square[0] + i <= 7 and start_square[0] + i >= 0 and start_square[1] + dir <= 7 and start_square[1] + dir >= 0:
                if not is_eaten and self.board[start_square[0] + i][start_square[1] + dir] == 0:
                    all_possible.append((start_square[0] + i, start_square[1] + dir))
                elif self.board[start_square[0] + i][start_square[1] + dir] != self.board[start_square[0][start_square[1]]]:
                    if start_square[0] + i * 2 <= 7 and start_square[0] + i * 2 >= 0 and start_square[1] + dir * 2 <= 7 and start_square[1] + dir * 2 >= 0:
                        if self.board[start_square[0] + i * 2][start_square[1] + dir * 2] == 0:
                            if not is_eaten:
                                is_eaten = True
                                all_possible = []
                            all_possible.append((start_square[0] + i * 2, start_square[1] + dir * 2))
            if abs(self.board[start_square[0][start_square[1]]]) == 2:
                dir *= -1
                if not is_eaten and self.board[start_square[0] + i][start_square[1] + dir] == 0:
                    all_possible.append((start_square[0] + i, start_square[1] + dir))
                elif self.board[start_square[0] + i][start_square[1] + dir] != self.board[start_square[0][start_square[1]]]:
                    if start_square[0] + i * 2 <= 7 and start_square[0] + i * 2 >= 0 and start_square[1] + dir * 2 <= 7 and start_square[1] + dir * 2 >= 0:
                        if self.board[start_square[0] + i * 2][start_square[1] + dir * 2] == 0:
                            if not is_eaten:
                                is_eaten = True
                                all_possible = []
                            all_possible.append((start_square[0] + i * 2, start_square[1] + dir * 2))
                dir *= -1

        return all_possible, is_eaten
                 
            
    def all_possible(self, is_black):
        moves = []
        eatings = []
        if is_black:
            was_eat = False
            for i in range(8):
                for j in range(8):
                    if self.board[i,j] > 0:
                        square_moves = self.all_possible_for_square(self.board[i,j], was_eat)
                        if len(square_moves[0]) > 0:
                            is_eat = square_moves[1]
                            if is_eat:
                                was_eat = is_eat
                                for move in square_moves[0]:
                                    eatings.append(move)
                            else:
                                for move in square_moves[0]:
                                    moves.append(move)
        else:
            was_eat = False
            for i in range(8):
                for j in range(8):
                    if self.board[i,j] < 0:
                        square_moves = self.all_possible_for_square(self.board[i,j], was_eat)
                        if len(square_moves[0]) > 0:
                            is_eat = square_moves[1]
                            if is_eat:
                                was_eat = is_eat
                                for move in square_moves[0]:
                                    eatings.append(move)
                            else:
                                for move in square_moves[0]:
                                    moves.append(move) 
        
        #Evil Laughter
        if len(eatings) > 0:
            return eatings, True
        else:
            return moves, False
            
    def is_terminal(self, length):
        return length == 0
                
    def minimax(self, depth, is_maximizing):
        possible_moves, are_eatings = self.all_possible(is_maximizing)   
        if self.is_terminal(len(possible_moves)):
            return self.score(possible_moves)

        
        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for move in possible_moves:
                self.move(move[0], move[1])
                if len(self.all_possible_for_square(move[0], True)[0]) == 0:
                    score = self.minimax(depth - 1, False)
                else:
                    score = self.minimax(depth - 1, True)

def fishkel_bot(game_board, color, count, timeout, hungry_piece, weights_arr=[10,5,7]):
    model = Model(game_board, 4, weights_arr)
    if color == 'white':
        move = model.minimax(False)
    else:
        move = model.minimax(True)
    return move