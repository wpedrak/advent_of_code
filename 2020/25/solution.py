CARD_PUBLIC_KEY = 5290733
DOOR_PUBLIC_KEY = 15231938


def find_loop_size(public_key):
    loop_number = 0
    subject = 7
    number = 1
    while True:
        number *= subject
        number %= 20201227
        loop_number += 1

        if number == public_key:
            return loop_number


def apply_loop(subject, loop_number):
    number = 1

    for _ in range(loop_number):
        number *= subject
        number %= 20201227

    return number


if __name__ == '__main__':
    card_secret = find_loop_size(CARD_PUBLIC_KEY)
    encryption_key = apply_loop(DOOR_PUBLIC_KEY, card_secret)
    print(encryption_key)
