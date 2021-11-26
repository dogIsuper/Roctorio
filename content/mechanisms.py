from mechanism import Mechanism, RegisterType
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
  self.inventory.push(ResourceStack(1))

RegisterType('roctorio:mechanism:pump:', {'on_init': pump_init, 'on_step': pump_step})
