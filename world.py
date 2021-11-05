from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from invariants import NoExcept

class IWorld(DisallowInterfaceInstantiation):
  def __init__(self): pass

class GridWorld(IWorld):
  @NoExcept
  def __init__(self, playground):
    IWorld.__init__(self)
    
    colors = [(1.0, 0.2, 1.0, 1),
              (1.0, 0.2, 0.6, 1),
              (1.0, 0.2, 0.2, 1),
              (1.0, 0.4, 0.2, 1),
              (1.0, 0.6, 0.2, 1)]
    
    self.blocks = [[colors[(i + j) % 5] for j in range(8)] for i in range(8)]
    self.playground = playground
    
    self.draw(initial=True)
  
  @NoExcept
  def draw(self, initial=False):
    if initial:
      self.playground.clear_widgets()
      
      for i, row in enumerate(self.blocks):
        for j, cell in enumerate(row):
          hex = Factory.Hex()
          hex.px, hex.py = j, i
          hex.color = cell
          self.playground.add_widget(hex)
