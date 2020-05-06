class Fq0:
    X = -0xd201000000010000
    PRIME = (X - 1) ** 2 * (X ** 4 - X ** 2 + 1) // 3 + X

    def __pow__(self, power):
        if not isinstance(power, int): return NotImplemented
        if power == 0: return self.const(1)
        if power == 1: return self
        if power % 2 == 0:
            return (self * self) ** (power // 2)
        return (self * self) ** (power // 2) * self


class Fq(Fq0):

    def __init__(self, q):
        self.q = q % self.PRIME

    def __repr__(self):
        return "{}".format(self.q)

    def __add__(self, other):
        if isinstance(other, Fq): return Fq(self.q + other.q)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Fq): return Fq(self.q - other.q)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Fq): return Fq(self.q * other.q)
        return NotImplemented

    def __invert__(self):
        return Fq(pow(self.q, self.PRIME - 2, self.PRIME))

    def __floordiv__(self, other):
        if isinstance(other, Fq): return self * ~other
        return NotImplemented

    def __eq__(self, other):
        return self.q == other.q

    @classmethod
    def const(cls, q):
        return Fq(q)

# Fp2 is constructed with Fp1(u) / (u^2 - β) where β = -1.
class Fq2(Fq):
    def __init__(self, q1, q0):
        self.q1 = q1  # imag
        self.q0 = q0  # real

    def __repr__(self):
        return "{}i {}".format(self.q1, self.q0)

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
        f = self.q1 * self.q1 + self.q0 * self.q0
        f_inv1 = pow(f, self.PRIME - 2)
        # return Fq2(self.q1 * f_inv1, -1 * self.q0 * f_inv1)
        return Fq2(Fq(-1) * self.q1 * f_inv1, self.q0 * f_inv1)

    def __floordiv__(self, other):
        if isinstance(other, Fq2): return self * ~other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Fq2): return self.q1 == other.q1 and self.q0 == other.q0
        return False

    @classmethod
    def const(cls, q0):
        return Fq2(Fq(0), Fq(q0))

    @classmethod
    def mul_by_nonresidue(cls, z):
        return Fq2(z.q1 - z.q0, z.q1 + z.q0)


# Fp6 is constructed with Fp2(v) / (v^3 - ξ) where ξ = u + 1
class Fq6(Fq):
    def __init__(self, q2, q1, q0):  # Each is Fq2
        self.q2 = q2
        self.q1 = q1
        self.q0 = q0

    def __repr__(self):
        return "{} {}i".format(self.q1, self.q0)

    def __add__(self, other):
        if isinstance(other, Fq6): return Fq6(self.q2 + other.q2, self.q1 + other.q1, self.q0 + other.q0)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Fq6): return Fq6(self.q2 - other.q2, self.q1 - other.q1, self.q0 - other.q0)
        return NotImplemented

    def __mul__(self, other):  # Fq2(v) / (v^3 - j) where j = u + 1
        if isinstance(other, Fq6):
            t0 = self.q0 * other.q0
            t1 = self.q0 * other.q1 + self.q1 * other.q0
            t2 = self.q0 * other.q2 + self.q1 * other.q1 + self.q2 * other.q0
            t3 = Fq2(Fq(1), Fq(1)) * (self.q1 * other.q2 + self.q2 * other.q1)
            t4 = Fq2(Fq(1), Fq(1)) * (self.q2 * other.q2)
            return Fq6(t2, t1 + t4, t0 + t3)  ### TKTKTKTK WORKS!?!!
        return NotImplemented

    def __invert__(self):
        alpha = Fq2(Fq(1), Fq(1))
        v0 = self.q0 * self.q0; v1 = self.q1 * self.q1; v2 = self.q2 * self.q2
        v3 = self.q0 * self.q1; v4 = self.q0 * self.q2; v5 = self.q1 * self.q2
        A = v0 - (alpha * v5)
        B = (alpha * v2) - v3
        C = v1 - v4
        v6 = self.q0 * A
        v6 = v6 + (alpha * self.q2 * B)
        v6 = v6 + (alpha * self.q1 * C)
        F = ~v6 # pow(v6, Fq.PRIME - 2)
        return Fq6(C * F, B * F, A * F)

    def __floordiv__(self, other):
        if isinstance(other, Fq6): return self * ~other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Fq6): return self.q2 == other.q2 and self.q1 == other.q1 and self.q0 == other.q0
        return False

    @classmethod
    def const(cls, q0):
        return Fq6(Fq2(Fq(0), Fq(0)), Fq2(Fq(0), Fq(0)), Fq2(Fq(0), Fq(q0)))

    def xx_mul_by_nonresidue(self):
        # multiply by v
        #a, b, c = self.q2, self.q1, self.q0
        return Fq6(self.q1, self.q0, self.q2*Fq2(Fq(1), Fq(1)))  # rev


