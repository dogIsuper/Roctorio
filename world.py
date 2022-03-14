from utils import DisallowInterfaceInstantiation, DecorCoordNormalizer, MechCoordNormalizer
from invariants import NoExcept

# the following lines will register decoration types and behaviours
import content.decorations
import content.mechanisms
import content.blocks

import resource

from entity import Entity, EntityPlayer
import decoration
import mechanism
import block

class IWorld(DisallowInterfaceInstantiation):
  def __init__(self, playground): pass
  def draw(self):                 pass
  def get_block(self, x, y):      pass
  def has_block(self, x, y):      pass
  def get_deco(self, x, y, side): pass
  def get_mech(self, x, y, side): pass
  
  def notify_inventory(self, pos, size):  pass
  def get_inventory(self, pos):           pass

class GridWorld(IWorld):
  @NoExcept
  def __init__(self, playground):
    IWorld.__init__(self, playground)
    
    self.canvas = playground
    
    River = decoration.GetType('roctorio:decoration:water:')
    Pipe = decoration.GetType('roctorio:decoration:pipe:')
    
    Pump = mechanism.GetType('roctorio:mechanism:drill:')
    Barrel = mechanism.GetType('roctorio:mechanism:barrel:')
    
    Grass = block.GetType('roctorio:block:grass:')
    
    self.blocks = [[Grass(self, j, i) for j in range(8)] for i in range(8)]
    self.mechanisms = [Barrel(self, 1, 1, j) for j in range(1, 6)]
    self.decorations = [Pipe(self, 1, i // 2 + 1, i % 2) for i in range(1, 8)]
    # self.decorations = [Decoration(self, 1, 2, 1)]
    
    self.mechanisms.append(Pump(self, 1, 1, 0))
    self.mechanisms.append(Barrel(self, 1, 4, 0))
    self.decorations.append(River(self, 1, 1, 0))
    self.decorations.extend(Pipe(self, 1, 1, i) for i in range(1, 6))
    
    # assert(self.get_mech(1, 2, 1))
    
    print(Entity.tx_source)
    self.entities = [Entity(self, 3, 5), EntityPlayer(self, 1, 1)]
    
    self.get_player().inventory.push(resource.GetType('roctorio:item:water:')(1))
    
    self.inventories = []
    self.draw()
  
  @NoExcept
  def return_unique_decors_mechs(self, L):
    positions = set()
    unique = []
    
    for item in L:
      if (*item.pos, item.side) in positions: continue
      unique.append(item)
      positions.add((*item.pos, item.side))
    
    return unique
  
  @NoExcept
  def get_block(self, x, y):
    try:
      return self.blocks[y][x]
    except IndexError:
      return Block(self.canvas, x, y) # caller shall not use .draw method on the returned block
  
  @NoExcept
  def has_block(self, x, y):
    return (0 <= y < len(self.blocks)) and (0 <= x < len(self.blocks[y]))
  
  @NoExcept
  def get_entity(self, x, y):
    self.pos = x, y
    for entity in self.entities:
      if tuple(entity.pos) == self.pos:
        return entity
    return None
  
  @NoExcept
  def has_entity(self, x, y):
    return bool(self.get_entity(x, y))
  
  @NoExcept
  def get_deco(self, px, py, side):
    px, py, side = DecorCoordNormalizer.normalize(px, py, side)
    
    for deco in self.decorations:
      if tuple(deco.pos) == (px, py) and deco.side == side:
        return deco
    
    return None
  
  @NoExcept
  def get_mech(self, px, py, side):
    px, py, side = MechCoordNormalizer.normalize(px, py, side)
    
    for mech in self.mechanisms:
      if tuple(mech.pos) == (px, py) and mech.side == side:
        return mech
    
    return None
  
  @NoExcept
  def remove_entity(self, entity):
    self.entities.remove(entity)
    entity.undraw()
  
  @NoExcept
  def draw(self):
    for row in self.blocks:
      for block in row:
        block.draw()
    
    for decoration in self.decorations:
      decoration.draw()
    
    for mechanism in self.mechanisms:
      mechanism.draw()
    
    for entity in self.entities:
      entity.draw()
  
  @NoExcept
  def notify_inventory(self, w):
    self.inventories.append(w)
  
  @NoExcept
  def get_inventory(self, resource):
    for inv in self.inventories[::-1]:
      if inv.widget.collide_widget(resource):
        return inv
    return None
  
  @NoExcept
  def get_player(self):
    for entity in self.entities:
      if entity.local_controlled():
        return entity
    
    return None
