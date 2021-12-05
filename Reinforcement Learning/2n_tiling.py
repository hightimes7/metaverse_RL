# 2xn Tiling with 2x1 tiles and 2x2 tiles
# T(n) = T(n-1) + 2T(n-2)

# 수학적 접근
n = int(input('n = '))
print((2**(n+1) + (-1)**n)//3)

'''
# 재귀
def Tiling(n):
    if n == 1: return 1
    if n == 2 : return 3
    return Tiling(n-1) + 2*Tiling(n-2)

n = int(input('n = '))
print(Tiling(n))
'''        
