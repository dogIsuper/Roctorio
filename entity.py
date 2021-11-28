from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, DivideFrequency
from invariants import NoExcept
from utils import directions

import random

class IEntity(DisallowInterfaceInstantiation):
  tx_source = ''

  def init(self, world, px, py): pass
  def draw(self):                pass
  def local_controlled(self):    pass

class Entity(IEntity):
  tx_source = 'assets\\entities\\entity-256.png'

  @NoExcept
  def __init__(self, world, px, py):
    self.pos = px, py
    self.world = world
    self.canvas = world.canvas
    self.widget = None

  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Entity()
      self.canvas.add_widget(self.widget)
      
    self.widget.px, self.widget.py = self.pos

  @NoExcept
  @DivideFrequency(20)
  def step(self):
    px, py = self.pos
    dx, dy = directions[random.randrange(0, 6)]
    nx, ny = px + dx, py + dy
    
    if self.world.has_block(nx, ny):
      self.pos = nx, ny
  
  @NoExcept
  def local_controlled(self):
    return False

class EntityPlayer(Entity):
  tx_source = 'assets\\entities\\entity-256.png'
  
  @NoExcept
  def step(self):
    pass

  @NoExcept
  def local_controlled(self):
    return True

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
