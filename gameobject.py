from utils import DisallowInterfaceInstantiation
from invariants import NoExcept
from kivy.uix.widget import Widget
from kivy.core.window import Window
from world import GridWorld

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

class EntityPlayerRun(Widget):
  def __init__(self, wd):
    self.widget = None
  
  def keyPressed(self, keyboard, keycode, text, modifiers):
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

class GameObject(IGameObject):
  @NoExcept
  def __init__(self, app):
    IGameObject.__init__(self)
    
    self.world = GridWorld(app.root.ids.playground)
    def CreateTest():
      test = EntityPlayerRun(None)
      TestKeyboard = Window.request_keyboard(None, test)
      TestKeyboard.bind(on_key_down=test.keyPressed)
      return test
    test = CreateTest()
    self.app = app
    
    self.init_world()
    player = self.world.get_player()
    test.widget = player
    self.tps = TpsMeter()
    self.tps.start()
  
  @NoExcept
  def log(self, *messages):
    message = ' '.join(str(m) for m in messages)
    print('[LOG %s] %s' % (time.strftime('%d-%m-%Y %H:%M:%S'), message))
  
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
