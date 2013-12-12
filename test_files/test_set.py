from sets import Set

s1 = Set()

s1.add(1)
s1.add(1)
s1.add(1)
s1.add(2)

s2 = Set()
s2.add(1)
s2.add(2)

s3 = Set()
s3.add(2)
s3.add(3)

s4 = set()
s4.add(3)
s4.add(4)
s4.add(4)

s5 = frozenset(s4)

print s1
print s2
print s3
print s4

d = {}
#d[s1] = "one and two"
d[s5] = "three and four"


print d
