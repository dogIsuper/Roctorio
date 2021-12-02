from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, DivideFrequency
from invariants import NoExcept
from world import GridWorld

import content.crafts
import craft

import time

class ITpsMeter(DisallowInterfaceInstantiation):
  def start(self):   pass
  def get_tps(self): pass

class TpsMeter(ITpsMeter):
  @NoExcept
  def start(self):
    self.last_tick = time.time() - 0.001
  
  @NoExcept
  def get_tps(self):
    cur_tick = time.time()
    tps = 1 / max(cur_tick - self.last_tick, 0.001)
    self.last_tick = cur_tick
    
    return tps

class KeyboardController(Widget):
  def __init__(self, player):
    self.widget = player
    
    keyboard = Window.request_keyboard(None, self)
    keyboard.bind(on_key_down=self.key_pressed)
  
  def key_pressed(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'w' and self.widget.pos[0] > 0 and self.widget.pos[1] < 7:
       self.widget.pos = [self.widget.pos[0] - 1, self.widget.pos[1] + 1]
    if keycode[1] == 'e' and self.widget.pos[1] < 7:
      self.widget.pos = [self.widget.pos[0], self.widget.pos[1] + 1]
    if keycode[1] == 'd' and self.widget.pos[0] < 7:
      self.widget.pos = [self.widget.pos[0] + 1, self.widget.pos[1]]
    if keycode[1] == 'x' and self.widget.pos[0] < 7 and self.widget.pos[1] > 0:
      self.widget.pos = [self.widget.pos[0] + 1, self.widget.pos[1] - 1]
    if keycode[1] == 'z' and self.widget.pos[1] > 0:
      self.widget.pos = [self.widget.pos[0], self.widget.pos[1] - 1]
    if keycode[1] == 'a' and self.widget.pos[0] > 0:
      self.widget.pos = [self.widget.pos[0] - 1, self.widget.pos[1]]
    self.widget.draw()

class IGameObject(DisallowInterfaceInstantiation):
  def log(self, message): pass
  def get_world(self):    pass
  def run_forever(self):  pass
  def put_recipes(self, layout): pass

class GameObject(IGameObject):
  @NoExcept
  def __init__(self, app):
    IGameObject.__init__(self)
    
    self.app = app
    self.world = GridWorld(app.root.ids.playground)
    self.init_world()
    
    player = self.world.get_player()
    self.controller = KeyboardController(player)
    
    self.recipes = [
      [1, 2, 5, 7]
    ]
    
    self.tps = TpsMeter()
    self.tps.start()
  
  @NoExcept
  def log(self, *messages):
    message = ' '.join(str(m) for m in messages)
    print('[Roctorio / LOG %s] %s' % (time.strftime('%d-%m-%Y %H:%M:%S'), message))
  
  @NoExcept
  def init_world(self):
    for deco in self.world.decorations:
      for (px, py) in deco.adjacent_tiles():
        self.world.get_block(px, py).tx_source = 'assets\\tiles\\light-grass-256-b.png'
    
    for mech in self.world.mechanisms:
      for (px, py) in mech.adjacent_tiles():
        self.world.get_block(px, py).tx_source = 'assets\\tiles\\desert-256-b.png'
  
  @NoExcept
  def step(self):
    self.app.tps = self.tps.get_tps()
    
    for mech in self.world.mechanisms:
      mech.step()
    
    for deco in self.world.decorations:
      deco.step()
    
    for entity in self.world.entities:
      entity.step()
    
    self.world.draw()
  
  @NoExcept
  def put_recipes(self, layout):
    for recipe in craft.GetCrafts():
      recipe.draw(self, layout)
  
  @NoExcept
  def craft(self, recipe_widget):
    recipe = recipe_widget.host
    recipe.craft(self.world.get_player())
