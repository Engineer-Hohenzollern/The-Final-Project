# we are creating custom ascii list by elimination problematic characters like del etc. we use this list for
# encryption and decryption by random shift value from 0 to 100
from random import *

ascii = list(range(32, 127)) + list(range(128, 255))  # to eliminate unwanted ascii character like del etc
# ⤴️we create a list of numbers which represents ascii value of the characters we create
s = str()
for r in ascii:
    s += chr(r)
s = list(s)  # s is our custom ascii list


def encode(d):
    global s
    d = d
    b = str()
    g = randint(0, 100)
    for r in d:
        c = s.index(r) + g
        # print(ord(r),c)
        b += s[c]
    b += s[g]  # the last character of the string is the encryption key
    return b


def decode(e):
    global s

    d = e
    b = str()
    i = s.index(d[len(d) - 1])  # converts the encryption key to the int value
    # print( i)
    for r in d:
        c = s.index(r) - i
        b += s[c]

    b = b[0:len(b) - 1]  # to remove key
    return b
