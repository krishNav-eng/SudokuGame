import pygame as pg
import time

class GameClock():
  def __init__(self):
    self.clock = pg.time.Clock()
    self.timeElapsed = 0
    self.seconds = 0
    self.minutes = 0
    self.hours = 0
    self.isStart = True

  def start(self):
    print("clock started")
    while True:
      if self.isStart:
        time.sleep(0.9)
        self.timeElapsed += 1
      else:
        break

  def getTimeElapsed(self) -> str:
    self.seconds = self.timeElapsed % 59
    self.minutes = (self.timeElapsed // 60) % 59
    self.hours = (self.timeElapsed // 3600) % 59

    return f"{self.hours}:{self.minutes}:{self.seconds}"
  
  def stop(self):
    print("GameClock stopped!")
    self.isStart = False
