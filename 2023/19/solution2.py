import re

from collections import namedtuple

PartRange = namedtuple('PartRange', ['x', 'm', 'a', 's'])
Range = namedtuple('Range', ['start', 'end'])
Rule = namedtuple('Rule', ['split', 'target'])
Workflow = tuple[str, list[Rule]]


def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def parse_workflows(lines: list[str]):
    return [parse_workflow(l) for l in lines]

def parse_workflow(line: str) -> Workflow:
    name, rules_part = line[:-1].split('{')
    return name, [parse_rule(r) for r in rules_part.split(',')]

def split_range(subject_range: Range, cmp: str, value: int) -> tuple[Range | None, Range | None]:
    start, end = subject_range
    if cmp == '<': 
        if end < value:
            return subject_range, None
        if value <= start:
            return None, subject_range
        return Range(start, value-1), Range(value, end)
    
    if cmp == '>':
        if end <= value:
            return None, subject_range
        if value < start:
            return subject_range, None
        return Range(value+1, end), Range(start, value)
    
    raise Exception(':<')


def parse_rule(string: str):
    if ':' not in string:
        return Rule(split=lambda x: (x, None), target=string)
    
    almost_parsed_rule = re.search(r'(?P<subject>[xmas])(?P<cmp>[<>])(?P<value>\d+):(?P<target>\w+)', string)
    groups = almost_parsed_rule.groupdict()
    subject = groups['subject']
    cmp = groups['cmp']
    value = int(groups['value'])
    def split_function(part_range: PartRange) -> tuple[PartRange | None, PartRange | None]:
        part_range_dict = part_range._asdict()
        subject_range: Range = part_range_dict[subject]
        accepted_range, rejected_range = split_range(subject_range, cmp, value)
        accepted_part_range = PartRange(**(part_range_dict | {subject: accepted_range})) if accepted_range else None
        rejected_part_range = PartRange(**(part_range_dict | {subject: rejected_range})) if rejected_range else None
        
        return accepted_part_range, rejected_part_range

    return Rule(split=split_function, target=groups['target'])

def part_len(part_range: PartRange) -> int:
    diffs = [end-start+1 for start, end in part_range]
    return diffs[0] * diffs[1] * diffs[2] * diffs[3]

def run() -> None:
    lines = get_lines()
    split_point = lines.index('')

    workflows_list = parse_workflows(lines[:split_point])
    workflows = dict(workflows_list)
    accepted_ranges = []
    full_range = Range(start=1, end=4000)
    to_visit = [('in', PartRange(x=full_range, m=full_range, a=full_range, s=full_range))]

    while to_visit:
        workflow_name, part_range = to_visit.pop()
        if workflow_name == 'R':
            continue
        if workflow_name == 'A':
            accepted_ranges.append(part_range)
            continue

        for rule in workflows[workflow_name]:
            accepted, rejected = rule.split(part_range)
            to_visit.append((rule.target, accepted))
            part_range = rejected

    parts_count = sum(part_len(ar) for ar in accepted_ranges)
    print(parts_count)

run()
