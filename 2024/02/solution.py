import itertools

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def is_safe(report: list[int]) -> bool:
    is_monotonic = report == sorted(report, reverse=report[0] > report[1])
    has_correct_increase = all(1 <= abs(x - y) <= 3 for x, y in  itertools.pairwise(report))
    return is_monotonic and has_correct_increase

def run() -> None:
    reports = [[int(x) for x in report_str.split()] for report_str in read_lines()]
    result = sum(is_safe(r) for r in reports)
    print(result)

run()
