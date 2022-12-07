from MctsAgent import get_mcts_move
import chess
import random
import time



class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        self.board.push_san(play)

    def playAIMove(self, iterations=20):

        bestMove = get_mcts_move(self.board.fen(), iterations)
            
        print('BEST MOVE', bestMove)
        self.board.push(bestMove)
        return

    def startGame(self):

        print("The game started!")
        print("You play WHITE!")

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
                self.playAIMove()
                turn = chess.WHITE
                continue
        return

    
if __name__ == '__main__':
    game = GameEngine(chess.Board())
    
    game.startGame()