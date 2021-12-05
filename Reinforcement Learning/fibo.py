# 수학적 접근
#fib(n) = fib(n-1) + fib(n-2)
#x^2 = x + 1
#x = (1 +/- root(1^2 + 4))/2
#alpha = (1+root(5))/2
#beta = (1-root(5))/2

import math
Sqrt5 = math.sqrt(5)
Phi = (1+Sqrt5)/2
def fib(n):
    return int((Phi**n - (1-Phi)**n)/Sqrt5 + 0.5)

n = int(input('n = '))
print(fib(n))

'''
# 철수와 영희 계단 오르기 (철수는 1칸, 영희는 5칸)
def stepp(dp, s):
    if s[0] == 10: return 1.0
    if s[1] == 10: return 0.0
    if s in dp: return dp[s]
    dp[s] = (2*stepp(dp, (s[0]+1, s[1])) + stepp(dp, (s[0], s[1]+1)))/3
    return dp[s]

dp = dict()
print(stepp(dp, (1,5)))

# 동적 프로그래밍
def fib(dp, n):
    if n == 0 : return 0
    if n == 1 : return 1
    if n in dp : return dp[n]
    dp[n] = fib(dp, n-1) + fib(dp, n-2)
    return dp[n]
dp = dict()
n = int(input('n = '))
print(fib(dp, n))


# 반복
def fib(n):
    f = [0, 1]
    for _ in range(2, n+1, 2):
        f[0] += f[1]
        f[1] += f[0]
    return f[n%2]

# 재귀
def fib(n):
    if n == 0 : return 0
    if n == 1 : return 1
    return fib(n-1)+fib(n-2)

n = int(input('n = '))
print(fib(n))
'''
