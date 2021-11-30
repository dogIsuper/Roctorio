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
  
  def _create_stack(self, id, quantity):
    widget = Factory.Resource()
    widget.q = quantity
    widget.tx_source = resource.GetType(id).tx_source
    return widget
  
  def draw(self, layout):
    if not self.widget:
      self.widget = Factory.CraftingRecipe()
      
      self.widget.add_widget(self._create_stack(*self.result))
      self.widget.add_widget(self._create_stack('roctorio:item:null:', 0))
      
      for id, quantity in self.sources:
        self.widget.add_widget(self._create_stack(id, quantity))
    
    if self.widget.parent not in [None, layout]:
      self.widget.parent.remove_widget(self.widget)
    
    layout.add_widget(self.widget)

def RegisterCraft(sources, result):
  RecipesEnum.append(CraftingRecipe(sources, result))

def GetCrafts():
  return RecipesEnum[:]
