from collections import namedtuple
from functools import partial

# Q_PRIME = 59


class Fq1:

    Q = -1
    @classmethod
    def set_q(cls, q): cls.Q = q

    def __init__(self, q): self.q = q % self.Q
    def __repr__(self): return "{}".format(self.q)
    def __add__(self, other):
        if isinstance(other, Fq2): return Fq2(self.q + other.q1, other.q0)
        return Fq1(self.q + other) if isinstance(other, int) else Fq1(self.q + other.q)
    def __sub__(self, other):
        if isinstance(other, Fq2): return Fq2(self.q - other.q1, other.q0)
        return Fq1(self.q + self.Q - other.q)
    def __mul__(self, other): return self.q * other if isinstance(other, Fq2) else Fq1(self.q * other.q)
    def __rmul__(self, other): return Fq1(self.q * other)
    def __invert__(self):
        x0, x1, y0, y1, a = 1, 0, 0, 1, self.Q
        b = self.q
        while a != 0:
            q, b, a = b // a, a, b % a
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return Fq1(x0)
    def __floordiv__(self, other): return self * ~other
    def __pow__(self, power):
        if power == 0: return Fq1(1)
        if power == 1: return self
        if power % 2 == 0:
            return (self * self) ** (power // 2)
        return (self * self) ** (power // 2) * self
    def __eq__(self, other): return self.q == other.q
    @staticmethod
    def one(): return Fq1(1)


class Fq2:

    Q = -1
    @classmethod
    def set_q(cls, q): cls.Q = q

    def __init__(self, q1, q0): self.q1 = q1 % self.Q; self.q0 = q0 % self.Q  # real, imag
    def __repr__(self): return "{} {}i".format(self.q1, self.q0)
    def __add__(self, other):
        if isinstance(other, int): return Fq2(self.q1 + other, self.q0)
        elif isinstance(other, Fq1): return Fq2(self.q1 + other.q, self.q0)
        else: return Fq2(self.q1 + other.q1, self.q0 + other.q0)
    def __sub__(self, other): return Fq2(self.q1 - other.q, self.q0) if isinstance(other, Fq1) else Fq2(self.q1 - other.q1, self.q0 - other.q0)
    def __mul__(self, other): return Fq2(self.q1 * other, self.q0 * other) if isinstance(other, int) else Fq2(self.q1 * other.q1 - self.q0 * other.q0, self.q1 * other.q0 + self.q0 * other.q1)
    def __rmul__(self, other): return Fq2(self.q1 * other, self.q0 * other)
    def __invert__(self):
        f_inv1 = (~Fq1(self.q1*self.q1 + self.q0*self.q0)).q
        return Fq2(self.q1 * f_inv1, -1 * self.q0 * f_inv1)
    def __floordiv__(self, other): return self * ~other
    def __pow__(self, power):
        if power == 0: return Fq2(1, 0)
        if power == 1: return self
        if power % 2 == 0:
            return (self * self) ** (power // 2)
        return (self * self) ** (power // 2) * self
    def __eq__(self, other): return self.q1 == other.q1 and self.q0 == other.q0
    @staticmethod
    def one(): return Fq2(1, 0)


Point = namedtuple('Point', ['x', 'y'])

# def distortion(p):
#     q = Point(Fq2(Q_PRIME-p.x.q, 0), Fq2(0, p.y.q))
#     return q

class Curve:
    # y^2 = x^3 + a * x + b
    # E: Y^2 = X^3 + X (over F59)
    # E: Y^2 = X^3 + 30 * X + 34

    A, B = -1, -1
    @classmethod
    def set_a_b(cls, a, b): cls.A = a; cls.B = b

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


if __name__ == "__main__":

    print("Start\n\n")

    P = Point(x=Fq1(25), y=Fq1(30))
    Q = Point(x=Fq2(-25, 0), y=Fq2(0, 30))
    R = Point(x=Fq1(40), y=Fq1(54))
    S = Point(x=Fq2(48, 55), y=Fq2(28, 51))

    p_plus_r = Curve.add(P, R)
    q_plus_s = Curve.add(Q, S)

    def vp(p_sub, p_pt):
        return Fq2(p_pt.x.q1 - p_sub.x.q, p_pt.x.q0)

    def lpp(p_sub1, p_sub2, p_pt):
        slope_num = p_sub2.y.q - p_sub1.y.q
        slope_den = p_sub2.x.q - p_sub1.x.q
        y_int = p_sub1.y.q*slope_den - p_sub1.x.q*slope_num
        return p_pt.x * (-slope_num) + p_pt.y * slope_den + y_int * (-1)

    def tp(p_sub, p_pt):
        alpha = ((3 * p_sub.x.q ** 2 + 1) * pow(2 * p_sub.y.q, Q_PRIME - 2, Q_PRIME)) % Q_PRIME
        y_int = -(p_sub.y.q - alpha * p_sub.x.q) % Q_PRIME
        return -alpha * p_pt.x + p_pt.y + y_int


    vp1 = vp(p_plus_r, q_plus_s)
    print("vp1 ", vp1)
    lpp1 = lpp(P, R, q_plus_s)
    print("lpp1 ", lpp1)
    x1 = vp1 // lpp1
    print("res step 1--> ", )
    tp1 = tp(P, q_plus_s)
    print("tp1 ", tp1)
    p2 = Curve.multiply(P, 2)
    v2p = vp(p2, q_plus_s)
    print("V2p: ", v2p)
    f2 = (x1**2) * tp1 // v2p
    print("f2 ", f2)

    print("Finish\n\n")

    ################ Everything below should work
    #sys.exit(0)

    for scalar in range(1, Q_PRIME):
        x = Fq1(scalar)
        x_inv = ~x
        one = x * x_inv
        assert one == Fq1(1)

    for scalar_r in range(1, Q_PRIME):
        for scalar_i in range(1, Q_PRIME):
            x = Fq2(scalar_r, scalar_i)
            x_inv = ~x
            one = x * x_inv
            assert one == Fq2(1, 0)

    g1 = Point(Fq1(25), Fq1(30))
    g2 = distortion(g1)
    print("generator 1 ", g1)
    print("generator 2 ", g2)
    for scalar in range(1, 3):
        print(scalar, "g1", Curve.multiply(g1, scalar))
        print(scalar, "g2", Curve.multiply(g2, scalar))

    print("----\n\n")



    p_plus_r = Curve.add(P, R)
    q_plus_s = Curve.add(Q, S)
    print("p+r", p_plus_r)
    print("q+s", q_plus_s)


    def v_test(p_def):
        return "X + {}".format(-p_def.x.q % Q_PRIME)

    def v_func(p_def):
        def v_func_inner(p_def, p): return Fq2(p.x.q1 - p_def.x.q, p.x.q0)
        return partial(v_func_inner, p_def)


    def l_test(p1_def, p2_def):
        slope_num = 1 * (p2_def.y.q - p1_def.y.q)
        slope_den = (p2_def.x.q - p1_def.x.q)
        y_int = p1_def.y.q*slope_den - p1_def.x.q*slope_num
        return "{}y + {}x + {} == 0".format(slope_den % Q_PRIME, -slope_num % Q_PRIME, -y_int % Q_PRIME)

    def l_func(p1_def, p2_def):
        slope_num = 1 * (p2_def.y.q - p1_def.y.q)
        slope_den = (p2_def.x.q - p1_def.x.q)
        y_int = p1_def.y.q*slope_den - p1_def.x.q*slope_num
        def l_func_inner(slope_num, slope_den, y_int, p): return p.x*(-slope_num) + p.y*slope_den + y_int*(-1)
        return partial(l_func_inner, slope_num, slope_den, y_int)


    def t_test(p_def):
        alpha = ((3*p_def.x.q**2 + 1) * pow(2*p_def.y.q, Q_PRIME-2, Q_PRIME)) % Q_PRIME
        y_int = -(p_def.y.q - alpha*p_def.x.q) % Q_PRIME
        return "{}x + {}y + {}".format(-alpha, 1, y_int)

    def t_func(p_def):
        alpha = ((3*p_def.x.q**2 + 1) * pow(2*p_def.y.q, Q_PRIME-2, Q_PRIME)) % Q_PRIME
        y_int = -(p_def.y.q - alpha*p_def.x.q) % Q_PRIME
        def t_func_inner(alpha, y_int, p_def): return -alpha*p_def.x + p_def.y + y_int
        return partial(t_func_inner, alpha, y_int)


    # V_p+r is just X + point_coord (maybe a minus)

    print("vert test: ", v_test(p_plus_r))
    print("line test : ", l_test(P, R))

    res_v = v_func(p_plus_r)
    print("res v", res_v(q_plus_s))
    res_l = l_func(P, R)
    print("res l", res_l(q_plus_s))

    print("f1--> ", res_v(q_plus_s) // res_l(q_plus_s))
    x1 = res_v(q_plus_s) // res_l(q_plus_s)

    print("Tp ", t_test(P))
    p2 = Curve.multiply(P,2)
    print("V2p ", v_test(p2))

    tf = t_func(P)
    print("tf (good: 3, 45i): ", tf(q_plus_s))
    vf = v_func(p2)
    print("vf (good: 43, 17i): ", vf(q_plus_s))
    print("x1", type(x1), type(vf), type(tf))
    print(x1**2)
    print("step 2: ", ((x1**2)*tf(q_plus_s)) // vf(q_plus_s))

    print(Fq2(18, 16) * Fq2(3, 45) // Fq2(43, 17)) # = 33 + 22i.