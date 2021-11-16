from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from invariants import NoExcept
# from overrided import Override

# resource stacks are immutable
class IResourceStack(DisallowInterfaceInstantiation):
  name = 'null-resource'
  
  def __init__(self, size):   pass
  def merge(self, other):     pass # returns merged stack and any remaining resources
  def split(self, size):      pass # returns stack with up to SIZE resources and other stack with remaining resources
  def draw(self, inv_widget): pass
  def undraw(self, inv_widget): pass

class ResourceStack(IResourceStack):
  name = 'resource'
  limit = 64
  
  @NoExcept
  def __init__(self, size):
    self.size = size
    self.widget = None
    
    if not size: self.name = 'void'
  
  @NoExcept
  def merge(self, other):
    size = min(self.size + other.size, self.limit)
    
    if self.size == self.limit:
      return self, other
    
    return ResourceStack(size), ResourceStack(self.size + other.size - size)
  
  @NoExcept
  def split(self, size):
    size = min(size, self.size)
    return ResourceStack(size), ResourceStack(self.size - size)
  
  @NoExcept
  def draw(self, inv_widget):
    if not self.widget:
      self.widget = Factory.Resource()
      self.widget.q = self.size
      self.widget.id = self.name
    
    if self.widget.parent not in (None, inv_widget):
      self.widget.parent.remove_widget(self.widget)
    
    if self.widget.parent != inv_widget:
      inv_widget.add_widget(self.widget)
  
  @NoExcept
  def undraw(self, inv_widget):
    if self.widget:
      inv_widget.remove_widget(self.widget)
