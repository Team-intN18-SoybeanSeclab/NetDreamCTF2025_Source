import random

p = 9223372036854775783 
e = 65537
subgroup_order = 60480

def qmul(q1, q2, p):
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    return (
        (a1*a2 - b1*b2 - c1*c2 - d1*d2) % p,
        (a1*b2 + b1*a2 + c1*d2 - d1*c2) % p,
        (a1*c2 - b1*d2 + c1*a2 + d1*b2) % p,
        (a1*d2 + b1*c2 - c1*b2 + d1*a2) % p
    )

def qconj(q, p):
    a, b, c, d = q
    return (a % p, (-b) % p, (-c) % p, (-d) % p)

def qnorm(q, p):
    a, b, c, d = q
    return (a*a + b*b + c*c + d*d) % p

def qinv(q, p):
    n = qnorm(q, p)
    inv_n = pow(n, -1, p)
    qc = qconj(q, p)
    return (qc[0] * inv_n % p, qc[1] * inv_n % p, qc[2] * inv_n % p, qc[3] * inv_n % p)

def qpow(q, exp, p):
    result = (1, 0, 0, 0)
    base = q
    while exp:
        if exp & 1:
            result = qmul(result, base, p)
        base = qmul(base, base, p)
        exp //= 2
    return result

def encode_flag(flag):
    flag_bytes = flag.encode()
    parts = [flag_bytes[0:8], flag_bytes[8:15], flag_bytes[15:22], flag_bytes[22:29]]
    return tuple(int.from_bytes(part, 'big') for part in parts)

def main():
    flag = "flag{xxx-xxx-xxx-xxx-xxx-xxx}"
    F = encode_flag(flag)
    F_q = F
    g = (2, 1, 0, 0)
    h = qpow(g, ((p * p - 1) // subgroup_order), p)
    r = random.randint(1, subgroup_order - 1)
    K = qpow(h, r, p)
    Y = qpow(K, e, p)
    K_inv = qinv(K, p)
    X = qmul(K, qmul(F_q, K_inv, p), p)
    print("----- Public Parameters -----")
    print("p =", p)
    print("e =", e)
    print("X =", X) 
    print("Y =", Y) 
    print("-----------------------------")

if __name__ == "__main__":
    main()
'''
X = (7380380986429696832, 34163292457091182, 3636630423226195928, 3896730209645707435)
Y = (1015918725738180802, 4456058114364993854, 0, 0)
'''