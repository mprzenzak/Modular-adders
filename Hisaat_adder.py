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
            b_prime[i] = a[i] & b[i]  # B'[i] = A[i] and B[i]

    for i in range(n):  # Fulfilling G', P', H'
        g_prime[i] = a_prime[i] and b_prime[i + 1]  # G'[i] = A'[i] and B'[i-1]
        p_prime[i] = a_prime[i] or b_prime[i + 1]  # P'[i] = A'[i] or B'[i-1]
        h_prime[i] = a_prime[i] ^ b_prime[i + 1]  # H'[i] = A'[i] xor B'[i-1]

    return g_0, p_0, h_0, a_prime, b_prime, k, g_prime, p_prime, h_prime


def int_to_bin_list(num: int) -> List[int]:
    return [int(bit) for bit in bin(num)[2:]]  # [2:] to remove '0b' from the beginning of the string


A = 63  # A < 2^n - 1
B = 7  # B < 2^n - 1
n = 6  # N >= 4
K = -10  # 3 <= K <= 2^(n-1) - 1 !!! K has to containt '-' before number !!!

A = int_to_bin_list(A)
B = int_to_bin_list(B)
K = int_to_bin_list(K)

G_0, P_0, H_0, A_prime, B_prime, K, G_prime, P_prime, H_prime = preprocessing(n, A, B, K)

