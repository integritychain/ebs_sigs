# Tower Fields for Fq1/2/6/12
import copy
from collections import namedtuple

simple_invert = True  # watch out: terrible perf and need to set max recursion to just over 381 * 12

class Fq1:

    X = -0xd201000000010000
    PRIME = (X - 1) ** 2 * (X ** 4 - X ** 2 + 1) // 3 + X

    def __pow__(self, power):  # supports all Fq*
        if not isinstance(power, int): return NotImplemented
        if power == 0: return self.const(1)
        if power == 1: return self
        if power % 2 == 0:
            return (self * self) ** (power // 2)
        return (self * self) ** (power // 2) * self

    def __init__(self, q):
        if not isinstance(q, int): raise ValueError
        self.q = q % self.PRIME

    def __repr__(self):
        return "{}".format(self.q)

    def __add__(self, other):
        if isinstance(other, Fq1): return Fq1(self.q + other.q)
        return NotImplemented

    def __sub__(self, other):
        if type(other) is Fq1: return Fq1(self.q - other.q)
        if isinstance(other, Fq12):
            return   Fq12(Fq6(Fq2(Fq1(-other.q1.q2.q1.q), Fq1(- other.q1.q2.q0.q)),
                              Fq2(Fq1(-other.q1.q1.q1.q), Fq1(- other.q1.q1.q0.q)),
                              Fq2(Fq1(-other.q1.q0.q1.q), Fq1(- other.q1.q0.q0.q))),
                          Fq6(Fq2(Fq1(-other.q0.q2.q1.q), Fq1(- other.q0.q2.q0.q)),
                              Fq2(Fq1(-other.q0.q1.q1.q), Fq1(- other.q0.q1.q0.q)),
                              Fq2(Fq1(-other.q0.q0.q1.q), Fq1(self.q - other.q0.q0.q0.q))))

        return NotImplemented

    def __mul__(self, other):
        if type(other) is Fq1: return Fq1(self.q * other.q)
        if isinstance(other, Fq12):
            return   Fq12(Fq6(Fq2(Fq1(self.q * other.q1.q2.q1.q), Fq1(self.q * other.q1.q2.q0.q)),
                              Fq2(Fq1(self.q * other.q1.q1.q1.q), Fq1(self.q * other.q1.q1.q0.q)),
                              Fq2(Fq1(self.q * other.q1.q0.q1.q), Fq1(self.q * other.q1.q0.q0.q))),
                          Fq6(Fq2(Fq1(self.q * other.q0.q2.q1.q), Fq1(self.q * other.q0.q2.q0.q)),
                              Fq2(Fq1(self.q * other.q0.q1.q1.q), Fq1(self.q * other.q0.q1.q0.q)),
                              Fq2(Fq1(self.q * other.q0.q0.q1.q), Fq1(self.q * other.q0.q0.q0.q))))
        return NotImplemented

    def __invert__(self):
        return self**(self.PRIME - 2)  # Simple invert via __pow__
        # Faster invert would use euclidean algorithm (to be written)

    def __floordiv__(self, other):
        if isinstance(other, Fq1): return self * ~other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Fq1): return self.q == other.q
        return NotImplemented

    @classmethod
    def const(cls, q):
        return Fq1(q)


# Fp2 is constructed with Fp1(u) / (u^2 - β) where β = -1.
class Fq2(Fq1):

    # noinspection PyMissingConstructor
    def __init__(self, q1, q0):
        if not isinstance(q1, Fq1) or not isinstance(q0, Fq1): raise ValueError
        self.q1 = q1
        self.q0 = q0

    def __repr__(self):
        return "{}u {}".format(self.q1, self.q0)

    def __add__(self, other):
        if isinstance(other, Fq2): return Fq2(self.q1 + other.q1, self.q0 + other.q0)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Fq2): return Fq2(self.q1 - other.q1, self.q0 - other.q0)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Fq2): return Fq2(self.q1 * other.q0 + self.q0 * other.q1,
                                              self.q0 * other.q0 - self.q1 * other.q1)
        return NotImplemented

    def __invert__(self):
        if simple_invert: return self ** ((self.PRIME**2)-2)
        factor = ~(self.q1 * self.q1 + self.q0 * self.q0)
        return Fq2(Fq1(-1) * self.q1 * factor, self.q0 * factor)

    def __floordiv__(self, other):  # Unnecessary as Fq is sufficient
        if isinstance(other, Fq2): return self * ~other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Fq2): return self.q1 == other.q1 and self.q0 == other.q0
        return NotImplemented

    def mul_nonres(self):
        return Fq2(self.q1 + self.q0, self.q0 - self.q1)

    @classmethod
    def const(cls, q):
        return Fq2(Fq1(0), Fq1(q))


