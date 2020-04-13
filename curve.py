from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])


class Curve:
    # y^2 = x^3 + a * x + b

    A, B = -1, -1  # Set correctly prior to use

    @classmethod
    def set_a_b(cls, a, b):
        cls.A = a
        cls.B = b

    @classmethod
    def add(cls, p, q):
        if p == "INFINITY": return q
        if q == "INFINITY": return p
        if p == q: return Curve.double(p)
        x1, y1 = p
        x2, y2 = q
        if x1 == x2: return "INFINITY"
        x3 = ((y2 - y1) // (x2 - x1))**2 - x1 - x2
        y3 = ((y2-y1) // (x2 - x1)) * (x1 - x3) - y1
        return Point(x3, y3)

    @classmethod
    def negate(cls, P):
        x1, y1 = P
        return Point(x1, -1*y1)

    @classmethod
    def double(cls, p):
        if p == "INFINITY": return "INFINITY"
        x1, y1 = p
        x3 = ((3 * x1**2 + cls.A) // (2 * y1))**2 - 2 * x1
        y3 = ((3 * x1**2 + cls.A) // (2 * y1)) * (x1 - x3) - y1
        return Point(x3, y3)

    @classmethod
    def multiply(cls, p, scalar):
        xx = bin(scalar)[:1:-1]
        res = None; temp = p
        for bit in bin(scalar)[:1:-1]:
            if bit == '1': res = temp if res is None else Curve.add(res, temp)
            temp = Curve.double(temp)
        return res
