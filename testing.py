#!/usr/bin/env python
# with is like your try .. finally block in this case
with open('stats.txt', 'r') as file:
    # read a list of lines into data
    data = file.readlines()

print data
print "Your name: " + data[0]

# now change the 2nd line, note that you have to add a newline
data[1] = 'Mage\n'

# and write everything back
with open('stats.txt', 'w') as file:
    file.writelines( data )
