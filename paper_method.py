import numpy as np

b0 = 0

a_00 = 0
a_10 = 1
b0_prime = 0
delta_1 = 3.2

start_guess = [0, 1]
delta = [0, 3.2]  # Shift by 1 to agree with paper
a_i = [2.03123535004797, 3.19483850876]
# a_i = [0, 1]

"""def bk(a, n):
    if n == 0:
        return 0
    else:
        return a - bk(a, n - 1) ** 2


def bk_prime(a, n):
    if n == 0:
        return 0
    else:
        return 1 - 2 * bk_prime(a, n - 1) * bk(a, n - 1)"""


def bk(mu, a, n):
    if n == 0:
        return 0
    else:
        return mu * (bk(mu, a, n - 1) * (1 - bk(mu, a, n - 1)) + a * (bk(mu, a, n - 1) ** 4) * (1 - bk(mu, a, n - 1)))


def bk_prime(mu, a, n):
    if n == 0:
        return 0
    else:
        return mu * (bk_prime(mu, a, n - 1) - 2 * bk_prime(mu, a, n - 1) * bk(mu, a, n - 1) +
                     a * (4 * bk_prime(mu, a, n - 1) * bk(mu, a, n - 1) ** 3 -
                          5 * bk_prime(mu, a, n - 1) * bk(mu, a, n - 1) ** 4))


def inter_aj(i):
    tol = 1e-5
    max_iter = 100
    a = 1/4

    if i > 1:
        a_next = a_i[i - 1] + (a_i[i - 1] - a_i[i - 2]) / delta[i - 1]
    elif i == 1:
        a_next = 1
    else:
        a_next = 0

    for _ in range(max_iter):
        a_prev = a_next
        a_next -= (bk(a_next, a, 2 ** i) / bk_prime(a_next, a, 2 ** i))

        if abs(a_next - a_prev) <= tol:
            break

    print(a_next)
    return a_next


num_iter = 4
for i in range(2, num_iter):
    a_i += [inter_aj(i)]
    delta += [(a_i[i - 1] - a_i[i - 2]) / (a_i[i] - a_i[i - 1])]

print(a_i)
print(delta[-1])
