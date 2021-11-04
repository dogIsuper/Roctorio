# from invariants import InvariantFailedError ### cyclic import #

class DisallowInterfaceInstantiation:
  def __init__(self):
    from invariants import InvariantFailedError
    
    class_name = self.__class__.__name__
    if class_name.startswith('I') and class_name[1:2].isupper():
      raise InvariantFailedError('Interface %s cannot be instantiated' % class_name)
