class Fq1:

    Q = -1  # Set correctly prior to use

    def __init__(self, q):
        self.q = q % self.Q

    def __repr__(self):
        return "{}".format(self.q)

    def __add__(self, other):
        if isinstance(other, Fq1): return Fq1(self.q + other.q)
        elif isinstance(other, int): return Fq1(self.q + other)
        elif isinstance(other, Fq2): return Fq2(self.q + other.q1, other.q0)
        else: return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Fq1): return Fq1(self.q + self.Q - other.q)
        elif isinstance(other, Fq2): return Fq2(self.q - other.q1, other.q0)
        else: return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Fq1): return Fq1(self.q * other.q)
        elif isinstance(other, Fq2): return self.q * other
        else: return NotImplemented

    def __rmul__(self, other):
        return Fq1(self.q * other)

    def __invert__(self):
        return Fq1(pow(self.q, self.Q-2, self.Q))

    def __floordiv__(self, other):
        if isinstance(other, Fq1): return self * ~other
        return NotImplemented

    def __pow__(self, power):
        if power == 0: return Fq1(1)
        if power == 1: return self
        if power % 2 == 0:
            return (self * self) ** (power // 2)
        return (self * self) ** (power // 2) * self

    def __eq__(self, other):
        return self.q == other.q

    @classmethod
    def set_q(cls, q):
        cls.Q = q

    @staticmethod
    def one(): return Fq1(1)



class Fq2:

    Q = -1

    def __init__(self, q1, q0):
        self.q1 = q1 % self.Q  # Real
        self.q0 = q0 % self.Q  # Imag

    def __repr__(self):
        return "{} {}i".format(self.q1, self.q0)

    def __add__(self, other):
        if isinstance(other, Fq2): return Fq2(self.q1 + other.q1, self.q0 + other.q0)
        elif isinstance(other, int): return Fq2(self.q1 + other, self.q0)
        elif isinstance(other, Fq1): return Fq2(self.q1 + other.q, self.q0)
        else: return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Fq2): return Fq2(self.q1 - other.q1, self.q0 - other.q0)
        elif isinstance(other, Fq1): return Fq2(self.q1 - other.q, self.q0)
        else: return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Fq2): return Fq2(self.q1 * other.q1 - self.q0 * other.q0, self.q1 * other.q0 + self.q0 * other.q1)
        elif isinstance(other, int): return Fq2(self.q1 * other, self.q0 * other)
        else: return NotImplemented

    def __rmul__(self, other):
        return Fq2(self.q1 * other, self.q0 * other)

    def __invert__(self):
        f = self.q1*self.q1 + self.q0*self.q0
        f_inv1 = pow(f, self.Q-2, self.Q)
        return Fq2(self.q1 * f_inv1, -1 * self.q0 * f_inv1)

    def __floordiv__(self, other):
        return self * ~other

    def __pow__(self, power):
        if power == 0: return Fq2(1, 0)
        if power == 1: return self
        if power % 2 == 0:
            return (self * self) ** (power // 2)
        return (self * self) ** (power // 2) * self

    def __eq__(self, other):
        return self.q1 == other.q1 and self.q0 == other.q0

    @classmethod
    def set_q(cls, q):
        cls.Q = q

    @staticmethod
    def one():
        return Fq2(1, 0)


# Extended Euclidean algorithm for another day...
# x0, x1, y0, y1, a = 1, 0, 0, 1, self.Q
# b = self.q
# while a != 0:
#     q, b, a = b // a, a, b % a
#     x0, x1 = x1, x0 - q * x1
#     y0, y1 = y1, y0 - q * y1
# return Fq1(x0)
