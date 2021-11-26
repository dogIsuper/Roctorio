from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from invariants import NoExcept

class IBlock(DisallowInterfaceInstantiation):
  tx_source = ''
  
  def __init__(self, canvas, px, py): pass
  def draw(self):                     pass
  def has_tag(self, tag):             pass

class Block(IBlock):
  tx_source = 'assets\\tiles\\grass-256-b.png'
  
  @NoExcept
  def __init__(self, world, px, py):
    self.pos = px, py
    self.canvas = world.canvas
    self.widget = None
    self.tags = ''
  
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Hex()
      self.widget.px, self.widget.py = self.pos
      self.canvas.add_widget(self.widget)
    
    self.widget.tx_source = self.tx_source
  
  @NoExcept
  def has_tag(self, tag):
    return tag.lower() in self.tags.split(':')
