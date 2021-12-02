from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, MechCoordNormalizer
from resource import ResourceStack
from invariants import NoExcept
from inventory import Inventory

import resource

MechanismsEnum = {}

class IMechanism(DisallowInterfaceInstantiation):
  tx_source = ''
  on_init = None
  on_step = None
  on_interact = None
  
  def __init__(self, canvas, px, py, side): pass
  def step(self): pass
  def draw(self): pass
  
  def adjacent_tiles(self): pass
  def adjacent_decos(self): pass

class Mechanism(IMechanism):
  tx_source = 'assets\\mechanisms\\pump-256.png'
  
  @NoExcept
  def __init__(self, world, hex_px, hex_py, side):
    *self.pos, self.side = MechCoordNormalizer.normalize(hex_px, hex_py, side)
    
    self.inventory = Inventory(world.canvas, self, 1)
    
    self.world = world
    self.canvas = world.canvas
    self.widget = None
    
    if self.on_init: self.on_init()
  
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Mechanism()
      self.widget.side = self.side
      self.widget.px, self.widget.py = self.pos
      self.canvas.add_widget(self.widget)
    
    self.widget.tx_source = self.tx_source
    if self.inventory: self.inventory.draw()
  
  @NoExcept
  def step(self):
    if self.on_step: self.on_step()
  
  @NoExcept
  def pop_stack(self, size):
    return self.inventory.pop(size)
  
  @NoExcept
  def push_stack(self, stack):
    return self.inventory.push(stack)
  
  @NoExcept
  def adjacent_tiles(self):
    return MechCoordNormalizer.adjacent_tiles(*self.pos, self.side)
  
  @NoExcept
  def adjacent_decos(self):
    return MechCoordNormalizer.adjacent_decos(*self.pos, self.side)

@NoExcept
def RegisterType(id, callbacks): # on_init, on_step, on_interact
  if 'resource' in callbacks:
    resource.RegisterType(id.replace('mechanism', 'item', 1),
                          callbacks.pop('resource'))
  
  return MechanismsEnum.setdefault(id, type(id, (Mechanism,), callbacks))

def GetType(id):
  return MechanismsEnum[id]
