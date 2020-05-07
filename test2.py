import random, fields2
from fields2 import Fq1, Fq2, Fq6, Fq12
from curve import Curve, Point

import sys
sys.setrecursionlimit(5000)

X = -0xd201000000010000
ORDER = X**4 - X**2 + 1
assert (ORDER == 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001)

fields2.simple_invert = False

print("\n1. Testing Fq1, Fq2, Fq6, Fq12: add, sub ...", end='')
for i in range(1_000):

    a1 = Fq1(random.randrange(1, Fq1.PRIME))
    b1 = (a1 + a1 + a1) - a1 - a1
    assert a1 == b1

    a2 = Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))
    b2 = (a2 + a2 + a2) - a2 - a2
    assert a2 == b2

    a6 = Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
             Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
             Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))))
    b6 = (a6 + a6 + a6) - a6 - a6
    assert a6 == b6

    a12 = Fq12(Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
                   Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
                   Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))),
               Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
                   Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
                   Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))))
    b12 = (a12 + a12 + a12) - a12 - a12
    assert a12 == b12
print("passed")


print("\n2. Testing Fq1, Fq2, Fq6, Fq12: mul, inv ...", end='')
for i in range(1_000):

    a1 = Fq1(random.randrange(1, Fq1.PRIME))
    b1 = Fq1(1) // a1
    res = a1 * b1
    assert res == Fq1(1)

    a2 = Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))
    b2 = Fq2.const(1) // a2
    res = a2 * b2
    assert res == Fq2.const(1)

    a6 = Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
             Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
             Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))))
    b6 = Fq6.const(1) // a6
    res = a6 * b6
    assert res == Fq6.const(1)

    a12 = Fq12(Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
                   Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
                   Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))),
               Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
                   Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))),
                   Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))))
    b12 = Fq12.const(1) // a12
    res = a12 * b12
    assert res == Fq12.const(1)
print("passed")


print("\n3. Testing g1 mul of Fq1 ...", end='')
G1 = Point(x=Fq1(0x17f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb),
           y=Fq1(0x08b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e1))
res = Curve.multiply(G1, 0x49abcbaa08d87d1cba8fd9c0ea04df30b94df934827a7383098ac39e1aafc218)
chk = Point(x=Fq1(0x19906b4953328ec688ffc9e41ea7d79d295c7de6249eb0397680306c5fe3aa3bbb45324bdbc379e8e4116166f2a0d40),
            y=Fq1(0x165f11693959e7193af31b99b724f95d7b49baa2394b758c2455ef725f32abd56361e1e151f2bbd7a7efc6f3bb5652d4))
assert res == chk
print("passed")


print("\n4. Testing g2 mul of Fq2...", end='')
G2 = Point(x=Fq2(Fq1(0x13e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e),
                 Fq1(0x24aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb8)),
           y=Fq2(Fq1(0x606c4a02ea734cc32acd2b02bc28b99cb3e287e85a763af267492ab572e99ab3f370d275cec1da1aaa9075ff05f79be),
                 Fq1(0xce5d527727d6e118cc9cdc6da2e351aadfd9baa8cbdd3a76d429a695160d12c923ac9cc3baca289e193548608b82801)))
res = Curve.multiply(G2, 0x49abcbaa08d87d1cba8fd9c0ea04df30b94df934827a7383098ac39e1aafc218)
chk = Point(x=Fq2(Fq1(0x2433912fa403e0d19d39c7687eb1041f474a82fdd646b1a35afb4d088f11469467468f1ba16c3e5838503919bdbfa24),
                  Fq1(0x14906db96db027e17449a1323198cfccde4d15456ce09f3fef4c7baed5495463b7cc750300e0e2918d5680d97a567122)),
            y=Fq2(Fq1(0xe82e52250625e4c0864645fba3b36e24c36dbc3d4bae0ca40b0c28b0e3780bf6b8d022c032727e8195e2a2b547be84b),
                  Fq1(0xf240b0ffee3ac62cd5576f012a92cd78c9ded14c11c7637caff4daf885c9a258783a7aef4dc1815737a5b606e03868e)))
assert res == chk
print("passed")
