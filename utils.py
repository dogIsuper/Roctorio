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

class TileCoordNormalizer:
  def normalize(px, py):
    return px, py
  
  def adjacent_decos(px, py): # not normalized
    return ((px, py, i) for i in range(6))
  
  def adjacent_mechs(px, py): # not normalized
    return ((px, py, i) for i in range(6))

class DecorCoordNormalizer:
  def normalize(px, py, side):
    if side < 3:
      return px, py, side
    
    if side == 3:
      return px - 1, py, 0
    if side == 4:
      return px - 1, py + 1, 1
    if side == 5:
      return px, py + 1, 2
  
  def adjacent_tiles(px, py, side):
    delta = ((1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1))
    
    return (px, py), (px + delta[side][0], py + delta[side][1])
  
  def adjacent_mechs(px, py, side): # not normalized
    return (px, py, side), (px, py, (side + 1) % 6)

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
  
  def adjacent_tiles(px, py, side):
    px, py, side = MechCoordNormalizer.normalize(px, py, side)
    
    if side == 0:
      return (px, py), (px + 1, py), (px, py + 1)
    else:
      return (px, py), (px + 1, py), (px + 1, py - 1)
  
  def adjacent_decos(px, py, side): # normalized
    px, py, side = MechCoordNormalizer.normalize(px, py, side)
    
    if side == 0:
      return (px, py, 0), (px, py + 1, 2), (px, py + 1, 1)
    else:
      return (px, py, 0), (px, py, 1), (px + 1, py, 2)

class IDecorationPuller(DisallowInterfaceInstantiation):
  def __init__(self, world, px, py, side): pass
  def pull_item(self):                     pass
  def push_item(self):                     pass
  
  def adjacent_decos(self):                pass
  def adjacent_mechs(self):                pass
  def get_variants(self):                  pass
  def sort_variants(self, variants):       pass

class DecorationPuller(IDecorationPuller): pass

def DivideFrequency(divisor, default=None):
  def wrap(fn):
    timer = 0
    
    def wrapper(*a, **k):
      nonlocal timer
      
      timer += 1
      if timer % divisor: return default
      
      return fn(*a, **k)
    
    wrapper.__name__ = fn.__name__
    wrapper.__qualname__ = fn.__qualname__
    
    return wrapper
  
  return wrap
