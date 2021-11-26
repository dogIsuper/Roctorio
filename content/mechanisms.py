from mechanism import Mechanism, RegisterType
from utils import MechCoordNormalizer
from resource import ResourceStack
from inventory import Inventory

def barrel_init(self):
  self.tx_source = 'assets\\mechanisms\\barrel-256.png'
  self.inventory = Inventory(self.world.canvas, self, 2)

RegisterType('roctorio:mechanism:barrel:', {'on_init': barrel_init})

#####

def pump_init(self):
  self.tx_source = 'assets\\mechanisms\\pump-256.png'
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
  
  self.inventory.push(ResourceStack(1))

RegisterType('roctorio:mechanism:pump:', {'on_init': pump_init, 'on_step': pump_step})
