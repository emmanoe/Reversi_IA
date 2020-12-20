# -*- coding: utf-8 -*-

import time
import Reversi
import numpy
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._nbMovesPlayed = 0
        self.WeightMap = numpy.array([[ 500,-150,  30,  10,   8,   8,  10,  30,-150, 500],
                                        [-150,-250,   0,   0,   0,   0,   0,   0,-250,-150],
                                        [  30,   0,   1,   2,   2,   2,   2,   1,   0,  30],
                                        [  10,   0,   2,  10,  12,  12,  10,   2,   0,  10],
                                        [   8,   0,   2,  12,  30,  30,  12,   2,   0,   8],
                                        [   8,   0,   2,  12,  30,  30,  12,   2,   0,   8],
                                        [  10,   0,   2,  10,  12,  12,  10,   2,   0,  10],
                                        [  30,   0,   1,   2,   2,   2,   2,   1,   0,  30],
                                        [-150,-250,   0,   0,   0,   0,   0,   0,-250,-150],
                                        [ 500,-150,  30,  10,   8,   8,  10,  30,-150, 500]])
        (Min,Max) = self.getIntervall(self.WeightMap)
        self._MinMapWeight = Min
        self._MaxMapWeight = Max

    def getPlayerName(self):
        return "my Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            #print("Referee told me to play but the game is over!")
            return (-1, -1)

        self._nbMovesPlayed+=1

        if self._nbMovesPlayed  == 13 :

            WeightMap2 = numpy.array([[   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                    [   0,   0,   0,   4,   4,   4,   4,   0,   0,   0],
                                    [   0,   0,   0,   4,  14,  14,   4,   0,   0,   0],
                                    [   0,   0,   0,   4,  14,  14,   4,   0,   0,   0],
                                    [   0,   0,   0,   4,   4,   4,   4,   0,   0,   0],
                                    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                                    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]])

            (Min,Max) = self.getIntervall(WeightMap2)

            self._MinMapWeight = Min
            self._MaxMapWeight = Max

            self.WeightMap = self.WeightMap-WeightMap2

        if self._nbMovesPlayed < 12 :
            moment = 1
            depth = 6
        elif self._nbMovesPlayed > 85 :
            moment = 3
            depth = 10
        else :
            moment = 2
            depth = 4
        
        [value,move] = self.maxValue(-9999,9999,0,depth,[],moment)

        self._board.push(move)
        #print("I am playing ", move)
        (c, x, y) = move
        assert (c == self._mycolor)

        #update the WeightMap
        if x == 0 and y == 0:
            self.WeightMap[0][1] = 300
            self.WeightMap[0][2] = 150
            self.WeightMap[0][3] = 80
            self.WeightMap[0][4] = 30
            self.WeightMap[1][0] = 300
            self.WeightMap[2][0] = 150
            self.WeightMap[3][0] = 80
            self.WeightMap[4][0] = 30
        if x == 9 and y == 9:
            self.WeightMap[9][8] = 300
            self.WeightMap[9][7] = 150
            self.WeightMap[9][6] = 80
            self.WeightMap[9][5] = 30
            self.WeightMap[8][9] = 300
            self.WeightMap[7][9] = 150
            self.WeightMap[6][9] = 80
            self.WeightMap[5][9] = 30
        if x == 0 and y == 9:
            self.WeightMap[0][8] = 300
            self.WeightMap[0][7] = 150
            self.WeightMap[0][6] = 80
            self.WeightMap[0][5] = 30
            self.WeightMap[1][9] = 300
            self.WeightMap[2][9] = 150
            self.WeightMap[3][9] = 80
            self.WeightMap[4][9] = 30
        if x == 9 and y == 0:
            self.WeightMap[9][1] = 300
            self.WeightMap[9][2] = 150
            self.WeightMap[9][3] = 80
            self.WeightMap[9][4] = 30
            self.WeightMap[8][0] = 300
            self.WeightMap[7][0] = 150
            self.WeightMap[6][0] = 80
            self.WeightMap[5][0] = 30

        #print("My current board :")
        #print(self._board)
        return (x, y)

    def playOpponentMove(self, x, y):
        assert (self._board.is_valid_move(self._opponent, x, y))
        #print("Opponent played ", (x, y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def maxValue(self,alpha,beta,depth,depthMax,bestMove,moment):
        if depth == depthMax or self._board.is_game_over() == True:
            return [self.evaluate(moment),bestMove]

        moves = self._board.legal_moves()

        if depth == 0:
            for move in self._board.legal_moves():
                [player,x,y] = move
                if (x == 0 and y == 0) or (x == 9 and y == 9) or (x == 0 and y == 9) or (x == 9 and y == 0):
                    return [0,move]              

        for move in moves:
            self._board.push(move)
            if depth == 0:
                bestMove = move
            [value,bestMove_] = self.minValue(alpha,beta,depth+1,depthMax,bestMove,moment)
            if alpha<value:
                alpha = value
                bestMove = bestMove_
            self._board.pop()
            if alpha >= beta:
                return [beta,bestMove]
        return [alpha,bestMove]

    def minValue(self,alpha,beta,depth,depthMax,bestMove,moment):
        if depth == depthMax:
            return [self.evaluate(moment),bestMove]
            
        for move in self._board.legal_moves():
            self._board.push(move)
            if depth == 0:
                bestMove = move
            [value,bestMove_] = self.maxValue(alpha,beta,depth+1,depthMax,bestMove,moment)
            if beta>value:
                beta = value
                bestMove = bestMove_
            self._board.pop()
            if alpha >= beta:
                return [alpha,bestMove]
        return [beta,bestMove]
    
    def getMovesBlackAndWhite(self):
        backup = self._board._nextPlayer
        self._board._nextPlayer = self._opponent
        opponentMoves = self._board.legal_moves()
        self._board._nextPlayer = self._mycolor
        myMoves = self._board.legal_moves()
        self._board._nextPlayer = backup
        return [myMoves,opponentMoves]

    # compare total weight of opponent pieces and mine 
    def evaluateCurrentPiecesWeight(self):
        myPiecesWeight = 0
        opponentPiecesWeight = 0
        for x in range(0,self._board._boardsize):
            for y in range(0,self._board._boardsize):
                if self._board._board[x][y] == self._mycolor :
                    myPiecesWeight += self.WeightMap[x][y]
                else:
                    opponentPiecesWeight += self.WeightMap[x][y]
        return [myPiecesWeight,opponentPiecesWeight]

    # the total weight of a set of moves
    def getMovesWeight(self,moves):
        sumW = 0
        for i in range (len(moves)):
            [player,x,y] = moves[i]
            sumW += self.WeightMap[x][y]
        return sumW

    def evaluateMobility(self):
        [myMoves,opponentMoves] = self.getMovesBlackAndWhite()
        opponentMovesWeight = self.getMovesWeight(opponentMoves)
        myMovesWeight = self.getMovesWeight(myMoves)
        return [myMovesWeight,opponentMovesWeight]
    
    def getIntervall(self,map):
        maxM = 0
        minM = 0
        for i in range (10):
            for j in range (10):
                val = map[i][j]
                if val<0:
                    minM += val
                else :
                    maxM += val
        return minM,maxM

    def normalizeValue(self,value,Min,Max):
        return 2*((value-Min)/(Max-Min))-1

    def evaluate(self,moment):
        if moment == 1:
            moves = self._board.legal_moves()
            if self._board._nextPlayer == self._opponent:
                val = self.getMovesWeight(moves)
                return self.normalizeValue(val,self._MinMapWeight,self._MinMapWeight)
            else:
                val = len(moves)
                return self.normalizeValue(val,1,20) 

        if moment == 2:
            moves = self._board.legal_moves()
            mobility = len(moves)
            mobility = self.normalizeValue(mobility,1,20)
            position = self.getMovesWeight(moves)
            position = self.normalizeValue(position,self._MinMapWeight,self._MinMapWeight)
            return mobility+10*position

        if moment == 3:
            (black,white) = self._board.get_nb_pieces()
            if self._opponent == self._board._BLACK:
                return white-black
            else:
                return black-white