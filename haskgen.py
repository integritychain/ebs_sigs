import random, fields2
from fields2 import Fq1, Fq2, Fq6, Fq12

fields2.simple_invert = False

print("module HT where")
print("import Fields2")
print("import Control.Exception (assert)")

print("\nsmoke_test_mulinv_fq1 =\n  do")
for i in range(10):
    a1 = Fq1(random.randrange(1, Fq1.PRIME))
    b1 = Fq1(1) // a1
    res = a1 * b1
    assert res == Fq1(1)

    print("    let a{} = Fq1 0x{:x}".format(i, a1.q))
    print("    let b{} = Fq1 0x{:x}".format(i, b1.q))
    print("    assert (a{} `mul` b{} == Fq1 1) $ print \"smoke_test_mulinv_fq1 {}a pass\"".format(i, i, i))
    print("    assert ((inv a{}) == b{}) $ print \"smoke_test_mulinv_fq1 {}b pass\"".format(i, i, i))
    print("    assert ((inv b{}) == a{}) $ print \"smoke_test_mulinv_fq1 {}c pass\"".format(i, i, i))


print("\nsmoke_test_mulinv_fq2 =\n  do")
for i in range(10):
    a2 = Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))
    b2 = Fq2(Fq1(0), Fq1(1)) // a2
    res = a2 * b2
    assert res == Fq2(Fq1(0), Fq1(1))

    print("    let a{} = Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})".format(i, a2.q1.q, a2.q0.q))
    print("    let b{} = Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})".format(i, b2.q1.q, b2.q0.q))
    print("    assert (a{} `mul` b{} == Fq2 (Fq1 0) (Fq1 1)) $ print \"smoke_test_mulinv_fq2 {}a pass\"".format(i, i, i))
    print("    assert ((inv a{}) == b{}) $ print \"smoke_test_mulinv_fq2 {}b pass\"".format(i, i, i))
    print("    assert ((inv b{}) == a{}) $ print \"smoke_test_mulinv_fq2 {}c pass\"".format(i, i, i))


print("\nsmoke_test_mulinv_fq6 =\n  do")
for i in range(10):
    a6 = Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))), Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))), Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))))
    b6 = Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(1))) // a6
    res = a6 * b6
    assert res == Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(1)))

    print("    let a{} = Fq6 (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x}))".format(i,
            a6.q2.q1.q, a6.q2.q0.q, a6.q1.q1.q, a6.q1.q0.q, a6.q0.q1.q, a6.q0.q0.q))
    print("    let b{} = Fq6 (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x}))".format(i,
            b6.q2.q1.q, b6.q2.q0.q, b6.q1.q1.q, b6.q1.q0.q, b6.q0.q1.q, b6.q0.q0.q))
    print("    assert (a{} `mul` b{} == Fq6 (Fq2 (Fq1 0) (Fq1 0)) (Fq2 (Fq1 0) (Fq1 0)) (Fq2 (Fq1 0) (Fq1 1))) $ print \"smoke_test_mulinv_fq6 {}a pass\"".format(i, i, i))
    print("    assert ((inv a{}) == b{}) $ print \"smoke_test_mulinv_fq6 {}b pass\"".format(i, i, i))
    print("    assert ((inv b{}) == a{}) $ print \"smoke_test_mulinv_fq6 {}c pass\"".format(i, i, i))


print("\nsmoke_test_mulinv_fq12 =\n  do")
for i in range(10):
    a12 = Fq12(Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))), Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))), Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))),
               Fq6(Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))), Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME))), Fq2(Fq1(random.randrange(1, Fq1.PRIME)), Fq1(random.randrange(1, Fq1.PRIME)))))
    b12 = Fq12(Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0))),  Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(1)))) // a12
    res = a12 * b12
    assert res == Fq12(Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0))), Fq6(Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(0)), Fq2(Fq1(0), Fq1(1))))

    print("    let a{} = Fq12 (Fq6 (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x}))) (Fq6 (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})))".format(i,
            a12.q1.q2.q1.q, a12.q1.q2.q0.q, a12.q1.q1.q1.q, a12.q1.q1.q0.q, a12.q1.q0.q1.q, a12.q1.q0.q0.q, a12.q0.q2.q1.q, a12.q0.q2.q0.q, a12.q0.q1.q1.q, a12.q0.q1.q0.q, a12.q0.q0.q1.q, a12.q0.q0.q0.q))
    print("    let b{} = Fq12 (Fq6 (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x}))) (Fq6 (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})) (Fq2 (Fq1 0x{:x}) (Fq1 0x{:x})))".format(i,
            b12.q1.q2.q1.q, b12.q1.q2.q0.q, b12.q1.q1.q1.q, b12.q1.q1.q0.q, b12.q1.q0.q1.q, b12.q1.q0.q0.q, b12.q0.q2.q1.q, b12.q0.q2.q0.q, b12.q0.q1.q1.q, b12.q0.q1.q0.q, b12.q0.q0.q1.q, b12.q0.q0.q0.q))
    print("    assert (a{} `mul` b{} == Fq12 (Fq6 (Fq2 (Fq1 0) (Fq1 0)) (Fq2 (Fq1 0) (Fq1 0)) (Fq2 (Fq1 0) (Fq1 0))) (Fq6 (Fq2 (Fq1 0) (Fq1 0)) (Fq2 (Fq1 0) (Fq1 0)) (Fq2 (Fq1 0) (Fq1 1))) ) $ print \"smoke_test_mulinv_fq12 {}a pass\"".format(i, i, i))
    print("    assert ((inv a{}) == b{}) $ print \"smoke_test_mulinv_fq12 {}b pass\"".format(i, i, i))
    print("    assert ((inv b{}) == a{}) $ print \"smoke_test_mulinv_fq12 {}c pass\"".format(i, i, i))

