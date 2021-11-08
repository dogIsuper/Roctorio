from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, MechCoordNormalizer
from invariants import NoExcept

class IMechanism(DisallowInterfaceInstantiation):
  tx_source = ''
  
  def __init__(self, canvas, px, py, side): pass
  def draw(self): pass

class Mechanism(IMechanism):
  tx_source = ''
  
  @NoExcept
  def __init__(self, canvas, hex_px, hex_py, side):
    *self.pos, self.side = MechCoordNormalizer.normalize(hex_px, hex_py, side)
    self.canvas = canvas
    self.widget = None
  
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Mechanism()
      self.widget.side = self.side
      self.widget.px, self.widget.py = self.pos
      self.canvas.add_widget(self.widget)
