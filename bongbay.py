from fractions import Fraction
import math

N_total = math.comb(280, 2) * math.comb(278, 2) * math.comb(276, 2)
N1 = math.comb(56, 3) * math.factorial(3) * (math.comb(5, 2) ** 3)
N2 = 3 * math.comb(56, 2) * math.factorial(2) * (math.comb(5, 2) ** 2) * math.comb(54, 2) * (5 ** 2)
N3 = 3 * 56 * math.comb(5, 2) * math.comb(55, 2) * (5 ** 2) * math.comb(53, 2) * (5 ** 2)
N4 = math.comb(56, 2) * (5 ** 2) * math.comb(54, 2) * (5 ** 2) * math.comb(52, 2) * (5 ** 2)

N_complement = N1 + N2 + N3 + N4
P = Fraction(N_total - N_complement, N_total)
print(f"Kết quả: {P}")