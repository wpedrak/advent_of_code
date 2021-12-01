def get_line(filename='input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()][0]


text = get_line()
balance = 0

for idx, letter in enumerate(text):
    balance += letter == '('
    balance -= letter == ')'

    if balance == -1:
        print(idx + 1)
        break
