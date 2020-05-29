f1=open("text.txt", "r")
    if f1.mode == 'r':
        s = f1.read()
b_s = bytearray(s)
b_s[1] = "Z"
s = str(b_s)
print s
