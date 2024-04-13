import numpy as np

b0 = 0

a_00 = 0
a_10 = 1
b0_prime = 0
delta_1 = 3.2

start_guess = [0, 1]
delta = [0, 3.2] # Shift by 1 to agree with paper
# a_i = [2.03123535004797, 3.19483850876]
a_i = []

def bk(a,n):
    if n==0:
        return 0
    else:
        return a - bk(a,n-1)**2

def bk_prime(a,n):
    if n==0:
        return 0
    else:
        return 1-2*bk_prime(a,n-1)*bk(a,n-1)

def inter_aj(i):
    tol = 1e-5
    max_iter = 1e4
    
    if (i>1):
        a_next = a_i[i-1] + (a_i[i-1]-a_i[i-2])/delta[i-1]
    elif(i == 1):
        a_next = 1
    else:
        a_next = 0
    
    for _ in range(max_iter):
        a_prev = a_next
        a_next -= (bk(a_next, 2**i)/bk_prime(a_next, 2**i))
    
        if abs(a_next - a_prev ) <= tol:
            break
    return a_next


num_iter = 100
for i in range(0, num_iter):
    a_i[i] = 