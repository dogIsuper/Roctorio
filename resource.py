from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from invariants import NoExcept

ResourcesEnum = {}

# resource stacks are immutable
class IResourceStack(DisallowInterfaceInstantiation):
  tx_source = 'assets\\resources\\water-256.png'
  id        = ''
  tags      = ''
  limit     = 64
  
  def __init__(self, size):   pass
  def merge(self, other):     pass # returns merged stack and any remaining resources
  def split(self, size):      pass
    # returns stack with up to SIZE resources and other stack with remaining resources
  def draw(self, inv_widget): pass
  def undraw(self, inv_widget): pass
  def has_tag(self, tag):     pass

class ResourceStack(IResourceStack):
  @NoExcept
  def __init__(self, size):
    self.size = size
    self.widget = None
  
  @NoExcept
  def merge(self, other):
    if self.size == 0:  return other, self
    if other.size == 0: return self, other
    
    if self.__class__.__name__ != other.__class__.__name__:
      return self, other
    
    size = min(self.size + other.size, self.limit)
    
    if self.size == self.limit:
      return self, other
    
    return self.__class__(size), self.__class__(self.size + other.size - size)
  
  @NoExcept
  def split(self, size):
    if self.size <= size:
      return self, ResourceStack(0)
    
    return self.__class__(size), self.__class__(self.size - size)
  
  @NoExcept
  def draw(self, inv_widget):
    if not self.widget:
      self.widget = Factory.Resource()
      self.widget.q = self.size
      self.widget.tx_source = self.tx_source
    
    if self.widget.parent not in (None, inv_widget):
      self.widget.parent.remove_widget(self.widget)
    
    if self.widget.parent != inv_widget:
      inv_widget.add_widget(self.widget)
  
  @NoExcept
  def undraw(self, inv_widget):
    if self.widget:
      inv_widget.remove_widget(self.widget)
  
  @NoExcept
  def has_tag(self, tag):
    return tag.lower() in self.tags.split(':')

@NoExcept
def RegisterType(id, callbacks): # tx_source, limit
  return ResourcesEnum.setdefault(id, type(id, (ResourceStack,), callbacks))

def GetType(id):
  return ResourcesEnum[id]
