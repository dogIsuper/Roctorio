from utils import DisallowInterfaceInstantiation

class IInvariantFailedError(DisallowInterfaceInstantiation): pass
class InvariantFailedError(Exception, IInvariantFailedError): pass

def NoExcept(fn):
  def inner(*a, **k):
    try:
      return fn(*a, **k)
    except Exception as exc:
      raise InvariantFailedError(fn.__qualname__) from exc
  
  inner.__name__ = fn.__name__
  inner.__qualname__ = fn.__qualname__
  
  return inner