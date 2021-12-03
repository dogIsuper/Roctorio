import content.resources

from mechanism import Mechanism, RegisterType
from utils import MechCoordNormalizer
from inventory import Inventory

import resource
import random

def barrel_init(self):
  self.tx_source = 'assets/mechanisms/barrel-256.png'
  self.inventory = Inventory(self.world.canvas, self, 4)

RegisterType(
  'roctorio:mechanism:barrel:',
  {'on_init': barrel_init, 'resource': {
    'tx_source': 'assets/mechanisms/barrel-256.png'
  }})

#####

def pump_init(self):
  self.tx_source = 'assets/mechanisms/pump-256.png'
  self.inventory = Inventory(self.world.canvas, self, 1)

def pump_step(self):
  # searching oceans and lakes
  for tile in MechCoordNormalizer.adjacent_tiles(*self.pos, self.side):
    if self.world.get_block(*tile).has_tag('water'):
      break
  else:
    # searching rivers
    for deco_pos in MechCoordNormalizer.adjacent_decos(*self.pos, self.side):
      deco = self.world.get_deco(*deco_pos)
      if deco and 'river' in deco.tx_source:
        break
    else:
      return # no water found nearby
  
  Water = resource.GetType('roctorio:item:water:')
  self.inventory.push(Water(1))

RegisterType(
  'roctorio:mechanism:pump:',
  {'on_init': pump_init, 'on_step': pump_step, 'resource': {
    'tx_source': 'assets/mechanisms/pump-256.png'
  }})

#####



def drill_init(self):
  self.tx_source = 'assets/mechanisms/drill-256.png'
  self.inventory = Inventory(self.world.canvas, self, 1)

def drill_step(self):
  # searching tile with ore
  max_ore_tile = None
  
  for tile in MechCoordNormalizer.adjacent_tiles(*self.pos, self.side):
    block = self.world.get_block(*tile)
    if block.has_tag('ground'):
      if not max_ore_tile or max_ore_tile.ore < block.ore:
        max_ore_tile = block
  
  if not max_ore_tile: return
  
  ore_amount = max_ore_tile.ore
  
  prob = 1
  if ore_amount < 256: prob = 0.9
  if ore_amount < 128: prob = 0.8
  if ore_amount < 64:  prob = 0.7
  if ore_amount < 32:  prob = 0.6
  if ore_amount < 16:  prob = 0.5
  if ore_amount < 8:   prob = 0.4
  if ore_amount < 4:   prob = 0.2
  if ore_amount < 2:   prob = 0.1
  
  if random.random() < prob:
    Ore = resource.GetType('roctorio:item:ore:')
    self.inventory.push(Ore(1))
    
    max_ore_tile.ore = max(ore_amount - 1, 0)

RegisterType(
  'roctorio:mechanism:drill:',
  {'on_init': drill_init, 'on_step': drill_step, 'resource': {
    'tx_source': 'assets/mechanisms/drill-256.png'
  }})
