from py_ecc.bn128 import neg, multiply, eq, G1, G2, pairing

def func():
    # -ab + cd = 0
    # A1B2 + C1D2 = 0
    # e(-aG1, bG2) + e(cG1, dG2) = 0

    a = 4
    b = 3
    c = 6
    d = 2
    
    P1 = new(multiply(G1, a));
    P2 = multiply(G2, b);

    Q1 = multiply(G1, c);
    Q2 = multiply(G2, d);

    assert (pairing(P2, P1) + pairing(Q2, Q1) == 0);
    print("Success!")

if __name__ == '__main__':
    func();
