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
