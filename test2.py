y=0
properformat=""
properformattemp2="xxxxx"
for w in properformattemp2:
    if w in ["x","X"]:
        if y==2:
            properformat+="z"
        else:
            properformat+=w
            y+=1
    else:
        properformat+=w
print(properformat)