from decoration import Decoration, RegisterType
from inventory import Inventory

def river_init(self):
  self.tx_source = 'assets\\decorations\\river-32-132.png'
  self.inventory = None

RegisterType('roctorio:decoration:water:', {'on_init': river_init})

#####

def pipe_init(self):
  self.tx_source = 'assets\\decorations\\copper-pipe-16-76.png'
  self.inventory = Inventory(self.world.canvas, self, 2)

def pipe_step(self):
  for i in range(1)[::-1]:
    slot_a = self.inventory.extract_stack(i)
    slot_b = self.inventory.extract_stack(i + 1)
    
    slot_b, slot_a = slot_b.merge(slot_a)
    
    self.inventory.put_stack(i, slot_a)
    self.inventory.put_stack(i + 1, slot_b)
  
  self.puller.pull_item()

RegisterType('roctorio:decoration:pipe:', {'on_init': pipe_init, 'on_step': pipe_step})