s = "abcdefg"
b_s = bytearray(s)
b_s[1] = "Z"
s = str(b_s)
print s
