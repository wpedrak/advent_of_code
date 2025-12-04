result = 0
cnt = 5

for id_range in open('input.txt', 'r').read().strip().split(','):
    start, end = map(int, id_range.split('-'))
    start_str = str(start)
    found: set[str] = set()
    for sequence_len in range(1, len(str(end))//2 + 1):
        repeat_counts = [cnt for cnt in range(2, len(str(end))+1) if len(str(start)) <= sequence_len * cnt <= len(str(end))]
        for repeat_count in repeat_counts:
            sequence = '1' + '0' * (sequence_len-1)
            while len(sequence) == sequence_len:
                current_id = sequence * repeat_count
                if start <= int(current_id) <= end and current_id not in found:
                    found.add(current_id)
                    result += int(sequence * repeat_count)
                sequence = str(int(sequence) + 1)

print(result)
