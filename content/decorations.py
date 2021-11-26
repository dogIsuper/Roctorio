from decoration import Decoration, RegisterType

def river_init(self):
  self.tx_source = 'assets\\decorations\\river-32-132.png'

RegisterType('roctorio:decoration:water:', {'on_init': river_init})

#####

def pipe_init(self):
  self.tx_source = 'assets\\decorations\\copper-pipe-16-76.png'

RegisterType('roctorio:decoration:pipe:', {'on_init': pipe_init})