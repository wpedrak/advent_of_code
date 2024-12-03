import re

def run() -> None:
    memory = open('input.txt', 'r', encoding='utf-8').read()
    result = sum(int(m[1]) * int(m[2]) for m in re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', memory))
    print(result)
        
run()
