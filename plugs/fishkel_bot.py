import numpy as np
from numpy.core.shape_base import block

class Model:
    def __init__(self, board, weights):
        self.board = self.gate_keeper(board)
        self.weights = weights
    
    #The last line of defence
    def gate_keeper(self, board):
        new_board = np.zeros((8,8), dtype=np.int32)
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece is not None:
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
        is_queen = abs(self.board[start[0][start[1]]]) == 2
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
        return is_queen
        
    def reverse_move(self, start, end, is_queen):
        temp = self.board[end[0]][end[1]]
        middle = ((start[0]+end[0])//2, (start[1]+end[1])//2)

        if self.is_eat(start,end):
            self.board[middle[0]][middle[1]] = temp
        if is_queen:
            self.board[start[0]][start[1]] = temp * 2
        self.board[start[0]][start[1]] = temp
        self.board[end[0]][end[1]] = None
        
            
    def score(self):
        white_queens = []
        black_queens = []
        white_attacking = []
        black_attacking = []
        black_defending = []
        white_defending = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i,j]
                if piece == -2:
                    white_queens.append(-1)
                elif piece == 2:
                    black_queens.append(1)
                if piece < 0:
                    if i >= 4:
                        white_defending.append(-1)
                    else:
                        white_attacking.append(-1)
                elif piece > 0:
                    if i < 4:
                        black_defending.append(-1)
                    else:
                        black_attacking.append(-1)
        black_score = (len(black_queens) * self.weights[0]) + (len(black_defending) * self.weights[1]) + (len(black_attacking) * self.weights[2])
        white_score = (len(white_queens) * self.weights[0]) + (len(white_defending) * self.weights[1]) + (len(white_attacking) * self.weights[2])
        return black_score - white_score
                    
        
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
                
    def minimax(self, depth, is_maximizing, possible_moves, alpha = float('-inf'), beta = float('inf')):
        if possible_moves == None:
            possible_moves, are_eatings = self.all_possible(is_maximizing)   
        are_eatings = True
        if self.is_terminal(len(possible_moves)):
            return (self.score(), None)

        
        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for move in possible_moves:
                is_queen = self.move(move[0], move[1])
                if are_eatings:
                    possible_for_square = len(self.all_possible_for_square(move[1], True)[0])
                if are_eatings and len(possible_for_square) != 0:
                    score = self.minimax(depth - 1, False, possible_for_square, alpha, beta)[0]
                else:
                    score = self.minimax(depth - 1, True, None, alpha, beta)[0]
                self.reverse_move(move[0], move[1], is_queen)
                if score > best_score:
                    best_score = score
                    best_move = move
                    alpha = score
                    if alpha > beta:
                        break
        else:
            best_score = float('inf')
            best_move = None
            for move in possible_moves:
                is_queen = self.move(move[0], move[1])
                if are_eatings:
                    possible_for_square = len(self.all_possible_for_square(move[1], True)[0])
                if are_eatings and len(possible_for_square) != 0:
                    score = self.minimax(depth - 1, False, possible_for_square, alpha, beta)[0]
                else:
                    score = self.minimax(depth - 1, True, None, alpha, beta)[0]
                self.reverse_move(move[0], move[1], is_queen)
                if score < best_score:
                    best_score = score
                    best_move = move
                    beta = score
                    if alpha > beta:
                        break

        return (best_score, best_move)
        

def fishkel_bot(game_board, color, count, timeout, hungry_piece, weights_arr=[10,5,7]):
    model = Model(game_board, weights_arr)
    if color == 'white':
        move = model.minimax(4, False, None)[1]
    else:
        move = model.minimax(4, True, None)[1]
    return move