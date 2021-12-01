class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        return f'<{self.value}>'

    def __repr__(self):
        return str(self)


def create_circle(size):
    mapping = {}

    for number in range(1, size + 1):
        mapping[number] = Node(number)

    for number, node in mapping.items():
        next_number = number % size + 1
        prev_number = (number - 2) % size + 1
        node.prev = mapping[prev_number]
        node.next = mapping[next_number]

    return mapping


def override_circle_beginning(circle_mapping, beginning):
    current_node = circle_mapping[1]
    for number in beginning:
        current_node.value = number
        circle_mapping[number] = current_node
        current_node = current_node.next


def take_three(current_cup):
    first_taken_cup = current_cup.next
    last_taken_cup = first_taken_cup.next.next

    current_cup.next = last_taken_cup.next
    last_taken_cup.next.prev = current_cup
    first_taken_cup.prev = None
    last_taken_cup.next = None

    return first_taken_cup, last_taken_cup


def get_destination_cup(circle, first_taken_cup, current_node):
    taken_values = [
        first_taken_cup.value,
        first_taken_cup.next.value,
        first_taken_cup.next.next.value,
    ]

    circle_size = len(circle)

    destination_cup_number = (current_node.value - 1)
    destination_cup_number = (destination_cup_number - 1) % circle_size + 1
    while destination_cup_number in taken_values:
        destination_cup_number -= 1
        destination_cup_number = (destination_cup_number - 1) % circle_size + 1

    return circle[destination_cup_number]


def insert_cups(destination_cup, first_taken_cup, last_taken_cup):
    after_insert_node = destination_cup.next

    destination_cup.next = first_taken_cup
    after_insert_node.prev = last_taken_cup
    first_taken_cup.prev = destination_cup
    last_taken_cup.next = after_insert_node


def get_next(current_node):
    return current_node.next


if __name__ == '__main__':
    cups_beginning = [1, 5, 6, 7, 9, 4, 8, 2, 3]
    circle = create_circle(10 ** 6)
    override_circle_beginning(circle, cups_beginning)
    current_node_number = cups_beginning[0]
    current_node = circle[current_node_number]

    for move_number in range(10 ** 7):
        if not move_number % 10000:
            print(move_number // 10000, '/', 10 ** 7 // 10000)
        first_taken_cup, last_taken_cup = take_three(current_node)
        destination_cup = get_destination_cup(circle, first_taken_cup, current_node)
        insert_cups(destination_cup, first_taken_cup, last_taken_cup)
        current_node = get_next(current_node)

    node1 = circle[1].next
    node2 = node1.next

    print(node1.value * node2.value)
