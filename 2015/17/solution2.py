def number_of_combinations(liquid, containers):
    dp = [[0] * (len(containers) + 1) for _ in range(liquid + 1)]
    dp[0][0] = 1

    for container in containers:
        prev_dp = dp
        dp = [[0] * (len(containers) + 1) for _ in range(liquid + 1)]
        dp[0][0] = 1

        for idx in range(1, liquid + 1):
            if idx - container < 0:
                dp[idx] = prev_dp[idx]
                continue
            for containers_number in range(1, len(containers) + 1):
                # print(idx, containers_number)
                dp[idx][containers_number] = prev_dp[idx][containers_number] + prev_dp[idx - container][containers_number - 1]

    return first_nonzero(dp[-1][1:])

def first_nonzero(array):
    for item in array:
        if item == 0:
            continue
        return item

    raise Exception('Not found')


containers = [43, 3, 4, 10, 21, 44, 4, 6, 47, 41, 34, 17, 17, 44, 36, 31, 46, 9, 27, 38]
liquid = 150

result = number_of_combinations(liquid, containers)
print(result)
