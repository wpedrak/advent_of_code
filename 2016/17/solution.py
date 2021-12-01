def number_of_combinations(liquid, containers):
    dp = [1] + [0] * liquid

    for container in containers:
        prev_dp = dp
        dp = [1] + [0] * liquid

        for idx in range(1, liquid + 1):
            if idx - container < 0:
                dp[idx] = prev_dp[idx]
                continue
            dp[idx] = prev_dp[idx] + prev_dp[idx - container]

    return dp[-1]


containers = [43, 3, 4, 10, 21, 44, 4, 6, 47, 41, 34, 17, 17, 44, 36, 31, 46, 9, 27, 38]
liquid = 150

result = number_of_combinations(liquid, containers)
print(result)
