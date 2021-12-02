from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation
from invariants import NoExcept

import content.resources
import resource

RecipesEnum = []

class ICraftingRecipe(DisallowInterfaceInstantiation):
  def __init__(self, sources, result): pass
  def draw(self, layout):              pass

class CraftingRecipe(ICraftingRecipe):
  def __init__(self, sources, result):
    self.sources = sources
    self.result = result
    self.widget = None
  
  @NoExcept
  def _create_stack(self, id, quantity):
    widget = Factory.Resource()
    widget.q = quantity
    widget.tx_source = resource.GetType(id).tx_source
    return widget
  
  @NoExcept
  def draw(self, game_object, layout):
    if not self.widget:
      self.widget = Factory.CraftingRecipe()
      self.widget.ids.craft_button.callback = game_object.craft
      self.widget.ids.craft_button.host = self
      
      self.widget.add_widget(self._create_stack(*self.result))
      self.widget.add_widget(Factory.CraftResultArrow())
      
      for id, quantity in self.sources:
        self.widget.add_widget(self._create_stack(id, quantity))
    
    if self.widget.parent not in [None, layout]:
      self.widget.parent.remove_widget(self.widget)
    
    layout.add_widget(self.widget)
  
  @NoExcept
  def craft(self, entity):
    stacks = []
    for id, quantity in self.sources:
      stack = entity.inventory.pop(quantity, filter_id=id)
      
      stacks.append(stack)
      if stack.size < quantity: break # not enough resources
    else:
      # got enough resources, crafting
      stack = entity.inventory.push(resource.GetType(self.result[0])(self.result[1]))
      
      if stack.size == 0: return # success
      if stack.size < self.result[1]:
        # some resources were pushed, some were not
        # rolling back the whole craft
        entity.inventory.pop(self.result[1] - stack.size, filter_id=self.result[0])
    
    # rollback - returning resources
    for stack in stacks:
      entity.inventory.push(stack)

def RegisterCraft(sources, result):
  RecipesEnum.append(CraftingRecipe(sources, result))

def GetCrafts():
  return RecipesEnum[:]
