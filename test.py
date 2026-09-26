#add x1, x2, x3
y="add     x1,   x2     ,     x3"
l=y.split(" ")
l1=[]
for i in l:
    if i=="":
        l.remove(i)
print(l)