# Fp6 is constructed with Fp2(v) / (v^3 - ξ) where ξ = u + 1
class Fq6(Fq1):

    # noinspection PyMissingConstructor
    def __init__(self, q2, q1, q0):
        if not isinstance(q2, Fq2) or not isinstance(q1, Fq2) or not isinstance(q0, Fq2): raise ValueError
        self.q2 = q2
        self.q1 = q1
        self.q0 = q0

    def __repr__(self):
        return "{}v^2 {}v {}".format(self.q2, self.q1, self.q0)

    def __add__(self, other):
        if isinstance(other, Fq6): return Fq6(self.q2 + other.q2, self.q1 + other.q1, self.q0 + other.q0)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Fq6): return Fq6(self.q2 - other.q2, self.q1 - other.q1, self.q0 - other.q0)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Fq6):
            t0 = self.q0 * other.q0
            t1 = self.q0 * other.q1 + self.q1 * other.q0
            t2 = self.q0 * other.q2 + self.q1 * other.q1 + self.q2 * other.q0
            t3 = (self.q1 * other.q2 + self.q2 * other.q1).mul_nonres()
            t4 = (self.q2 * other.q2).mul_nonres()
            return Fq6(t2, t1 + t4, t0 + t3)
        return NotImplemented

    def __invert__(self):
        if simple_invert: return self ** ((self.PRIME**6)-2)
        v0 = self.q0 * self.q0; v1 = self.q1 * self.q1; v2 = self.q2 * self.q2
        v3 = self.q0 * self.q1; v4 = self.q0 * self.q2; v5 = self.q1 * self.q2
        a = v0 - v5.mul_nonres()
        b = v2.mul_nonres() - v3
        c = v1 - v4
        factor = ~(self.q0 * a + (self.q2 * b).mul_nonres() + (self.q1 * c).mul_nonres())
        return Fq6(c * factor, b * factor, a * factor)

    def __floordiv__(self, other):  # Unnecessary as Fq is sufficient
        if isinstance(other, Fq6): return self * ~other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Fq6): return self.q2 == other.q2 and self.q1 == other.q1 and self.q0 == other.q0
        return NotImplemented

    def mul_nonres(self):
        return Fq6(self.q1, self.q0, self.q2.mul_nonres())

    @classmethod
    def const(cls, q):
        return Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(q)))



# Fp12 is constructed with Fp6(w) / (w^2 - γ) where γ = v
class Fq12(Fq1):

    # noinspection PyMissingConstructor
    def __init__(self, q1, q0):
        if not isinstance(q1, Fq6) or not isinstance(q0, Fq6): raise ValueError
        self.q1 = q1
        self.q0 = q0

    def __repr__(self):
        return "{}w {}".format(self.q1, self.q0)

    def __add__(self, other):
        if isinstance(other, Fq12): return Fq12(self.q1 + other.q1, self.q0 + other.q0)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Fq12): return Fq12(self.q1 - other.q1, self.q0 - other.q0)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Fq12):
            return Fq12(self.q1 * other.q0 + self.q0 * other.q1,
                        self.q0 * other.q0 + (self.q1 * other.q1).mul_nonres())
        return NotImplemented

    def __invert__(self):
        if simple_invert: return self ** ((self.PRIME**12)-2)
        factor = ~(self.q0*self.q0 - (self.q1*self.q1).mul_nonres())
        return Fq12(Fq6.const(-1) * factor * self.q1, factor * self.q0)

    def __floordiv__(self, other):  # Unnecessary as Fq is sufficient
        if isinstance(other, Fq12): return self * ~other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Fq12): return self.q1 == other.q1 and self.q0 == other.q0
        return NotImplemented

    @classmethod
    def const(cls, q):
        return Fq12(Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0))), Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(q))))


assert Fq1.PRIME == 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab

Point = namedtuple('Point', ['x', 'y'])

def fq2_mul_fq12(fq2, fq12):
    result = copy.deepcopy(fq12)
    result.q1.q2 *= fq2
    result.q1.q1 *= fq2
    result.q1.q0 *= fq2
    result.q0.q2 *= fq2
    result.q0.q1 *= fq2
    result.q0.q0 *= fq2
    return result

def untwist(point_fq2):
    ut_root = Fq6(Fq2(Fq1(0x0), Fq1(0x0)), Fq2(Fq1(0x0), Fq1(1)), Fq2(Fq1(0x0), Fq1(0x0)))
    fq6_zero = Fq6(Fq2(Fq1(0x0), Fq1(0x0)), Fq2(Fq1(0x0), Fq1(0x0)), Fq2(Fq1(0x0), Fq1(0x0)))
    wsq = ~Fq12(fq6_zero, ut_root)   # Can be made a constant
    wcu = ~Fq12(ut_root, fq6_zero)   # Can be made a constant
    x_new = fq2_mul_fq12(point_fq2.x, wsq)
    y_new = fq2_mul_fq12(point_fq2.y, wcu)
    return Point(x=x_new, y=y_new)


def deval(R, P):
    rx2 = R.x * R.x
    slope = (rx2 + rx2 + rx2) * (~(R.y + R.y))
    v = R.y - slope * R.x
    ret = P.y - P.x * slope - v
    return ret

    # # do everything projectively
    # slope_num = 3 * pow(xR, 2)
    # slope_den = 2 * yR * zR
    # v_num = yR * slope_den - slope_num * xR * zR
    # v_den = slope_den * zR3
    # ret_num = yP * slope_den * zR3 - xP * slope_num * zR3 - v_num
    # ret_den = v_den
