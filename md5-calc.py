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

from math import sin, floor


def bitwise_not(n):
    temp = "{0:b}".format(n).replace("0", "x").replace("1", "0").replace("x", "1")
    return int(temp, 2)


class MD5:

    def __init__(self, message="MD5"):
        self.message = message
        self.a = "01234567"
        self.b = "89abcdef"
        self.c = "fedcba98"
        self.d = "76543210"
        self.bin_message = self.message_padding()
        self.message_array = self.create_message_array()
        self.shift_amount = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    def message_padding(self):
        bin_message = ''.join([format(ord(i), 'b').zfill(8) for i in self.message])
        bin_message += "10000000"
        bin_message += "0" * (448 - len(bin_message))
        bin_message += format(len(self.message) * 8, 'b').zfill(64)

        assert len(bin_message) == 512

        return str(bin_message)

    def create_message_array(self):
        bin_msg = [self.bin_message[i:i + 32] for i in range(0, 512, 32)]
        return [hex(int(i, 2))[2:].zfill(8) for i in bin_msg]

    def f(self):
        return hex((int(self.b, 16) & int(self.c, 16)) | (bitwise_not(int(self.b, 16)) & int(self.d, 16)))[2:].zfill(8)

    def g(self):
        return hex((int(self.b, 16) & int(self.d, 16)) | (int(self.c, 16) & bitwise_not(int(self.d, 16))))[2:].zfill(8)

    def h(self):
        return hex(int(self.b, 16) ^ int(self.c, 16) ^ int(self.d, 16))[2:].zfill(8)

    def i(self):
        return hex(int(self.c, 16) ^ (int(self.b, 16) | bitwise_not(int(self.d, 16))))[2:].zfill(8)

    def mod_add(self, x, y):
        x = int(x, 16)
        y = int(y, 16)
        z = pow(2, 32)

        return hex((x + y) % z)[2:].zfill(8)

    def constant(self, i):
        return hex(floor(abs(sin(i + 1)) * pow(2, 32)))[2:].zfill(8)

    def bitshift(self, n, i):
        temp = int(n, 16)

        temp = ((temp << self.shift_amount[i]) & 0xFFFFFFFF) | (temp >> (32 - self.shift_amount[i]))
        return hex(temp)[2:].zfill(8)



    def round1(self):
        for i in range(16):
            self.a = self.mod_add(self.a, self.f())
            self.a = self.mod_add(self.a, self.message_array[i])
            self.a = self.mod_add(self.a, self.constant(i))
            self.a = self.bitshift(self.a, i)
            self.a = self.mod_add(self.a, self.b)

            self.a, self.b, self.c, self.d = self.d, self.a, self.b, self.c

    def round2(self):
        for i in range(16, 32):
            self.a = self.mod_add(self.a, self.g())
            self.a = self.mod_add(self.a, self.message_array[(1 + 5 * i) % 16])
            self.a = self.mod_add(self.a, self.constant(i))
            self.a = self.bitshift(self.a, i)
            self.a = self.mod_add(self.a, self.b)
            self.a, self.b, self.c, self.d = self.d, self.a, self.b, self.c

    def round3(self):
        for i in range(32, 48):
            self.a = self.mod_add(self.a, self.h())
            self.a = self.mod_add(self.a, self.message_array[(5 + 3 * i) % 16])
            self.a = self.mod_add(self.a, self.constant(i))
            self.a = self.bitshift(self.a, i)
            self.a = self.mod_add(self.a, self.b)

            self.a, self.b, self.c, self.d = self.d, self.a, self.b, self.c

    def round4(self):
        for i in range(48, 64):
            self.a = self.mod_add(self.a, self.i())
            self.a = self.mod_add(self.a, self.message_array[(7 * i) % 16])
            self.a = self.mod_add(self.a, self.constant(i))
            self.a = self.bitshift(self.a, i)
            self.a = self.mod_add(self.a, self.b)

            self.a, self.b, self.c, self.d = self.d, self.a, self.b, self.c


    def md5(self):
        self.round1()
        self.round2()
        self.round3()
        self.round4()

        print("gamererre " + self.a + " " + self.b + " " + self.c + " " + self.d)

        oiva = "01234567"
        oivb = "89abcdef"
        oivc = "fedcba98"
        oivd = "76543210"

        self.a = self.mod_add(self.a, oiva)
        self.b = self.mod_add(self.b, oivb)
        self.c = self.mod_add(self.c, oivc)
        self.d = self.mod_add(self.d, oivd)

        return self.a + " " + self.b + " " + self.c + " " + self.d


def main():
    calc_hash = MD5("MD5")

    print(calc_hash.md5())


if __name__ == "__main__":
    main()
