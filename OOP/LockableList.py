# Implement a lockable list class
# you should be able to store values in the list, additionaly
# you should be able to make the list mutable/immutable by calling lock and unlock functions
# implement setting/getting values, multiplying the list
# adding two lists (minding if the lists are locked), and so on

class LockableList():
    def __init__(self, *values, locked=False):
        self.values = list(values)
        self.locked = locked

    def __str__(self):
        return f'{self.values}'
    
    def __repr__(self):
        values = ', '.join([value.__repr__() for value in self.values])
        return f'LockableList({values})'

    def __len__(self):
        return len(self.values)

    def __getitem__(self, i):
        if isinstance(i, int):
            if i < 0:
                i = len(self.values) + i

            if i < 0 or i >= len(self.values):
                raise IndexError('LockableList index out of range')
            else:
                return self.values[i]

        elif isinstance(i, slice):
            start, stop, step = i.indices(len(self.values))
            rng = range(start, stop, step)
            return LockableList(*[self.values[index] for index in rng])
        else:
            invalid_type = type(i)
            raise TypeError(
                'LockableList indices must be integers or slices, not {}'
                .format(invalid_type.__name__)
            )

    def __setitem__(self, i, values):
        if self.locked == True:
            raise RuntimeError(
                'LockableList object does not support item assignment when locked'
            )

        if isinstance(i, int):
            if i < 0:
                i = len(self.values) + i

            if i < 0 or i >= len(self.values):
                raise IndexError('LockableList index out of range')
            else:
                self.values[i] = values

        elif isinstance(i, slice):
            start, stop, step = i.indices(len(self.values))
            rng = range(start, stop, step)
            if step != 1:
                if len(rng) != len(values):
                    raise ValueError(
                        "attempt to assign a sequence of size {} to extended slice of size {}"
                        .format(len(values), len(rng))
                    )

                else:
                    for index, value in zip(rng, values):
                        self.vlaues[index] = value

            else:
                self.values = self.values[:start] + values + self.values[stop:]
        else:
            invalid_type = type(i)
            raise TypeError(
                'LockableList indices must be integers or slices, not {}'
                .format(invalid_type.__name__)
            )
    
    def __add__(self, other):
        if isinstance(other, LockableList):
            return LockableList(*(self.values + other.values))
        
        invalid_type = type(other)
        raise TypeError(
            'can only concatenate list or LockableList (not \'{}\') to LockableList'
            .format(invalid_type.__name__)
        )

    def __iadd__(self, other):
        if self.locked:
            raise RuntimeError(
                'LockedList object does not support in-place concatenation while locked'
            )

        if isinstance(other, LockableList):
            self.values = self.values + other.values
            return self
        
        invalid_type = type(other)
        raise TypeError(
            'can only concatenate list or LockableList (not \'{}\') to LockableList'
            .format(invalid_type.__name__)
        )
        
    def __mul__(self, i):
        if isinstance(i, int):
            return LockableList(*(self.values * i))

        invalid_type = type(i)
        raise TypeError(
            'can\'t multiply LockableList by non-int of type \'{}\''
            .format(invalid_type.__name__)
        )
        
    def __imul__(self, i):
        if self.locked:
            raise RuntimeError(
                'LockedList object does not support in-place multiplication while locked'
            )

        if isinstance(i, int):
            self.values *= i
            return self

        invalid_type = type(i)
        raise TypeError(
            'can\'t multiply LockableList by non-int of type \'{}\''
            .format(invalid_type.__name__)
        )

    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False
    
