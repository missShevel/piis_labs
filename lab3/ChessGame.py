import random as rd
from xxlimited import Null
import chess

class AIEngine:

    def __init__(self, board: chess.Board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def calculateFigureCost(self, square):
        figureCost = 0
        pieceType = self.board.piece_type_at(square)
        if (pieceType == chess.PAWN):
            figureCost = 1
        if (pieceType == chess.ROOK):
            figureCost = 5.1
        if (pieceType == chess.BISHOP):
            figureCost = 3.33
        if (pieceType == chess.KNIGHT):
            figureCost = 3.2
        if (pieceType == chess.QUEEN):
            figureCost = 8.8

        if (self.board.color_at(square)!=self.color):
            return -figureCost
        return figureCost

    def evaluate(self):
        compt = 0
        #Sums up the material values
        for i in range(64):
            compt+=self.calculateFigureCost(chess.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001*rd.random()
        return compt

    def negaMax(self, depth):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if (depth == 0):
            return (self.evaluate(), Null)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -(self.negaMax(depth - 1)[0])
            if score > bestScore:
                bestScore = score
                bestMove = move
            self.board.pop()
        return bestScore, bestMove
    
    def negaScout(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        n = beta
        if (depth == 0):
            return (self.evaluate(), Null)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -(self.negaScout(depth - 1, -n, -alpha)[0])
            if score > bestScore:
                if n == beta or depth <= 2:
                    bestScore = score
                    bestMove = move
                else:
                    bestScore = -(self.negaScout(depth - 1, -beta, -score)[0])
                    bestMove = move
            if bestScore > alpha:
                alpha = bestScore
            self.board.pop()
            if alpha >= beta:
                return alpha, move
            n = alpha + 1
            bestMove = move
        return bestScore, bestMove

    def pvs(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if (depth == 0):
            return (self.evaluate(), Null)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -(self.pvs(depth - 1, -beta, -alpha)[0])
            self.board.pop()
            if score >= beta:
                return beta, move
            if score > alpha:
                alpha = score
            bestMove = move
            bestScore = score     
        return bestScore, bestMove

    def mateOpportunity(self):
        if (self.board.legal_moves.count()==0):
            if (self.board.turn == self.color):
                return -999
            else:
                return 999
        else:
            return 0

    #to make the engine develop in the first moves
    def openning(self):
        if (self.board.fullmove_number<10):
            if (self.board.turn == self.color):
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0

class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        while True:
            if play not in (self.board.legal_moves):
                print("Wrong move, try again")
                play = input("Enter your move: ")
            else:
                break

        self.board.push_san(play)

    def playAIMove(self, maxDepth, color, method, alpha, beta):
        engine = AIEngine(self.board, maxDepth, color)
        if(method=='negamax'):
            bestMove = engine.negaMax(maxDepth)[1]
        elif(method=='negascout'):
            bestMove = engine.negaScout(maxDepth, alpha, beta)[1]
        else:
            bestMove = engine.pvs(maxDepth, alpha, beta)[1]
            
            
        print('BEST MOVE', bestMove)
        self.board.push(bestMove)
        return

    def startGame(self, method):
        aiColor = chess.BLACK
        print("The game started!")
        print("You play WHITE!")
        maxDepth = 3
        alpha = float('-inf')
        beta = float('inf')
        turn = chess.WHITE
        while (not self.board.is_checkmate()):
            print(self.board)
            if turn == chess.WHITE:
                print('\n\nWhite move\n\n')
                self.playHumanMove()
                turn = chess.BLACK
                continue
            if turn == chess.BLACK:
                print('\n\nBlack move\n\n')
                self.playAIMove(maxDepth, aiColor, method, alpha, beta)
                turn = chess.WHITE
                continue
        return

    

game = GameEngine(chess.Board())
print("Possible methods: negamax, negascout, pvs")
method = input("Choose method: ")
while True:
    if method != "negamax" and method != "negascout" and method != "pvs":
        print("Wrong method, try again")
        method = input("Choose method: ")
    else:
        break
print("You choosed method", method)
game.startGame(method)