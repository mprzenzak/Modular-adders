# Definicja funkcji decimal_to_rns, która konwertuje liczbę dziesiętną na system reszt (RNS).
def decimal_to_rns(number, moduli):
    # Obliczenie reszt dla każdego z modułów (elementów listy moduli) i zapisanie ich w liście residues.
    residues = [number % modulus for modulus in moduli]
    # Zwracanie listy reszt.
    return residues


# Definicja funkcji rns_to_decimal, która konwertuje liczbę zapisaną w systemie reszt (RNS) na liczbę dziesiętną.
def rns_to_decimal(residues, moduli):
    total = 0
    M = 1
    # Obliczenie iloczynu wszystkich modułów.
    for modulus in moduli:
        M *= modulus

    # Obliczenie liczby dziesiętnej na podstawie reszt i modułów.
    for i in range(len(residues)):
        m_i = M // moduli[i]
        total += residues[i] * m_i * pow(m_i, -1, moduli[i])

    # Zwracanie liczby dziesiętnej modulo M.
    return total % M


# Definicja funkcji rns_addition, która dodaje dwie liczby zapisane w systemie reszt (RNS).
def rns_addition(x, y, moduli):
    # Dodawanie elementów list x, y oraz wykonywanie operacji modulo dla każdego elementu listy moduli.
    result = [(x_i + y_i) % modulus for x_i, y_i, modulus in zip(x, y, moduli)]
    # Zwracanie listy zawierającej wynik dodawania.
    return result


# Inicjalizacja modułów RNS.
moduli = [3, 5, 7]
# moduli = [23, 29, 31]

# Inicjalizacja liczb dziesiętnych.
# num1 = 10+9
# num2 = 15
num1 = 99
num2 = 7

# Konwersja liczb dziesiętnych na system reszt (RNS).
num1_rns = decimal_to_rns(num1, moduli)
num2_rns = decimal_to_rns(num2, moduli)

# Dodawanie liczb w systemie reszt (RNS).
result_rns = rns_addition(num1_rns, num2_rns, moduli)

# Konwersja wyniku z systemu reszt (RNS) na system dziesiętny.
result_decimal = rns_to_decimal(result_rns, moduli)

# Wypisanie wyników.
print(f"Dodawanie liczb {num1} i {num2}:")
print(f"{num1_rns} (RNS) + {num2_rns} (RNS) = {result_rns} (RNS)")
print(f"W systemie dziesiętnym: {num1} + {num2} = {result_decimal}")
