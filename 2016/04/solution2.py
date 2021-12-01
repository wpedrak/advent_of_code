import hashlib


def get_hash(text):
    return hashlib.md5(text.encode()).hexdigest()


def solve(secret_key):
    decimal = 0

    while True:
        if decimal % 1000 == 0:
            print(decimal)
        to_hash = secret_key + str(decimal)
        hashed = get_hash(to_hash)
        if hashed[:6] == '000000':
            return decimal

        decimal += 1


secret_key = 'bgvyzdsv'
result = solve(secret_key)

print(result)
