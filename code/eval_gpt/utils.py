def edit_distance_integers(a, b):

    a = str(a)
    b = str(b)

    m = len(a)
    n = len(b)

    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

    return dp[m][n]


def length_longest_nondecreasing_subsequence(nums):

    n = len(nums)

    dp = [1 for _ in range(n)]

    for i in range(1, n):
        for j in range(i):
            if nums[i] >= nums[j]:
                dp[i] = max(dp[i], 1 + dp[j])

    return max(dp)