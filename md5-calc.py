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


class MD5:

    def __init__(self, message="Gustavs MD5 SOP"):
        self.message = message
        self.a = int("01234567", 16)
        self.b = int("89abcdef", 16)
        self.c = int("fedcba98", 16)
        self.d = int("76543210", 16)
        self.bin_message = self.message_padding()
        self.message_array = self.message_array()

    def message_padding(self):
        bin_message = ''.join(format(ord(i), 'b').zfill(8) for i in self.message)
        bin_message += "10000000"
        bin_message += "0" * (448 - len(bin_message))
        bin_message += format(len(self.message) * 8, 'b').zfill(64)

        assert len(bin_message) == 512

        return bin_message

    def message_array(self):
        bin_msg = [self.bin_message[i:i+32] for i in range(0, 512, 32)]
        return [hex(int(i, 2))[2:].zfill(8) for i in bin_msg]


    def f(self):
        return hex((self.b & self.c) | (~self.b & self.d))[2:]

    def moda(self, x, y, z="100000000"):
        x = int(x, 16)
        y = int(y, 16)
        z = int(z, 16)
        return hex((x + y) % z)[2:]

    def constant(self, i):
        return hex(int(abs(sin(i + 1)) * 2 ** 32))[2:]

    def bitshift(self, n):
        temp = int(n, 16)
        return hex(temp << 7 | temp >> 25)[4:]






"""
print(MD5().f())

print(MD5().moda("01234567", "fedcba98"))
print(MD5().moda("54686579", "ffffffff"))

print(MD5().moda(MD5().constant(0), "54686578"))

print(MD5().bitshift("2bd309f0"))

print(MD5().moda("e984f815", "89abcdef"))


print(MD5().message_array)

"""

