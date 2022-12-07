import chess
import np

root = None

class MctsNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.board = chess.Board(state)
        self.parent_action = parent_action
        self.children = []
        self.parent = parent

        if self.parent and self.parent.board.turn == chess.BLACK:
            self.board.turn = chess.WHITE
        else:
            self.board.turn = chess.BLACK

        self._num_visits = 0
        self._num_wins = 0
        self._num_losses = 0
        self._available_actions = self.get_available_actions()

    def get_q(self):
        #q value for ucb - reward from a node
        return self._num_wins - self._num_losses

    def get_n(self):
       #n value for ucb - number of visits in node
        return self._num_visits

    def expand(self):
        action = self._available_actions.pop()
        new_state = self.move(action)
        child = MctsNode(new_state, parent=self, parent_action=action)
        self.children.append(child)
        return child

    def select(self):
        curr_node = self
        while not curr_node.is_leaf_node():
            if len(curr_node._available_actions) == 0:
                curr_node = curr_node.best_child()
            else:
                return curr_node.expand()
        return curr_node


    def simulate(self):
        curr_node = self

        while not curr_node.is_game_over():
            possible_moves = curr_node.get_available_actions()
            selected_move = np.random.randint(len(possible_moves))
            new_board = curr_node.move(possible_moves[selected_move])
            curr_node = MctsNode(state=new_board, parent=curr_node, parent_action=selected_move)
        return curr_node.get_game_result()

    def backpropagate(self, game_result):
        if game_result == 1:
            self._num_wins += 1
        elif game_result == -1:
            self._num_losses += 1
        self._num_visits += 1
        if self.parent != None:
            self.parent.backpropagate(game_result)

    def is_leaf_node(self):
        return self.is_game_over()


    def best_child(self, C=0.1):
        values = [ (child.get_q() / child.get_n()) + C * np.sqrt((2 * np.log(self.get_n()) / child.get_n())) for child in self.children ] 
        best_child = np.argmax(values)
        return self.children[best_child]
  

    def is_game_over(self):
        game_result = (self.board.is_checkmate() 
                        or self.board.is_stalemate() 
                        or self.board.is_seventyfive_moves() 
                        or self.board.is_fivefold_repetition() 
                        or self.board.is_insufficient_material())
        return game_result


    def get_available_actions(self):
        return list(self.board.legal_moves)


    def move(self, action): # board state after move
            next_state = self.board.copy()
            next_state.push(action)
            return next_state.fen()


    def get_game_result(self):   
        if self.board.outcome().winner == chess.WHITE:
            res = -1
        elif self.board.outcome().winner == chess.BLACK:
            res = 1
        elif self.board.outcome().winner == None:
            res = 0
        return res


    def get_best_move(self, num_iter): # perform best move from the state
        for i in range(int(num_iter)):
            node = self.select()
            result = node.simulate()
            node.backpropagate(result)
        return self.best_child(C=0.0).parent_action


def get_mcts_move(root_state, iterations):
    global root
    root = MctsNode(state=root_state)
    if root.is_game_over():
        return root
    return root.get_best_move(iterations)


