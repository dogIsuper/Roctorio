from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, DecorCoordNormalizer
from resource import ResourceStack
from invariants import NoExcept
from inventory import Inventory

class IDecoration(DisallowInterfaceInstantiation):
  tx_source = ''
  
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
    
    self.inventory = Inventory(world.canvas, self, 2)
    
    self.world = world
    self.canvas = world.canvas
    self.widget = None
  
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Decoration()
      self.widget.px, self.widget.py = self.pos
      self.widget.side = self.side
      self.canvas.add_widget(self.widget)
    
    self.inventory.draw()
  
  @NoExcept
  def step(self):
    pass
  
  @NoExcept
  def adjacent_tiles(self):
    return DecorCoordNormalizer.adjacent_tiles(*self.pos, self.side)
  
  @NoExcept
  def adjacent_mechs(self):
    return DecorCoordNormalizer.adjacent_mechs(*self.pos, self.side)
