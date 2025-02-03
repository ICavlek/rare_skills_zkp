import galois
import numpy as np
import random


def example_1():
    p = 17
    GF = galois.GF(p)

    xs = GF(np.array([1,2,3]))
    
    def L(v):
        return galois.lagrange_poly(xs, v)
    
    # two arbitrary vectors
    v1 =  GF(np.array([4,8,2]))
    v2 =  GF(np.array([1,6,12]))

    assert L(v1 + v2) == L(v1) + L(v2)

    lambda_ = GF(15)
    assert L(lambda_ * v1) == lambda_ * L(v1)

def example_2():
    # Checking A*v1 = B*v2 in O(1) instead of O(n) iterating
    p = 17
    GF = galois.GF(p)

    x_values = GF(np.array([1, 2]))

    def L(v):
        return galois.lagrange_poly(x_values, v)

    p1 = L(GF(np.array([6, 4])))
    p2 = L(GF(np.array([3, 7])))
    q1 = L(GF(np.array([3, 12])))
    q2 = L(GF(np.array([9, 6])))

    u = random.randint(0, p) # Schwarz-Zippel Lemma
    tau = GF(u) # a random point

    left_hand_side = p1(tau) * GF(2) + p2(tau) * GF(4)
    right_hand_side = q1(tau) * GF(2) + q2(tau) * GF(2)

    assert left_hand_side == right_hand_side

if __name__ == '__main__':
    # example_1()
    example_2()
