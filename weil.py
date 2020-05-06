from curve import Curve


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


def miller_loop(P, XXX):
    T = P
    f = 1
    for i in [0, 1]:  # TODO: NEED ORDER HERE
        gtmp = g_pq(T, T, XXX)
        f = f * f * gtmp
        T = Curve.multiply(T, 2)
        if i == 1:
            g_tmp = g_pq(T, P, XXX)
            f = f * g_tmp  # g_pq(T, P, XXX)
            T = Curve.add(T, P)
    return f


def weil_pairing(P, Q, S, R, order):
    x1 = miller_loop(P, Curve.add(Q, S))
    x2 = miller_loop(P, S)
    x3 = miller_loop(Q, Curve.add(P, R)) # Curve.negate(S)))
    x4 = miller_loop(Q, R) # Curve.negate(S))
    result = (x1 // x2) // (x3 // x4)
    return result

