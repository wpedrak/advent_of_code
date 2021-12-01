import math

def is_prime(n):
    for potential_divisor in range(2, int(math.sqrt(n)) + 1):
        if n % potential_divisor == 0:
            return False

    return True

number_of_not_primes = 0

for number in range(106700, 123700 + 1, 17):
    number_of_not_primes += not is_prime(number)

print(number_of_not_primes)
