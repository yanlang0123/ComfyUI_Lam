class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False
    
class AlwaysTupleZero(tuple):
    def __getitem__(self, i):
        if i<super().__len__():
            return AlwaysEqualProxy(super().__getitem__(i))
        else:
            return AlwaysEqualProxy(super().__getitem__(-1))