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

  @NoExcept
  def step(self):
    import random
    
    x=random.randrange(1, 8)
    
    px,py = self.pos
    
    if x == 1 and 8 > px - 1 >= 0 and 0 <= py + 1 < 8:
      self.pos = (px - 1, py + 1)
    elif x == 2 and 0 <= py + 1 < 8:
      self.pos = (px, py + 1)
    elif x == 3 and 8 > px + 1 >= 0:
      self.pos = (px + 1, py)
    elif x == 4 and 8 > px + 1 >= 0 and 0 <= py - 1 < 8:
      self.pos = (px + 1, py - 1)
    elif x == 5 and 0 <= py - 1 < 8:
      self.pos = (px, py - 1)
    elif x == 6 and 8 > px - 1 >= 0:
      self.pos = (px - 1, py)
      
    self.widget.px, self.widget.py = self.pos
class IEntityHP(DisallowInterfaceInstantiation):
  def init(self, world, px, py): pass
  def draw(self):                pass
  
class EntityHP(IEntityHP):

  @NoExcept
  def __init__(self, world, px, py):
    self.pos = px, py
    self.canvas = world.canvas
    self.widget = None
    
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.EntHP()
      self.widget.px, self.widget.py = self.pos
      self.canvas.add_widget(self.widget)
