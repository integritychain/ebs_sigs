import random

from elliptical import Fq1, Fq2, Point, Curve

random.seed(1234)
Fq1.set_q(631)
Fq2.set_q(1)

Curve.set_a_b(30, 34)


for i in range(10):
    a = Fq1(random.randrange(1, Fq1.Q))
    b = Fq1.one() // a
    assert a * b == Fq1.one()

P = Point(x=Fq1(36), y=Fq1(60))
Q = Point(x=Fq1(121), y=Fq1(387))

# for i in range(1, 12):
#     print(i, Curve.multiply(P, i))
# for i in range(1, 12):
#     print(i, Curve.multiply(Q, i))

S = Point(x=Fq1(0), y=Fq1(36))
Q_plus_S = Curve.add(Q, S)
P_minus_S = Curve.add(P, Curve.negate(S))


def g_pq(p, q, point):
    if p.x == q.x and p.y != q.y:  # Two different points forming a vertical line
        return point.x - p.x  # Vertical line
    elif p == q:   # One point duplicated
        slope = (3 * p.x**2 + Curve.A) // (2 * p.y)
    else:
        slope = (q.x - p.x) // (q.y - q.y)
    numerator = point.y - p.y - slope * (point.x - p.x)
    xyz = point.x + p.x
    denominator = xyz + q.x - slope**2
    return numerator // denominator


m = 5  # 101 -> 0 1 msb->lsb not including msb

def weil(P, XXX):
    T = P
    f = 1
    for i in [0, 1]:
        f = f * f * g_pq(T, T, XXX)
        T = Curve.multiply(T, 2)
        if i == 1:
            f = f * g_pq(T, P, XXX)
            T = Curve.add(T, P)
    return f


x1 = weil(P, Q_plus_S)
x2 = weil(P, S)
x3 = x1 // x2
print("x1 {} // x2 {}  = {}".format(x1, x2, x3))

y1 = weil(Q, P_minus_S)
y2 = weil(Q, Curve.negate(S))
y3 = y1 // y2
print("y1 {} // y2 {}  = {}".format(y1, y2, y3))

e5 = x3 // y3
e6 = e5 ** 5
print("242==GOOD e5(P,Q) = {} and **5->{}".format(e5, e6))


def full_weil(P, Q, S, R, order):
    #S = Point(x=Fq1(0), y=Fq1(36))
    x1 = weil(P, Curve.add(Q, S))
    x2 = weil(P, S)
    x3 = weil(Q, Curve.add(P, R)) # Curve.negate(S)))
    x4 = weil(Q, R) # Curve.negate(S))
    result = (x1 // x2) // (x3 // x4)
    print("debug x1 {}; x2 {}; x3 {}; x4 {}".format(x1, x2, x3, x4))
    print("result: {}  ; Raised={}".format(result, result**order))

print("\n\nGOOD=512")
full_weil(P=Point(x=Fq1(617), y=Fq1(5)), Q=Point(x=Fq1(121), y=Fq1(244)), S=S, R=Curve.negate(S), order=5)

print("\n\n")


Fq1.set_q(59)
Fq2.set_q(59)
Curve.set_a_b(1, 0)

for i in range(10):
    a = Fq2(random.randrange(1, Fq2.Q), random.randrange(1, Fq2.Q))
    b = Fq2.one() // a
    res = a * b
    assert res == Fq2.one()

print("\n\nTHESIS==46+56i")
P = Point(x=Fq2(25, 0), y=Fq2(30, 0))    # (25, 30)
# P = Point(x=Fq1(25), y=Fq1(30))    # (25, 30)
Q = Point(x=Fq2(-25, 0), y=Fq2(0, 30))  # (−25, 30i)
S = Point(x=Fq2(48, 55), y=Fq2(28, 51))  # (48 + 55i, 28 + 51i)
# R = Point(x=Fq2(40, 0), y=Fq2(54, 0))
R = Point(x=Fq1(40), y=Fq1(54))

full_weil(P=P, Q=Q, S=S, R=Curve.negate(S), order=5)



