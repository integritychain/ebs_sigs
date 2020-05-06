import random
from fields import Fq1, Fq2
from curve import Curve, Point
from weil import miller_loop, weil_pairing


random.seed(1234)

print("\n\n1. Testing Fq1 and Fq2 inverse", end='')
Fq1.set_q(631)
Fq2.set_q(2**255 - 19)
for i in range(10):
    a1 = Fq1(random.randrange(1, Fq1.Q))
    b1 = Fq1.one() // a1
    assert a1 * b1 == Fq1.one()
    a2 = Fq2(random.randrange(1, Fq2.Q), random.randrange(1, Fq2.Q))
    b2 = Fq2.one() // a2
    res = a2 * b2
    assert a2 * b2 == Fq2.one()
print("...passed\n\n")


Curve.set_a_b(30, 34)
P = Point(x=Fq1(36), y=Fq1(60))
Q = Point(x=Fq1(121), y=Fq1(387))
S = Point(x=Fq1(0), y=Fq1(36))

print("group1 = [", end='')
for i in range(1,5):
    g = Curve.multiply(P, i)
    print("(Affine {:3} {:3}), ".format(g.x.q, g.y.q), end='')
print("")

print("group2 = [", end='')
for i in range(1,5):
    g = Curve.multiply(Q, i)
    print("(Affine {:3} {:3}), ".format(g.x.q, g.y.q), end='')
print("]")

print("2. Testing Text p323...", end='')
x1 = miller_loop(P, Curve.add(Q, S))
x2 = miller_loop(P, S)
x3 = x1 // x2
assert x1 == Fq1(103) and x2 == Fq1(219) and x3 == Fq1(473)

y1 = miller_loop(Q, Curve.add(P, Curve.negate(S)))
y2 = miller_loop(Q, Curve.negate(S))
y3 = y1 // y2
assert y1 == Fq1(284) and y2 == Fq1(204) and y3 == Fq1(88)

e5 = x3 // y3
e6 = e5 ** 5
assert e5 == Fq1(242) and e6 == Fq1.one()
print("passed\n\n")


print("3. Testing Text p324...", end='')
Pp = Point(x=Fq1(617), y=Fq1(5))
Qp = Point(x=Fq1(121), y=Fq1(244))

res = weil_pairing(P=Pp, Q=Qp, S=S, R=Curve.negate(S), order=5)
assert res == Fq1(512)
print("passed\n\n")


print("4. Testing Thesis p39...", end='')
Fq1.set_q(59)
Fq2.set_q(59)
Curve.set_a_b(1, 0)
P = Point(x=Fq2(25, 0), y=Fq2(30, 0))    # (25, 30)
# P = Point(x=Fq1(25), y=Fq1(30))    # (25, 30)
Q = Point(x=Fq2(-25, 0), y=Fq2(0, 30))  # (−25, 30i)
S = Point(x=Fq2(48, 55), y=Fq2(28, 51))  # (48 + 55i, 28 + 51i)
# R = Point(x=Fq2(40, 0), y=Fq2(54, 0))
R = Point(x=Fq1(40), y=Fq1(54))

res = weil_pairing(P=P, Q=Q, S=S, R=Curve.negate(S), order=5)
assert res == Fq2(46, 56)
print("passed\n\n")
