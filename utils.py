# from invariants import InvariantFailedError ### cyclic import #

class DisallowInterfaceInstantiation:
  def __init__(self):
    from invariants import InvariantFailedError
    
    class_name = self.__class__.__name__
    if class_name.startswith('I') and class_name[1:2].isupper():
      raise InvariantFailedError('Interface %s cannot be instantiated' % class_name)

class SymbolDecorationsPathParser:
  def parse(path, px=0, py=0):
    for cmd in path:
      if   cmd == 'R': px, py = px + 1, py + 0
      elif cmd == 'l': px, py = px - 1, py + 0
      elif cmd == 'u': px, py = px - 1, py + 1
      elif cmd == 'U': px, py = px + 0, py + 1
      elif cmd == 'd': px, py = px + 0, py - 1
      elif cmd == 'D': px, py = px + 1, py - 1
      
      yield px, py
  
  def coords_to_globals(coords, SIZE):
    # duplicating logic from roctorio.kv
    OFFSET_X = SIZE * 1 / 4 * (3 ** 0.5)
    OFFSET_Y = SIZE * 3 / 4
    
    for (px, py) in coords:
      yield (px * 2 + py) * OFFSET_X, py * OFFSET_Y
  
  def parse_to_globals(path, SIZE, px=0, py=0):
    yield from SymbolDecorationsPathParser.coords_to_globals(SymbolDecorationsPathParser.parse(path, px, py), SIZE)

class MechCoordNormalizer:
  def normalize(px, py, side):
    if side in [0, 1]:
      return px, py, side
    
    if side in [3, 4]:
      return px - 1, py, 4 - side
    
    if side == 2:
      return px, py - 1, 0
    
    if side == 5:
      return px - 1, py + 1, 1
