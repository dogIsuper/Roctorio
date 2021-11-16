from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from invariants import NoExcept

class IEntity(DisallowInterfaceInstantiation):
  tx_source = ''

  def init(self, world, px, py): pass
  def draw(self):                pass

class Entity(IEntity):
  tx_source = 'assets\\entities\\entity-256.png'

  @NoExcept
  def __init__(self, world, px, py):
    self.pos = px, py
    self.canvas = world.canvas
    self.widget = None

  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Entity()
      self.widget.px, self.widget.py = self.pos
      self.canvas.add_widget(self.widget)
