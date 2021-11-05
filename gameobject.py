from utils import DisallowInterfaceInstantiation
from invariants import NoExcept
from world import GridWorld

import time

class ITpsMeter(DisallowInterfaceInstantiation):
  def start(self):   pass
  def get_tps(self): pass

class TpsMeter(ITpsMeter):
  def start(self):
    self.last_tick = time.time() - 0.001
  
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
  def __init__(self, app):
    IGameObject.__init__(self)
    
    self.world = GridWorld(app.root.ids.playground)
    self.app = app
    
    self.tps = TpsMeter()
    self.tps.start()
  
  def log(self, *messages):
    message = ' '.join(str(m) for m in messages)
    print('[LOG %s] %s' % (time.strftime('%d-%m-%Y %H:%M:%S'), message))
  
  def step(self):
    self.app.tps = self.tps.get_tps()
    
    self.world.draw(initial=False)
