import random as rd
from xxlimited import Null
import chess
import chess.engine

pawntable = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20]

bookstable = [
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30]

class AIEngine:
    

    def __init__(self, board: chess.Board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

#### REFACTOR #####
    def evaluate(self):

        # engine = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/14.1/bin/stockfish")
        # result = engine.analyse(self.board, chess.engine.Limit(depth=1, time=0.01))
        # score = result["score"].white()
        # print(score.score())
        # return score.score()

        board = self.board
        if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0
        
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))
        
        material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
        
        pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KING, chess.BLACK)])
    
        eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

        if board.turn:
            return eval
        else:
            return -eval

    def negaMax(self, depth):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if (depth == 0):
            return (self.evaluate(), Null)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1*(self.negaMax(depth - 1)[0])
            if score > bestScore:
                bestScore = score
                bestMove = move
            self.board.pop()
        return bestScore, bestMove

    ### REWRITE #####
    def negaScout(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        # n = beta
        if (depth == 0):
            return (self.evaluate(), Null)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -(self.negaScout(depth - 1, -beta, -alpha)[0])
            # if score > bestScore:
            # if n == beta or depth <= 2:
            #     bestScore = score
            #         # bestMove = move
            # else:
            #     bestScore = -(self.negaScout(depth - 1, -beta, -score)[0])
            #         # bestMove = move
            # if bestScore > alpha:
            #     alpha = bestScore
            # self.board.pop()
            # if alpha >= beta:
            #     return alpha, move
            # n = alpha + 1
            # bestMove = move
            if score > alpha and score < beta:
                alpha = -(self.negaScout(depth - 1, -beta, -score)[0])
            alpha = max(alpha, score)
            if alpha >= beta:
                return (alpha, Null)
            beta = alpha + 1
            if score > bestScore:
                bestScore = score
                bestMove = move
            self.board.pop() 
        return bestScore, bestMove

#### REWRITE #####
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


class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        # while True:
        #     if play not in (self.board.legal_moves):
        #         print("Wrong move, try again")
        #         play = input("Enter your move: ")
        #     else:
        #         break

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