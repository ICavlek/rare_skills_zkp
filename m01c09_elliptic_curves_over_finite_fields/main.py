import libnum
import matplotlib.pyplot as plt
from py_ecc.bn128 import G1, multiply, neg, add
import math
import numpy as np

def generate_points(mod):
    xs = []
    ys = []
    def y_squared(x):
        return (x**3 + 3) % mod

    for x in range(0, mod):
        if libnum.has_sqrtmod_prime_power(y_squared(x), mod, 1):
            square_roots = libnum.sqrtmod_prime_power(y_squared(x), mod, 1)

            # we might have two solutions
            for sr in square_roots:
                ys.append(sr)
                xs.append(x)
    return xs, ys

def double(x, y, a, p):
    lambd = (((3 * x**2) % p ) *  pow(2 * y, -1, p)) % p
    newx = (lambd**2 - 2 * x) % p
    newy = (-lambd * newx + lambd * x - y) % p
    return (newx, newy)

def add_points(xq, yq, xp, yp, p, a=0):
    if xq == yq == None:
        return xp, yp
    if xp == yp == None:
        return xq, yq

    assert (xq**3 + 3) % p == (yq ** 2) % p, "q not on curve"
    assert (xp**3 + 3) % p == (yp ** 2) % p, "p not on curve"

    if xq == xp and yq == yp:
        return double(xq, yq, a, p)
    elif xq == xp:
        return None, None

    lambd = ((yq - yp) * pow((xq - xp), -1, p) ) % p
    xr = (lambd**2 - xp - xq) % p
    yr = (lambd*(xp - xr) - yp) % p
    return xr, yr

def example_1():
    xs, ys = generate_points(11)
    fig, (ax1) = plt.subplots(1, 1);
    fig.suptitle('y^2 = x^3 + 3 (mod p)');
    fig.set_size_inches(6, 6);
    ax1.set_xticks(range(0,11));
    ax1.set_yticks(range(0,11));
    plt.grid()
    plt.scatter(xs, ys)
    plt.plot();
    plt.show(block=True);

def example_2():
    # for our purposes, (4, 10) is the generator point G
    next_x, next_y = 4, 10
    print(0, 4, 10)
    points = [(next_x, next_y)]
    for i in range(1, 13):
        # repeatedly add G to the next point to generate all the elements
        next_x, next_y = add_points(next_x, next_y, 4, 10, 11)
        print(i, next_x, next_y)
        points.append((next_x, next_y))

    xs11, ys11 = generate_points(11)

    fig, (ax1) = plt.subplots(1, 1);
    fig.suptitle('y^2 = x^3 + 3 (mod 11)');
    fig.set_size_inches(13, 6);

    ax1.set_title("modulo 11")
    ax1.scatter(xs11, ys11, marker='o');
    ax1.set_xticks(range(0,11));
    ax1.set_yticks(range(0,11));
    ax1.grid()

    for i in range(0, 11):
        plt.annotate(str(i+1), (points[i][0] + 0.1, points[i][1]), color="red");
    
    plt.plot();
    plt.show(block=True);

def example_3():
    xs = []
    ys = []
    for i in range(1,1000):
        xs.append(i)
        ys.append(int(multiply(G1, i)[1]))
        xs.append(i)
        ys.append(int(neg(multiply(G1, i))[1]))
    plt.scatter(xs, ys, marker='.')
    plt.plot();
    plt.show(block=True);

def example_4():
    # Prover
    secret_x = 5
    secret_y = 10

    x = multiply(G1, 5)
    y = multiply(G1, 10)

    proof = (x, y, 15)

    # verifier
    if multiply(G1, proof[2]) == add(proof[0], proof[1]):
        print("statement is true")
    else:
        print("statement is false")

if __name__ == '__main__':
    # example_1();
    # example_2();
    # example_3();
    example_4();
