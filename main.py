#!/usr/bin/env python
# [Participating in Game Off 2021]
# Roctorio is game similar to Factorio which uses hexagonal field.
# You control the raccoon that tries to build his base on an unknown planet.
#
# (c) 2021-2022, ProgramCrafter, dogIsuper, KarmaNT, SmartMushroom, JustWannaLive

from kivy.config import Config
Config.set('graphics', 'maxfps', 2000)
Config.set('graphics', 'width', 1500)
Config.set('graphics', 'height', 800)
Config.set('kivy', 'log_level', 'debug')

from kivy.factory import Factory
from kivy.clock import Clock
from kivy.app import App

import time
import os

try:
  import devpatch
except:
  pass

from gameobject import GameObject

class RoctorioGameThread:
  def __init__(self, app):
    self.app = app
    self.pause_level = 0
    
  def start(self):
    Clock.schedule_once(self.update, 0)
  
  def update(self, timer):
    step_start = time.time()
    if not self.pause_level:
      self.app.game.step()
    step_end = time.time()
    
    if not self.pause_level:
      self.app.game.step()
    
    sps = 1.0 / max(step_end - step_start, 0.0001) # simulation steps per second
    
    if sps > 500:
      sps = 100 * (sps // 100)
    elif sps > 100:
      sps = 10 * (sps // 10)
    else:
      sps = 0.5 * (sps // 0.5)
    
    self.app.root.ids.tps_meter.text = 'TPS: %.3f\nSPS: %.3f' % (self.app.tps, sps)
    
    Clock.schedule_once(self.update, 0)
  
  def pause_game(self):
    self.pause_level += 1
    self.app.game.log('Pause level', self.pause_level)
  
  def continue_game(self):
    self.pause_level -= 1
    self.app.game.log('Pause level', self.pause_level)

class RoctorioApp(App):
  def build(self):
    self.root = Factory.GameInterface()
    self.game = GameObject(self)
    
    self.tps = 0.0
    
    self.game_thread = RoctorioGameThread(self)
    self.game_thread.start()
  
  def put_recipes(self, recipes_layout):
    self.game.put_recipes(recipes_layout)
  
  def fillable_button_callback(self, fillable):
    fillable.progress += 1
    
    if fillable.progress >= fillable.needed:
      fillable.progress -= fillable.needed
      
      if fillable.callback:
        fillable.callback(fillable)

if __name__ == '__main__':
  try:
    RoctorioApp().run()
  except:
    __import__('traceback').print_exc()
    input('...')
