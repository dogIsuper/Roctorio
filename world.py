from utils import DisallowInterfaceInstantiation
from invariants import NoExcept

from block import Block

class IWorld(DisallowInterfaceInstantiation):
  def __init__(self, playground): pass
  def draw(self):                 pass

class GridWorld(IWorld):
  @NoExcept
  def __init__(self, playground):
    IWorld.__init__(self, playground)
    
    self.blocks = [[Block(playground, j, i) for j in range(8)] for i in range(8)]
    
    self.playground = playground
    
    self.draw()
  
  @NoExcept
  def draw(self):
    for row in self.blocks:
      for block in row:
        block.draw()