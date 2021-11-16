from utils import DisallowInterfaceInstantiation, DecorCoordNormalizer, MechCoordNormalizer
from invariants import NoExcept

from decoration import Decoration
from mechanism import Mechanism
from entity import Entity
from block import Block

class IWorld(DisallowInterfaceInstantiation):
  def __init__(self, playground): pass
  def draw(self):                 pass

class GridWorld(IWorld):
  @NoExcept
  def __init__(self, playground):
    IWorld.__init__(self, playground)
    
    self.canvas = playground
    
    self.blocks = [[Block(self, j, i) for j in range(8)] for i in range(8)]
    self.mechanisms = [Mechanism(self, 1, 1, j) for j in range(6)]
    self.decorations = [Decoration(self, 1, i // 2 + 1, i % 2) for i in range(1, 8)]
    
    print(Entity.tx_source)
    self.entities = [Entity(self, 3, 5)]
    
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
      return Block(self.playground, x, y) # caller shall not use .draw method on the returned block
  
  @NoExcept
  def get_deco(self, px, py, side):
    px, py, side = DecorCoordNormalizer.normalize(px, py, side)
    
    for deco in self.decorations:
      if deco.pos == (px, py) and deco.side == side:
        return deco
    
    return None
  
  @NoExcept
  def get_mech(self, px, py, side):
    px, py, side = MechCoordNormalizer.normalize(px, py, side)
    
    for mech in self.mechanisms:
      if mech.pos == (px, py) and mech.side == side:
        return mech
    
    return None
  
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
