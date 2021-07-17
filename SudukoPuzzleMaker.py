import random as rd
from time import time_ns

class SudukoPuzzleMaker:
  def __init__(self):
    self.dim = 9
    self.board = [[0 for _ in range(self.dim)] for _ in range(self.dim)]

  def makeBoard(self):
    st = time_ns()

    for i in range(self.dim):
      for j in range(self.dim):
        num = rd.randint(1, self.dim)
        if num == 0:
          print("0")
          self.board[j][i] = 0

        else :
          if self.possible(i, j, num):
            self.board[i][j] = num

    ft = time_ns()
    tt = ft - st
    print(f"Time taken: {tt}ns || {tt//100}ms")

  def getBoard(self):
    return self.board

  def possible(self, row, col, num):
    for x in range(self.dim):
      if self.board[row][x] == num:
        return False
      if self.board[x][col] == num:
        return False

    k = row//3
    l = col//3
    for x in range(3):
      for y in range(3):
        if self.board[k+x][l+y] == num:
          return False

    return True

  def getSpaceCount(self):
    counter = 0
    for i in range(self.dim):
      for j in range(self.dim):
        if self.board[i][j] == 0:
          counter += 1

    return counter
