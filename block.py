from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from invariants import NoExcept

import random

BlocksEnum = {}

class IBlock(DisallowInterfaceInstantiation):
  tx_source = ''
  tags = ''
  
  def __init__(self, canvas, px, py): pass
  def draw(self):                     pass
  def has_tag(self, tag):             pass

class Block(IBlock):
  @NoExcept
  def __init__(self, world, px, py):
    self.pos = px, py
    self.canvas = world.canvas
    self.widget = None
    
    if self.has_tag('ground'):
      self.ore = random.randint(256, 1024)
  
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

@NoExcept
def RegisterType(id, callbacks): # on_init, on_step, on_interact
  return BlocksEnum.setdefault(id, type(id, (Block,), callbacks))

def GetType(id):
  return BlocksEnum[id]
