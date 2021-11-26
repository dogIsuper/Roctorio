from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, DivideFrequency
from utils import DecorCoordNormalizer, MechCoordNormalizer
from resource import ResourceStack
from invariants import NoExcept
from inventory import Inventory

DecorationsEnum = {}

class IDecoration(DisallowInterfaceInstantiation):
  tx_source = ''
  on_init = None
  on_step = None
  on_interact = None
  
  def __init__(self, canvas, px, py, side): pass
  def draw(self): pass
  def step(self): pass
  
  def adjacent_tiles(self): pass
  def adjacent_mechs(self): pass

class Decoration(IDecoration):
  tx_source = ''
  
  @NoExcept
  def __init__(self, world, px, py, side):
    *self.pos, self.side = DecorCoordNormalizer.normalize(px, py, side)
    
    self.inventory = None
    
    self.world = world
    self.canvas = world.canvas
    self.widget = None
    
    if self.on_init: self.on_init()
  
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Decoration()
      self.widget.px, self.widget.py = self.pos
      self.widget.side = self.side
      self.canvas.add_widget(self.widget)
    
    self.widget.tx_source = self.tx_source
    if self.inventory: self.inventory.draw()
  
  @NoExcept
  @DivideFrequency(100)
  def log(self, mechs, cells):
    print('Adjacent mechs:', mechs, cells)
  
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
    return DecorCoordNormalizer.adjacent_tiles(*self.pos, self.side)
  
  @NoExcept
  def adjacent_mechs(self):
    return DecorCoordNormalizer.adjacent_mechs(*self.pos, self.side)

@NoExcept
def RegisterType(id, callbacks): # on_init, on_step, on_interact
  return DecorationsEnum.setdefault(id, type(id, (Decoration,), callbacks))

def GetType(id):
  return DecorationsEnum[id]
