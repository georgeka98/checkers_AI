import random

class checkers:

  def __init__(self, human):

    self.board = [["X","-","X","-","X","-","X","-"],["-","X","-","X","-","X","-","X"],["X","-","X","-","X","-","X","-"],["-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-"],["-","O","-","O","-","O","-","O"],["O","-","O","-","O","-","O","-"],["-","O","-","O","-","O","-","O"]]
    self.human = human
    self.ai = "O" if human == "X" else "X"
    self.players = ["X", "O"]
    self.no_capture_turn = 0
    self.game_end = False

  def print_board(self):

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        print(self.board[len(self.board[row]) - 1 - row][col], end=" ")
      print()
    print()

  def moves_available(self,player):

    # in the future, positions may have the following format: [a, [x,y]]
    # a can have the following values:
    # 1 = move diagnonally
    # 2 = capture
    # 3 = king (moves to 8th rank)
    # 4 = capture & king (moves to 8th rank)
    total_positions = []

    # for X
    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] == "X" and player == "X": # to simplify things - no second jumps are included now.
          if (row + 1 <= len(self.board) - 1): # pawn not on 8th row
            if col-1 >= 0 and self.board[row+1][col-1] == "-": # left diagnonlaly
              total_positions.append([[row,col],[1,[row+1,col-1]]])
              if row + 1 == len(self.board) - 1: # if on 8th row
                total_positions[-1] = [[row,col],[3,[row+1,col-1]]]
            if col+1 <= len(self.board[row]) - 1 and self.board[row+1][col+1] == "-": # right diagnonaly
              total_positions.append([[row,col],[1,[row+1,col+1]]])
              if row + 1 == len(self.board) - 1: # if on 8th row
                total_positions[-1] = [[row,col],[3,[row+1,col+1]]]
          if (row + 2 <= len(self.board) - 1): # examining jumps/capture
            if col-1 >= 0 and self.board[row+1][col-1] == "O": # left diagnonlaly
              if col-2 >= 0 and self.board[row+2][col-2] == "-":
                total_positions.append([[row,col],[2[row+2,col-2]]])
                if row + 2 == len(self.board) - 1: # if on 8th row
                  total_positions[-1] = [[row,col],[4,[row+2,col-2]]]
            if col+1 <= len(self.board[row]) - 1 and self.board[row+1][col+1] == "O": # right diagnonaly
              if col+2 <= len(self.board[row]) - 1 and self.board[row+2][col+2] == "-":
                total_positions.append([[row,col],[2,[row+2,col+2]]])
                if row + 2 == len(self.board) - 1: # if on 8th row
                  total_positions[-1] = [[row,col],[4,[row+2,col+2]]]
        if self.board[row][col] == "O" and player == "O": # to simplify things - no second jumps are included now.
          if (row - 1 >= 0): # pawn not on 8th row
            if col-1 >= 0 and self.board[row-1][col-1] == "-": # left diagnonlaly
              total_positions.append([[row,col],[1,[row-1,col-1]]])
              if row - 1 == 0: # if on 0th row
                total_positions[-1] = [[row,col],[3,[row-1,col-1]]]
            if col+1 <= len(self.board[row]) - 1 and self.board[row-1][col+1] == "-": # right diagnonaly
              total_positions.append([[row,col],[1,[row-1,col+1]]])
              if row - 1 == 0: # if on 0th row
                total_positions[-1] = [[row,col],[3,[row-1,col+1]]]
          if (row - 2 <= len(self.board) - 1): # examining jumps/capture
            if col-1 >= 0 and self.board[row-1][col-1] == "X": # left diagnonlaly
              if col-2 >= 0 and self.board[row-2][col-2] == "-":
                total_positions.append([[row,col],[2,[row-2,col-2]]])
                if row - 2 == 0: # if on 0th row
                  total_positions[-1] = [[row,col],[4,[row-2,col-2]]]
            if col+1 <= len(self.board[row]) - 1 and self.board[row-1][col+1] == "X": # right diagnonaly
              if col+2 <= len(self.board[row]) - 1 and self.board[row-2][col+2] == "-":
                total_positions.append([[row,col],[2,[row-2,col+2]]])
                if row - 2 == 0: # if on 0th row
                  total_positions[-1] = [[row,col],[4,[row-2,col+2]]]

    return total_positions

  def update_board(self, move, player): # update enviroment

    if move[1][0] == 1 or move[1][0] == 3:
      self.board[move[0][0]][move[0][1]] = "-"
      self.board[move[1][1][0]][move[1][1][1]] = player

    if move[1][0] == 2 or move[1][0] == 3:
      self.board[move[0][0]][move[0][1]] = "-"

      if move[0][0] < move[1][1][0]:
        if move[0][1] < move[1][1][1]: # X right
          self.board[move[0][0]+1][move[0][1]+1] = "-"
        if move[0][1] > move[1][1][1]: # X left
          self.board[move[0][0]+1][move[0][1]-1] = "-"
      if move[0][0] > move[1][1][0]:
        if move[0][1] < move[1][1][1]: # O right
          self.board[move[0][0]-1][move[0][1]+1] = "-"
        if move[0][1] > move[1][1][1]: # O left
          self.board[move[0][0]-1][move[0][1]-1] = "-"

      self.board[move[1][1][0]][move[1][1][1]] = player

  def win_check(self, total_positions, player):

    self.game_end = False
    self.player_won = "-"

    if len(total_positions) == 0:
      if player == self.human: # no moves for human
        self.player_won = self.ai
      elif player == self.ai: # no moves for ai
        self.player_won = self.human
      self.game_end = True
      return True # either player X or O has won the game

    return False

  def move_legit(self, available_moves, piece, move_dest):

    move = []
    for i in available_moves:
      if i[0] == piece and i[1][1] == move_dest:
        move = i

    return move

  def ai_play(self):

    available_moves = self.moves_available(self.ai)
    if not self.win_check(available_moves, self.ai): # checking if human player has won - the AI player wont have any available moves

      pos = random.choice(available_moves)
      self.update_board(pos,self.ai)

      self.print_board()
    
  def human_play(self):

    available_moves = self.moves_available(self.human)
    if not self.win_check(available_moves, self.human): # checking if AI player has won - the human player wont have any available moves

      print("choose piece... ")
      row_init = int(input("choose row ... "))
      col_init = int(input("choose col ... "))
      print()
      print("choose where to move it ... ")
      row = int(input("choose row ... "))
      col = int(input("choose col ... "))

      move = self.move_legit(available_moves, [row_init,col_init], [row,col])

      #print(move,available_moves)
      #print(available_moves[0][0] == [row_init,col_init], available_moves[0][1][1] == [row,col], available_moves[0][0], available_moves[0][1][1], [row_init,col_init], [row,col])

      if move != []:
        self.update_board(move, self.human)
      
      self.print_board()

  def play(self):

    if self.human == "X":

      self.human_play()

      if self.game_end:
        return 0

      self.ai_play()

    else:
      self.ai_play()

      if self.game_end:
        return 0

      self.human_play()

    self.play()






game = checkers("X")
game.print_board()
game.play()