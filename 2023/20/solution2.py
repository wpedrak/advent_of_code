import math

from collections import deque, Counter
import networkx as nx
import matplotlib.pyplot as plt


plt.figure(figsize=(20, 12), dpi=200)


class Module:
    def __init__(self, name: str, outputs: list[str]) -> None:
        self.name = name
        self.outputs = outputs
        self.inputs = []

    def receive_pulse(self, src: str, high: bool) -> list[tuple[str, bool]]:
        raise Exception('not implemented')
    
    def state(self) -> str:
        raise Exception('not implemented')


class Broadcaster(Module):
    def __init__(self, name: str, outputs: list[str]) -> None:
        super().__init__(name, outputs)

    def receive_pulse(self, src: str, high: bool) -> list[tuple[str, bool]]:
        return [(o, high) for o in self.outputs]
    
    def state(self) -> str:
        return ''


class FlipFlop(Module):
    def __init__(self, name: str, outputs: list[str]) -> None:
        super().__init__(name, outputs)
        self.on = False

    def receive_pulse(self, src: str, high: bool) -> list[tuple[str, bool]]:
        if high:
            return []
        self.on = not self.on
        return [(o, self.on) for o in self.outputs]

    def state(self) -> str:
        return self.name + ':' + ['OFF', 'ON'][self.on]

class Conjunction(Module):
    def __init__(self, name: str, outputs: list[str]) -> None:
        super().__init__(name, outputs)
        self.last_pulse = set()
    
    def set_input_size(self, input_size: int) -> None:
        self.input_size = input_size

    def receive_pulse(self, src: str, high: bool) -> list[tuple[str, bool]]:
        if high:
            self.last_pulse.add(src)
        elif src in self.last_pulse:
            self.last_pulse.remove(src)

        return [(o, len(self.last_pulse) != len(self.inputs)) for o in self.outputs]
    
    def state(self) -> str:
        return f'{self.name}:{sorted(self.last_pulse)}'


def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def parse_modules() -> list[Module]:
    return [parse_module(l) for l in get_lines()]

def parse_module(line: str) -> Module:
    name_part, destinations_part = line.split(' -> ')
    module_creator = {
        'b': Broadcaster,
        '%': FlipFlop,
        '&': Conjunction,
    }[name_part[0]]
    name = name_part if module_creator == Broadcaster else name_part[1:]
    outputs = destinations_part.split(', ')

    return module_creator(name, outputs)

def fill_inputs(modules: dict[str, Module]) -> None:
    for module in modules.values():
        for output_name in module.outputs:
            if output_name == 'rx':
                continue
            modules[output_name].inputs.append(module)
    
def fresh_modules() -> dict[str, Module]:
    modules_list = parse_modules()
    modules = {m.name: m for m in modules_list}
    fill_inputs(modules)
    return modules

def push_the_button(modules: dict[str, Module], observer: str) -> bool:
    bus = deque([('', 'broadcaster', False)])
    seen_low_pulse = False
    while bus:
        sending_module_name, receiving_module_name, high_pulse = bus.popleft()
        if sending_module_name == observer and not high_pulse:
            seen_low_pulse = True
        if receiving_module_name not in modules:
            continue
        module = modules[receiving_module_name]
        next_pulses = module.receive_pulse(sending_module_name, high_pulse)
        bus += [(receiving_module_name, next_receiver, high) for next_receiver, high in next_pulses]

    return seen_low_pulse

def extract_group(modules: dict[str, Module], pivot: str) -> dict[str, Module]:
    pivot_module = modules[pivot]
    neighbours = set(pivot_module.inputs + [modules[o] for o in pivot_module.outputs])
    return {n.name: n for n in neighbours if isinstance(n, FlipFlop)} | {'broadcaster': modules['broadcaster']} | {pivot: pivot_module}

def state(modules: dict[str, Module]) -> frozenset[str]:
    return frozenset(m.state() for m in modules.values())

def find_low_pulse(pivot: str) -> int:
    modules = fresh_modules()
    group = extract_group(modules, pivot)

    low_pulses = []
    seen_states = set()
    first_state = state(group)
    pushes = 0

    while state(group) not in seen_states:
        seen_states.add(state(group))
        pushes += 1
        if push_the_button(group, pivot):
            low_pulses.append(pushes)

    # the cycle ends in the "all off" state        
    assert first_state == state(group)

    # there is only one low pulse in the cycle
    assert len(low_pulses) == 1

    # low pulse is at the end of the cycle
    assert pushes == low_pulses[0]
 
    return low_pulses[0]

def run() -> None:
    pivots = ['sd', 'db', 'qz', 'lx'] # see graph.png
    pulses = [find_low_pulse(p) for p in pivots]

    print(math.lcm(*pulses))

def visualise() -> None:
    modules = parse_modules()

    G = nx.DiGraph()
    G.add_nodes_from([m.name for m in modules] + ['rx'])
    for module in modules:
        G.add_edges_from((module.name, o) for o in module.outputs)

    colors = {
        Conjunction: "green",
        FlipFlop: "cyan",
        Broadcaster: "red"
    }
    nx.draw_planar(G, with_labels=True, arrows=True, node_color=[colors[type(m)] for m in modules] + ["red"])
    plt.savefig("graph.png")


run()
# visualise()
