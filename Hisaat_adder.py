import math
from typing import List, Tuple


def preprocessing(n: int, a: List[int], b: List[int], k: List[int]) -> Tuple[
    List[int], List[int], List[int], List[int], List[int], List[int], List[int], List[int], List[int]]:
    g_0 = [0] * n  # vector G
    p_0 = [0] * n  # vector P
    h_0 = [0] * n  # vector H

    a_prime = [0] * n  # vector A'
    b_prime = [0] * (n + 1)  # vector B'

    g_prime = [0] * n  # vector G'
    p_prime = [0] * n  # vector P'
    h_prime = [0] * n  # vector H'

    k[0] = 0  # set the most significant bit of k to 0 (K max = 2^(n-1))

    for i in range(n):  # Fulfilling vectors: G, P, H, A', B'

        g_0[i] = a[i] and b[i]  # G[i] = A[i] and B[i]
        p_0[i] = a[i] or b[i]  # P[i] = A[i] or B[i]
        h_0[i] = a[i] ^ b[i]  # H[i] = A[i] xor B[i]

        if k[i]:  # 1 == True

            a_prime[i] = not (a[i] ^ b[i])  # A'[i] = not(A[i] xor B[i])
            b_prime[i] = a[i] or b[i]  # B'[i] = A[i] or B[i]

        else:  # 0 == False

            a_prime[i] = a[i] ^ b[i]  # A'[i] = A[i] xor B[i]
            b_prime[i] = a[i] and b[i]  # B'[i] = A[i] and B[i]

    for i in range(n):  # Fulfilling G', P', H'
        g_prime[i] = a_prime[i] and b_prime[i + 1]  # G'[i] = A'[i] and B'[i-1]
        p_prime[i] = a_prime[i] or b_prime[i + 1]  # P'[i] = A'[i] or B'[i-1]
        h_prime[i] = a_prime[i] ^ b_prime[i + 1]  # H'[i] = A'[i] xor B'[i-1]

    return g_0, p_0, h_0, a_prime, b_prime, k, g_prime, p_prime, h_prime


def parallel_prefix(n: int, g_0: List[int], p_0: List[int], g_prime: List[int], p_prime: List[int]) -> tuple[
    list[int], list[int], list[int], int]:
    g_out = [0] * n  # G_out vector tab for multiplexer
    p_out = [0] * n  # P_out vector tab for multiplexer

    g_prime_out = [0] * n  # G'_out vector tab for multiplexer
    p_prime_out = [0] * n  # P'_out vector tab for multiplexer

    counter = 0

    for i in range(0, n):  # Copying G, P, G', P' values to G_out, P_out, G'_out, P'_out tabs

        g_out[i] = g_0[i]
        p_out[i] = p_0[i]

        g_prime_out[i] = g_prime[i]
        p_prime_out[i] = p_prime[i]

    layers = math.ceil(math.log2(n))  # Number of layers in parallel-prefix network
    for i in range(0, layers):  # Parallel-prefix loop through layers
        for j in range((n - 2), -1, -1):  # Parallel-prefix loop through vector from end to beginning
            g_out[j] = g_out[j] or (g_out[j + 1] and p_out[j])
            g_prime_out[j] = g_prime_out[j] or (g_prime_out[j + 1] and p_prime_out[j])

            if counter < (2 ** i):
                p_out[j] = p_out[j] and p_out[j + 1]
                p_prime_out[j] = p_prime_out[j] and p_prime_out[j + 1]

                counter = counter + 1

    c_out = g_out[-1]

    return g_out, p_out, g_prime_out, c_out


def multiplexer(n: int, c_out: bool, h_0: List[int], h_prime: List[int], g_out: List[int], g_prime_out: List[int]) -> \
        Tuple[List[int], List[int]]:  # Multiplexing stage
    h_multi = [0] * n  # H_multi vector tab
    g_multi = [0] * n  # G_multi vector tab

    h_source = h_0 if c_out else h_prime
    g_source = g_out if c_out else g_prime_out

    for i in range(n - 1):  # Multiplexing G, H vectors for range from 0 to n-1
        h_multi[i] = h_source[i]
        g_multi[i] = g_source[i + 1]

    g_multi[n - 1] = h_source[n - 1]
    h_multi[n - 1] = 0  # First bit of multiplexed vector H is always 0

    return h_multi, g_multi


def sum_computation(n, h_multi, g_multi):  # Sum computation stage
    s = [0] * n  # Creating S vector for computing sum

    for i in range(n):  # Sum computing loop
        s[i] = h_multi[i] ^ g_multi[i]  # S[i] = H_multi[i] xor G_multi[i]

    return s


def integer_to_binary(number: int, length: int) -> List[int]:
    binary_rep = bin(number)[2:]  # [2:] to remove '0b' prefix

    if len(binary_rep) > length:
        binary_rep = binary_rep[-length:]  # trim first few bits if longer

    bit_list = []
    for bit in binary_rep:
        bit_list.append(int(bit))

    while len(bit_list) < length:
        bit_list.insert(0, 0)

    return bit_list


def binary_to_integer(bin_list: List[int]) -> int:
    return int(''.join(str(bit) for bit in bin_list), 2)  # 2 because binary


A = 63  # A < 2^n - 1
B = 32  # B < 2^n - 1
K = 5  # 3 <= K <= 2^(n-1) - 1
n = 7  # N >= 4
# 70 mod 54 = 70 (-)
# 70 mod 74 = 70 (+)

print("Choose mode. Type + or -")
mode = input()

A = integer_to_binary(A, n)
B = integer_to_binary(B, n)
K = integer_to_binary(K, n)

if mode == "+":
    for i in range(len(K)):
        if (K[i] == 0):
            K[i] = 1
        else:
            K[i] = 0
    K[-1] = 1

G_0, P_0, H_0, A_prime, B_prime, K, G_prime, P_prime, H_prime = preprocessing(n, A, B, K)
G_out, P_out, G_prime_out, C_out = parallel_prefix(n, G_0, P_0, G_prime, P_prime)
H_multi, G_multi = multiplexer(n, C_out, H_0, H_prime, G_out, G_prime_out)

s = sum_computation(n, H_multi, G_multi)
print(binary_to_integer(s))
