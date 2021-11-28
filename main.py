# [Participating in Game Off 2021]
# Roctorio is game similar to Factorio which uses hexagonal field.
# You control the raccoon that tries to build his base on an unknown planet.
#
# (c) 2021, ProgramCrafter, dogIsuper, KarmaNT, SmartMushroom, JustWannaLive

from kivy.config import Config
Config.set('graphics', 'maxfps', 100)
Config.set('graphics', 'width', 1600)
Config.set('graphics', 'height', 1024)

from kivy.factory import Factory
from kivy.clock import Clock
from kivy.app import App

import time
import os

from gameobject import GameObject

class RoctorioGameThread:
  def __init__(self, app):
    self.app = app
    
  def start(self):
    Clock.schedule_once(self.update, 0)
  
  def update(self, timer):
    step_start = time.time()
    self.app.game.step()
    step_end = time.time()
    
    sps = 1.0 / max(step_end - step_start, 0.0001) # simulation steps per second
    
    self.app.root.ids.tps_meter.text = 'TPS: %.3f\nSPS: %.3f' % (self.app.tps, sps)
    
    Clock.schedule_once(self.update, 0)

class RoctorioApp(App):
  def build(self):
    self.root = Factory.GameInterface()
    self.game = GameObject(self)
    
    self.tps = 0.0
    
    self.game_thread = RoctorioGameThread(self)
    self.game_thread.start()

if __name__ == '__main__':
  try:
    RoctorioApp().run()
  except:
    __import__('traceback').print_exc()
    input('...')
