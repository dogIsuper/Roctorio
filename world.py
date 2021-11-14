from utils import DisallowInterfaceInstantiation, DecorCoordNormalizer
from invariants import NoExcept

from decoration import Decoration
from mechanism import Mechanism
from block import Block

class IWorld(DisallowInterfaceInstantiation):
  def __init__(self, playground): pass
  def draw(self):                 pass

class GridWorld(IWorld):
  @NoExcept
  def __init__(self, playground):
    IWorld.__init__(self, playground)
    
    self.blocks = [[Block(playground, j, i) for j in range(8)] for i in range(8)]
    self.decorations = [Decoration(playground, 3, 3, i) for i in range(0, 6, 2)]
    self.mechanisms = [Mechanism(playground, 1, 1, j) for j in range(6)]
    
    self.playground = playground
    
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
  def draw(self):
    for row in self.blocks:
      for block in row:
        block.draw()
    
    for decoration in self.decorations:
      decoration.draw()
    
    for mechanism in self.mechanisms:
      mechanism.draw()