# Fp12 is constructed with Fp6(w) / (w^2 - γ) where γ = v
class Fq12(Fq):
    def __init__(self, q1, q0):
        self.q1 = q1
        self.q0 = q0

    def __repr__(self):
        return "{}i {}".format(self.q1, self.q0)

    def __add__(self, other):
        if isinstance(other, Fq12): return Fq12(self.q1 + other.q1, self.q0 + other.q0)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Fq12): return Fq12(self.q1 - other.q1, self.q0 - other.q0)
        return NotImplemented

    # fn mul_assign(&mut self, other: &Self) {
    #     let mut aa = self.c0;
    #     aa.mul_assign(&other.c0);
    #     let mut bb = self.c1;
    #     bb.mul_assign(&other.c1);
    #     let mut o = other.c0;
    #     o.add_assign(&other.c1);
    #     self.c1.add_assign(&self.c0);
    #     self.c1.mul_assign(&o);
    #     self.c1.sub_assign(&aa);
    #     self.c1.sub_assign(&bb);
    #     self.c0 = bb;
    #     self.c0.mul_by_nonresidue();
    #     self.c0.add_assign(&aa);
    # }



    def __mul__(self, other):
        if isinstance(other, Fq12):
            aa = self.q0 * other.q0
            bb = self.q1 * other.q1
            o = other.q1 + other.q0
            res1 = (self.q0 + self.q1) * o - aa - bb
            res0 = bb.xx_mul_by_nonresidue() + aa
            # return Fq12(res1, res0)
            return Fq12(self.q1 * other.q0 + self.q0 * other.q1, self.q0 * other.q0 + (self.q1 * other.q1).xx_mul_by_nonresidue())
            # bad return Fq12(self.q1 * other.q0 + self.q0 * other.q1, self.q0 * other.q0 - self.q1 * other.q1)
        return NotImplemented

    # def __invert__(self):
    #     f = self.q1 * self.q1 + self.q0 * self.q0
    #     f_inv1 = pow(f, self.PRIME - 2)
    #     # return Fq12(-1 * self.q1 * f_inv1, self.q0 * f_inv1)
    #     return Fq12(Fq6(Fq2(0,0), Fq2(0,0), Fq2(0,-1)) * self.q1 * f_inv1, self.q0 * f_inv1)


    def __invert__(self):
        return self.getFac()
        print("here")
        a, b = self.q0, self.q1
        factor = ~(a*a - (b*b).xx_mul_by_nonresidue())
        print("FAC {}".format(factor))
        res = Fq12((Fq6.const(0)-b) * factor, a * factor )
        return res

    def getFac(self):
        a, b = self.q0, self.q1
        factor = ~(a*a - (b*b).xx_mul_by_nonresidue())  # note inv gone!
        # return (b*b).xx_mul_by_nonresidue()
        # return a * a - (b * b).xx_mul_by_nonresidue()
        # return ~(a * a - (b * b).xx_mul_by_nonresidue())
        return Fq12((Fq6.const(0) - factor) * self.q1, factor * self.q0)    # factor

    def __floordiv__(self, other):
        if isinstance(other, Fq12): return self * ~other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Fq12): return self.q1 == other.q1 and self.q0 == other.q0
        return False

    @classmethod
    def const(cls, q0):
        return Fq12(Fq6(Fq2(Fq(0), Fq(0)), Fq2(Fq(0), Fq(0)), Fq2(Fq(0), Fq(0))), Fq6(Fq2(Fq(0), Fq(0)), Fq2(Fq(0), Fq(0)), Fq2(Fq(0), Fq(q0))))

    # @classmethod
    # def mul_by_nonresidue(cls, z):
    #     return Fq2(z.q1 - z.q0, z.q1 + z.q0)








assert Fq.PRIME == 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
