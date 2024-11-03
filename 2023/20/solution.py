from collections import deque, Counter

class Module:
    def __init__(self, name: str, outputs: list[str]) -> None:
        self.name = name
        self.outputs = outputs

    def receive_pulse(self, src: str, high: bool) -> list[tuple[str, bool]]:
        raise Exception('not implemented')


class Broadcaster(Module):
    def __init__(self, name: str, outputs: list[str]) -> None:
        super().__init__(name, outputs)

    def receive_pulse(self, src: str, high: bool) -> list[tuple[str, bool]]:
        return [(o, high) for o in self.outputs]


class FlipFlop(Module):
    def __init__(self, name: str, outputs: list[str]) -> None:
        super().__init__(name, outputs)
        self.on = False

    def receive_pulse(self, src: str, high: bool) -> list[tuple[str, bool]]:
        if high:
            return []
        self.on = not self.on
        return [(o, self.on) for o in self.outputs]


class Conjunction(Module):
    def __init__(self, name: str, outputs: list[str]) -> None:
        super().__init__(name, outputs)
        self.last_pulse = set()
        self.input_size = 0
    
    def set_input_size(self, input_size: int) -> None:
        self.input_size = input_size

    def receive_pulse(self, src: str, high: bool) -> list[tuple[str, bool]]:
        if high:
            self.last_pulse.add(src)
        elif src in self.last_pulse:
            self.last_pulse.remove(src)

        return [(o, len(self.last_pulse) != self.input_size) for o in self.outputs]


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

def count_conjunction_inputs(modules: list[Module]) -> None:
    inputs_count = Counter(output for module in modules for output in module.outputs)
    
    for module in modules:
        if not isinstance(module, Conjunction):
            continue
        module.set_input_size(inputs_count[module.name])
    
def run() -> None:
    modules_list = parse_modules()
    count_conjunction_inputs(modules_list)
    modules = {m.name: m for m in modules_list}

    high_pulses = 0
    low_pulses = 0
    for _ in range(1000):
        bus = deque([('', 'broadcaster', False)])
        while bus:
            sending_module_name, receiving_module_name, high_pulse = bus.popleft()
            high_pulses += high_pulse
            low_pulses += not high_pulse
            if receiving_module_name not in modules:
                continue
            module = modules[receiving_module_name]
            next_pulses = module.receive_pulse(sending_module_name, high_pulse)
            bus += [(receiving_module_name,) + np for np in next_pulses]

    print(f'{low_pulses} * {high_pulses}  = {low_pulses * high_pulses}')

run()
