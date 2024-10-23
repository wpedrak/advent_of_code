import re

from collections import namedtuple

Part = namedtuple('Part', ['x', 'm', 'a', 's'])
Rule = namedtuple('Rule', ['cmp', 'target'])
Workflow = tuple[str, list[Rule]]


def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def parse_workflows(lines: list[str]):
    return [parse_workflow(l) for l in lines]

def parse_workflow(line: str) -> Workflow:
    name, rules_part = line[:-1].split('{')
    return name, [parse_rule(r) for r in rules_part.split(',')]

def parse_rule(string: str):
    if ':' not in string:
        return Rule(cmp=lambda x: True, target=string)
    
    almost_parsed_rule = re.search(r'(?P<subject>[xmas])(?P<cmp>[<>])(?P<value>\d+):(?P<target>\w+)', string)
    groups = almost_parsed_rule.groupdict()
    def cmp_function(part: Part) -> bool:
        subject = part._asdict()[groups['subject']]
        value = int(groups['value'])
        if groups['cmp'] == '<':
            return subject < value
        if groups['cmp'] == '>':
            return subject > value
        raise Exception(':<')

    return Rule(cmp=cmp_function, target=groups['target'])

def parse_parts(lines: list[str]):
    return [parse_part(l) for l in lines]

def parse_part(line: str):
    matched_part = re.search(r'{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}', line)
    return Part(**{k: int(v) for k, v in matched_part.groupdict().items()})

def process(workflows: dict[str, list[Rule]], part: Part) -> str:
    workflow = 'in'

    while workflow not in 'AR':
        for cmp, target in workflows[workflow]:
            if not cmp(part):
                continue

            workflow = target
            break

    return workflow

def run() -> None:
    lines = get_lines()
    split_point = lines.index('')

    workflows_list = parse_workflows(lines[:split_point])
    workflows = dict(workflows_list)
    parts = parse_parts(lines[split_point+1:])

    result = 0
    for part in parts:
        if process(workflows, part) == 'R':
            continue

        result += sum(part)
    
    print(result)

run()
