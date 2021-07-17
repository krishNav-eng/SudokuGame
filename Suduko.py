import pygame
from GameClock import GameClock
from SudukoPuzzleMaker import SudukoPuzzleMaker
import pygame as pg
import threading as t

# Init
pg.init()
pg.font.init()

clock = GameClock()

# Window
WIN_WIDTH, WIN_HEIGHT = 500, 500
window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Suduko")

NUM_SIZE = 30
TIME_BOX_SIZE = 50
GAP_X = window.get_width()// 9
GAP_Y = (window.get_height() - TIME_BOX_SIZE)// 9
BOARD_SIZE = (GAP_X * 9, GAP_Y*9)
OFF_SET_X = GAP_X // 2
OFF_SET_Y = GAP_Y // 2
selectBox_x = 0
selectBox_y = 0

font = pg.font.SysFont('Calibri', NUM_SIZE)

# PuzzleMaker
maker = SudukoPuzzleMaker()
maker.makeBoard()
board = maker.getBoard()
permission = []
GameOn = True
running = True

# Functions
def permissions():
  global permission, board
  permission = [[0 for i in range(9)] for i in range(9)]
  for i in range(9):
    for j in range(9):
      if (board[i][j] == 0):
        permission[i][j] = True
      else:
        permission[i][j] = False    

permissions()

def drawGrid():
  for i in range(10):
    # vertical line
    if (i % 3 == 0):
      pg.draw.line(window, (255, 255, 255), (GAP_X * i, 0),(GAP_X * i, BOARD_SIZE[1]), 3)
      pg.draw.line(window, (255, 255, 255), (0, GAP_Y * i), (BOARD_SIZE[0], GAP_Y * i), 3)
    else:
      pg.draw.line(window, (255, 255, 255), (GAP_X * i, 0),(GAP_X * i, BOARD_SIZE[1]), 1)
      pg.draw.line(window, (255, 255, 255), (0, GAP_Y * i), (BOARD_SIZE[0], GAP_Y * i), 1)

def drawNumber():
  for i in range(9):
    for j in range(9):
      num = board[i][j]
      color = (255, 255, 255)
      if (num != 0):
        if permission[i][j]:
          color = (255,0,255)
        text = font.render(str(num), True, color)
        textRect = text.get_rect()
        textRect.center = (GAP_X * i + OFF_SET_X, GAP_Y * j + OFF_SET_Y)
        window.blit(text, textRect)

def textBox(text:str, x:int, y:int, font:pg.font.SysFont, color):
  render_text = font.render(text, True, color)
  render_text_box = render_text.get_rect()
  render_text_box.center = (x, y)
  window.blit(render_text, render_text_box)
  pg.display.update()

def UpdateTime():
  textBox(clock.getTimeElapsed(), 300, BOARD_SIZE[1] + OFF_SET_Y, font, (255, 255, 255))


def selectBox(pos):
  global selectBox_x, selectBox_y
  mouse_x = pos[0]
  mouse_y = pos[1]
  selectBox_x, selectBox_y = (mouse_x // GAP_X) %9, (mouse_y // GAP_Y)% 9

def highlight_box():
  global selectBox_x, selectBox_y
  x, y = selectBox_x, selectBox_y
  pygame.draw.lines(window, (0,255,0), True, 
  [(GAP_X*x, GAP_Y*y), (GAP_X*x, GAP_Y*(y+1)), 
   (GAP_X*(x+1), GAP_Y*(y+1)), (GAP_X *(x+1), GAP_Y*(y))], 5)

def key_function():
  global GameOn, running,selectBox_x, selectBox_y
  keys = pg.key.get_pressed()
  if permission[selectBox_x][selectBox_y]:
    if keys[pg.K_1]:
      board[selectBox_x][selectBox_y] = 1
    if keys[pg.K_2]:
      board[selectBox_x][selectBox_y] = 2
    if keys[pg.K_3]:
      board[selectBox_x][selectBox_y] = 3
    if keys[pg.K_4]:
      board[selectBox_x][selectBox_y] = 4
    if keys[pg.K_5]:
      board[selectBox_x][selectBox_y] = 5
    if keys[pg.K_6]:
      board[selectBox_x][selectBox_y] = 6
    if keys[pg.K_7]:
      board[selectBox_x][selectBox_y] = 7
    if keys[pg.K_8]:
      board[selectBox_x][selectBox_y] = 8
    if keys[pg.K_9]:
      board[selectBox_x][selectBox_y] = 9
    if keys[pg.K_DELETE]:
      board[selectBox_x][selectBox_y] = 0
  if keys[pg.K_ESCAPE]:
    GameOn = False
    running = False

def repetition(arr):
  for i in range(len(arr)):
    if arr[i] in arr[i+1:]:
      return False

  return True

def check():
  while True:
    # Check row
    for i in range(9):
      if repetition(board[i]):
        print("Check some where wrong!")
    
    for i in range(9):
      if repetition([board[i][j] for j in range(9)]):
        print("Check! some where wrong!")

def highlighting_box():
  while True:
    if (running):
      highlight_box()
    else:
      break


selectionThread = t.Thread(target=highlighting_box)
selectionThread.start()

timeThread = t.Thread(target=clock.start)
timeThread.start()

# checkingThread = t.Thread(target=check)
# checkingThread.start()

while running:
  for e in pg.event.get():
    if e.type == pg.QUIT:
      GameOn = False
      running = False

    if e.type == pg.VIDEORESIZE:
      WIN_WIDTH, WIN_HEIGHT = window.get_width(), window.get_height()
      NUM_SIZE = 30
      TIME_BOX_SIZE = 50
      GAP_X = window.get_width()// 9
      GAP_Y = (window.get_height() - TIME_BOX_SIZE)// 9
      BOARD_SIZE = (GAP_X * 9, GAP_Y*9)
      OFF_SET_X = GAP_X // 2
      OFF_SET_Y = GAP_Y // 2

    if e.type == pg.MOUSEBUTTONDOWN:
      selectBox(pg.mouse.get_pos())
    
    if e.type == pg.KEYDOWN:
      if e.key == pg.K_UP:
        if (selectBox_y > 0): selectBox_y -= 1
      if e.key == pg.K_DOWN:
        if (selectBox_y < 8): selectBox_y += 1
      if e.key == pg.K_RIGHT:
        if (selectBox_x < 8) : selectBox_x += 1
      if e.key == pg.K_LEFT:
        if (selectBox_x > 0): selectBox_x -= 1

  window.fill((0,0,0))

  if GameOn:  
    drawGrid()
    drawNumber()
    key_function()
    UpdateTime()

  pg.display.flip()

pg.quit()
clock.stop()
