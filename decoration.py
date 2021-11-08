from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, SymbolDecorationsPathParser
from invariants import NoExcept

class IDecoration(DisallowInterfaceInstantiation):
  tx_source = ''
  
  def __init__(self, canvas, px, py, side): pass
  def draw(self): pass

class Decoration(IDecoration):
  tx_source = ''
  
  @NoExcept
  def __init__(self, canvas, px, py, side):
    self.side = side
    self.pos = px, py
    self.canvas = canvas
    self.widget = None
  
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Decoration()
      self.widget.px, self.widget.py = self.pos
      self.widget.side = self.side
      self.canvas.add_widget(self.widget)
