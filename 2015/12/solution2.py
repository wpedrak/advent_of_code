import json


def get_line(filename='12/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()][0]


def sum_numbers(json_data):
    if type(json_data) == int:
        return json_data

    if type(json_data) == list:
        result = 0
        for item in json_data:
            result += sum_numbers(item)
        return result

    if type(json_data) == dict:
        result = 0
        for item in json_data.values():
            if item == "red":
                return 0
            result += sum_numbers(item)
        return result

    return 0


data = json.loads(get_line())
result = sum_numbers(data)

print(result)
