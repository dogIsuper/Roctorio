from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, MechCoordNormalizer
from resource import ResourceStack
from invariants import NoExcept
from inventory import Inventory

class IMechanism(DisallowInterfaceInstantiation):
  tx_source = ''
  
  def __init__(self, canvas, px, py, side): pass
  def step(self): pass
  def draw(self): pass

class Mechanism(IMechanism):
  tx_source = ''
  
  @NoExcept
  def __init__(self, canvas, hex_px, hex_py, side):
    *self.pos, self.side = MechCoordNormalizer.normalize(hex_px, hex_py, side)
    
    self.inventory = Inventory(canvas, self, 1)
    
    self.canvas = canvas
    self.widget = None
  
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Mechanism()
      self.widget.side = self.side
      self.widget.px, self.widget.py = self.pos
      self.canvas.add_widget(self.widget)
    
    self.inventory.draw()
  
  @NoExcept
  def step(self):
    old_water = self.inventory.extract_stack(0)
    new_water = ResourceStack(1)
    
    sum_water, _ = ResourceStack.merge(old_water, new_water)
    self.inventory.put_stack(0, sum_water)
  
  @NoExcept
  def adjacent_tiles(self):
    return MechCoordNormalizer.adjacent_tiles(*self.pos, self.side)
  
  @NoExcept
  def adjacent_decos(self):
    return MechCoordNormalizer.adjacent_decos(*self.pos, self.side)