print("""
smoke_test_g1 = do
    let
      g1_gx = Fq1 0x17f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb
      g1_gy = Fq1 0x08b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e1
      g1_generator = Affine g1_gx g1_gy
      double = g_add g1_generator g1_generator
      triple = g_add double g1_generator
      mult = g_mul 0x49abcbaa08d87d1cba8fd9c0ea04df30b94df934827a7383098ac39e1aafc218 g1_generator
    assert (double == Affine
      {ax = Fq1 0x572cbea904d67468808c8eb50a9450c9721db309128012543902d0ac358a62ae28f75bb8f1c7c42c39a8c5529bf0f4e,
       ay = Fq1 0x166a9d8cabc673a322fda673779d8e3822ba3ecb8670e461f73bb9021d5fd76a4c56d9d4cd16bd1bba86881979749d28})
      $ print "g1 double ok"
    assert (triple == Affine
      {ax = Fq1 0x9ece308f9d1f0131765212deca99697b112d61f9be9a5f1f3780a51335b3ff981747a0b2ca2179b96d2c0c9024e5224,
       ay = Fq1 0x32b80d3a6f5b09f8a84623389c5f80ca69a0cddabc3097f9d9c27310fd43be6e745256c634af45ca3473b0590ae30d1})
      $ print "g1 triple ok"
    assert (mult == Affine
      {ax = Fq1 0x19906b4953328ec688ffc9e41ea7d79d295c7de6249eb0397680306c5fe3aa3bbb45324bdbc379e8e4116166f2a0d40,
       ay = Fq1 0x165f11693959e7193af31b99b724f95d7b49baa2394b758c2455ef725f32abd56361e1e151f2bbd7a7efc6f3bb5652d4})
      $ print "g1 mult ok"

""")


print("""
smoke_test_g2 = do
    let
      g2_gx = Fq2 (Fq1 0x13e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e)
                  (Fq1 0x24aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb8)
      g2_gy = Fq2 (Fq1 0x606c4a02ea734cc32acd2b02bc28b99cb3e287e85a763af267492ab572e99ab3f370d275cec1da1aaa9075ff05f79be)
                  (Fq1 0xce5d527727d6e118cc9cdc6da2e351aadfd9baa8cbdd3a76d429a695160d12c923ac9cc3baca289e193548608b82801)
      g2_generator = Affine g2_gx g2_gy
      double = g_add g2_generator g2_generator
      triple = g_add double g2_generator
      mult = g_mul 0x49abcbaa08d87d1cba8fd9c0ea04df30b94df934827a7383098ac39e1aafc218 g2_generator
    assert (double == Affine
      {ax = Fq2 (Fq1 0xa4edef9c1ed7f729f520e47730a124fd70662a904ba1074728114d1031e1572c6c886f6b57ec72a6178288c47c33577)
                (Fq1 0x1638533957d540a9d2370f17cc7ed5863bc0b995b8825e0ee1ea1e1e4d00dbae81f14b0bf3611b78c952aacab827a053),
       ay = Fq2 (Fq1 0xf6d4552fa65dd2638b361543f887136a43253d9c66c411697003f7a13c308f5422e1aa0a59c8967acdefd8b6e36ccf3)
                (Fq1 0x468fb440d82b0630aeb8dca2b5256789a66da69bf91009cbfe6bd221e47aa8ae88dece9764bf3bd999d95d71e4c9899)})
      $ print "g2 double ok"
    assert (triple == Affine
      {ax = Fq2 (Fq1 0x9380275bbc8e5dcea7dc4dd7e0550ff2ac480905396eda55062650f8d251c96eb480673937cc6d9d6a44aaa56ca66dc)
                (Fq1 0x122915c824a0857e2ee414a3dccb23ae691ae54329781315a0c75df1c04d6d7a50a030fc866f09d516020ef82324afae),
       ay = Fq2 (Fq1 0x8f239ba329b3967fe48d718a36cfe5f62a7e42e0bf1c1ed714150a166bfbd6bcf6b3b58b975b9edea56d53f23a0e849)
                (Fq1 0xb21da7955969e61010c7a1abc1a6f0136961d1e3b20b1a7326ac738fef5c721479dfd948b52fdf2455e44813ecfd892)})
      $ print "g2 triple ok"
    assert (mult == Affine
      {ax = Fq2 (Fq1 0x2433912fa403e0d19d39c7687eb1041f474a82fdd646b1a35afb4d088f11469467468f1ba16c3e5838503919bdbfa24)
                (Fq1 0x14906db96db027e17449a1323198cfccde4d15456ce09f3fef4c7baed5495463b7cc750300e0e2918d5680d97a567122),
       ay = Fq2 (Fq1 0xe82e52250625e4c0864645fba3b36e24c36dbc3d4bae0ca40b0c28b0e3780bf6b8d022c032727e8195e2a2b547be84b)
                (Fq1 0xf240b0ffee3ac62cd5576f012a92cd78c9ded14c11c7637caff4daf885c9a258783a7aef4dc1815737a5b606e03868e)})
      $ print "g2 mult ok"
""")


print("\n\nsmoke =\n    do")
print("      smoke_test_mulinv_fq1")
print("      smoke_test_mulinv_fq2")
print("      smoke_test_mulinv_fq6")
print("      smoke_test_mulinv_fq12")
print("      smoke_test_g1")
print("      smoke_test_g2")

