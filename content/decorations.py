from decoration import Decoration, RegisterType
from utils import MechCoordNormalizer
from inventory import Inventory

def river_init(self):
  self.tx_source = 'assets/decorations/river-32-132.png'
  self.inventory = Inventory(self.world, self, 0)

RegisterType(
  'roctorio:decoration:water:',
  {'on_init': river_init, 'resource': {
    'tx_source': 'assets/decorations/river-32-132.png'
  }})

#####

def pipe_init(self):
  self.tx_source = 'assets/decorations/copper-pipe-32-132.png'
  self.inventory = Inventory(self.world, self, 2)
  self.move_direction = 1

def pipe_step(self):
  # pulling items
  pull_mech_pos = *self.pos, self.side + self.move_direction
  pull_from = self.world.get_mech(*pull_mech_pos)
  
  if not pull_from:
    for deco_pos in MechCoordNormalizer.adjacent_decos(*pull_mech_pos):
      deco = self.world.get_deco(*deco_pos)
      if deco not in [None, self]:
        pull_from = deco
        break
  
  if pull_from:
    pull_from.push_stack(self.push_stack(pull_from.pop_stack(1)))
  
  # moving items in the pipe
  for i in range(1)[::-1]:
    slot_a = self.inventory.extract_stack(i)
    slot_b = self.inventory.extract_stack(i + 1)
    
    slot_b, slot_a = slot_b.merge(slot_a)
    
    self.inventory.put_stack(i, slot_a)
    self.inventory.put_stack(i + 1, slot_b)
  
  # pushing items
  push_mech_pos = *self.pos, self.side + 1 - self.move_direction
  push_to = self.world.get_mech(*push_mech_pos)
  
  if not push_to:
    for deco_pos in MechCoordNormalizer.adjacent_decos(*push_mech_pos):
      deco = self.world.get_deco(*deco_pos)
      if deco not in [None, self]:
        push_to = deco
        break
  
  if push_to:
    stack = self.inventory.extract_stack(1)
    self.inventory.put_stack(1, push_to.push_stack(stack))

def pipe_interact(self):
  self.move_direction = 1 - self.move_direction
  
  self.widget.r = self.move_direction

RegisterType(
  'roctorio:decoration:pipe:',
  {'on_init': pipe_init, 'on_step': pipe_step, 'on_interact': pipe_interact,
   'resource': {
    'tx_source': 'assets/decorations/copper-pipe-32-132.png'
  }})
