import random as ric

ascii = list(range(32, 127)) + list(range(128, 255))  # to eliminate unwanted ascii character like del etc
s = str()
for r in ascii:
    s += chr(r)
s = list(s)  # s is our coustom ascii list


def encode(d):
    global S
    d = d
    b = str()
    g = ric.randint(0, 100)
    for r in d:
        c = s.index(r) + g
        # print(ord(r),c)
        b += s[c]
    b += s[g]  # the last character of the string is the encryption key
    return b


def decode(e):
    global S

    d = e
    b = str()
    i = s.index(d[len(d) - 1])  # converts the encryption key to the int value
    # print( i)
    for r in d:
        c = s.index(r) - i
        b += s[c]
        # print(ord(r),c)
    b = b[0:len(b) - 1]  # to remove key
    return b




