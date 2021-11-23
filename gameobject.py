from utils import DisallowInterfaceInstantiation
from invariants import NoExcept
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

class IGameObject(DisallowInterfaceInstantiation):
  def log(self, message): pass
  def get_world(self):    pass
  def run_forever(self):  pass

class GameObject(IGameObject):
  @NoExcept
  def __init__(self, app):
    IGameObject.__init__(self)
    
    self.world = GridWorld(app.root.ids.playground)
    self.app = app
    
    self.init_world()
    
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
