#!/usr/bin/python
# Simple fixed-point numerical class
# $Revision$, $Date$
# RW Penney, December 2006


class FPnum(object):
    fraction_bits = 384
    scale = 1L << fraction_bits
    round = 1L << (fraction_bits - 1)

    def __init__(self, val=0L):
        self.value = long(val * self.scale)

    def SetFraction(self, n_bits=32):
        self.fraction_bits = n_bits
        scale = 1L << n_bits
        round = 1L << (n_bits - 1)

    # unary arithmetic operations:
    def __neg__(self):
        new = FPnum()
        new.value = -self.value
        return new

    # arithmetic comparison tests:
    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __nonzero__(self):
        return (self.value != 0)

    # arithmetic combinations:
    def __add__(self, other):
        new = FPnum()
        new.value = self.value + other.value
        return new

    def __iadd__(self, other):
        self.value += other.value
        return self

    def __sub__(self, other):
        new = FPnum()
        new.value = self.value - other.value
        return new

    def __isub__(self, other):
        self.value -= other.value
        return self

    def __mul__(self, other):
        new = FPnum()
        new.value = (self.value * other.value + self.round) / self.scale
        return new

    def __div__(self, other):
        new = FPnum()
        new.value = (self.value * self.scale + self.round) / other.value
        return new

    # printing/converstion routines:
    def __str__(self):
        val = self.value
        rep = ''
        if self.value < 0:
            rep = '-'
            val *= -1
        whole = val / self.scale
        frac = val - self.scale * whole
        rep += str(whole)
        if frac != 0:
            rep += '.'
            idx = 0
            while idx < (self.fraction_bits / 3) and frac != 0:
                frac *= 10L
                q = frac / self.scale
                rep += str(q)
                frac -= q * self.scale
                idx += 1
        return rep

    # mathematical functions:
    def sqrt(self):
        rt = FPnum(1)
        while True:
            delta = (rt - self / rt) / FPnum(2)
            rt -= delta
            if delta.value == 0: break
        return rt


if __name__ == "__main__":
    q = FPnum(-32)
    for idx in xrange(0,32):
        print q
        q /= FPnum(2)
    rt = FPnum(2).sqrt()
    print rt
    print rt * rt
