from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from invariants import NoExcept

class IWorld(DisallowInterfaceInstantiation):
  def __init__(self): pass

class GridWorld(IWorld):
  @NoExcept
  def __init__(self, playground):
    IWorld.__init__(self)
    
    self.blocks = [['assets\\tiles\\grass-256-b.png' for j in range(8)] for i in range(8)]
    self.tiles = []
    
    self.playground = playground
    
    self.draw(initial=True)
  
  @NoExcept
  def draw(self, initial=False):
    if initial:
      self.playground.clear_widgets()
      
      self.tiles = []
      for i, row in enumerate(self.blocks):
        self.tiles.append([])
        for j, cell in enumerate(row):
          hex = Factory.Hex()
          hex.px, hex.py = j, i
          self.playground.add_widget(hex)
          self.tiles[-1].append(hex)
    
    for i, row in enumerate(self.blocks):
      for j, cell in enumerate(row):
        self.tiles[i][j].tx_source = cell
