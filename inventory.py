from kivy.uix.widget import Widget
from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, DivideFrequency
from utils import GameDesignSolutions
from resource import ResourceStack
from invariants import NoExcept

class IInventory(DisallowInterfaceInstantiation):
  def __init__(self, world, host, slots): pass
  def draw(self): pass

class Inventory(IInventory):
  @NoExcept
  def __init__(self, world, host, slots):
    self.stacks = [ResourceStack(0) for i in range(slots)]
    self.canvas = world.canvas
    self.world = world
    self.widget = None
    self.host = host
  
  def extract_stack(self, i):
    return self.stacks[i]
  
  def put_stack(self, i, stack):
    old_stack = self.stacks[i]
    
    if old_stack != stack:
      old_stack.undraw(self.widget)
      self.stacks[i] = stack
  
  def push(self, stack):
    for i in range(len(self.stacks)):
      if stack.size == 0: break
      
      slot, stack = self.extract_stack(i).merge(stack)
      self.put_stack(i, slot)
    
    return stack
  
  def pop(self, max_size, filter_id=''):
    stack = ResourceStack(0)
    
    for i in range(len(self.stacks)):
      slot = self.extract_stack(i)
      if filter_id not in (slot.__class__.__name__, ''):
        continue  # this is safe because .extract_stack() does not change state
      
      stack, slot = slot.split(max_size)
      self.put_stack(i, slot)
      
      max_size -= stack.size
      if not max_size: break
    
    return stack
  
  @NoExcept
  @DivideFrequency(80)
  def debug_print(self, *a, **k):
    print(*a, **k)
  
  @NoExcept
  def draw(self, debug=False):
    # TODO: remove debug prints
    if not self.host:
      if debug:
        self.debug_print(self, 'had no host so could not be drawn')
    
    if not self.widget:
      self.widget = Factory.Inventory()
      self.canvas.add_widget(self.widget)
      
      self.world.notify_inventory(self)
    
    self.widget.host = self.host if isinstance(self.host, Widget) else self.host.widget
    
    # TODO: remove forcing widget position
    # widget.host = ... must work as well, but for some reason doesn't
    self.widget.pos = GameDesignSolutions.inventory_position(self.host)
    
    if debug:
      self.debug_print('selected host', self.widget.host,
                       'pos', self.widget.host.host_pos,
                       'widget pos', self.widget.pos)
    
    for stack in self.stacks:
      stack.draw(self)
    
    self.widget.opacity = GameDesignSolutions.inventory_opacity(self)
  
  @NoExcept
  def pop_resource(self, resource):
    for slot, stack in enumerate(self.stacks):
      if stack == resource:
        self.stacks[slot] = ResourceStack(0)
    return resource
