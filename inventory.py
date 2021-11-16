from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from resource import ResourceStack
from invariants import NoExcept

class IInventory(DisallowInterfaceInstantiation):
  def __init__(self, canvas, host, slots): pass
  def draw(self): pass

class Inventory(IInventory):
  @NoExcept
  def __init__(self, canvas, host, slots):
    self.stacks = [ResourceStack(0)] * slots
    self.canvas = canvas
    self.widget = None
    self.host = host
  
  def extract_stack(self, i):
    return self.stacks[i]
  
  def put_stack(self, i, stack):
    old_stack = self.stacks[i]
    
    if old_stack != stack:
      old_stack.undraw(self.widget)
      self.stacks[i] = stack
  
  @NoExcept
  def draw(self):
    if not self.widget and self.host:
      self.widget = Factory.Inventory()
      self.widget.host = self.host.widget
      self.canvas.add_widget(self.widget)
    
    for stack in self.stacks:
      stack.draw(self.widget)
