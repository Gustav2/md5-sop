"""
Original input: Gustavs MD5 SOP

Binary: len = 120. Padding needed = 448-1-120=327

M0 - M15
01000111 01110101 01110011 01110100 
01100001 01110110 01110011 00100000 
01001101 01000100 00110101 00100000 
01010011 01001111 01010000 10000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 00000000 
00000000 00000000 00000000 01111000

47757374
61767320
4d443520
534f5080
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000078


Init vector:
A – 01234567
B – 89abcdef
C – fedcba98
D – 76543210

"""

from math import sin


def f(b, c, d):
    b = int(b, 16)
    c = int(c, 16)
    d = int(d, 16)
    return hex((b & c) | (~b & d))

print(f("89abcdef", "fedcba98", "76543210"))

def moda(x, y, z = "100000000"):
    x = int(x, 16)
    y = int(y, 16)
    z = int(z, 16)
    return hex((x + y) % z) 

def constant(i):
    return hex(int(abs(sin(i + 1)) * 2**32)) 

print(moda("54686579", "ffffffff"))

print(moda(constant(0), "54686578"))

def bitshift(n):


print(bin())