list1=[1,2,3,4,5]
list2=[1,1,1,1,1]
j=0
for i in list1:
    list2[j]=i
    j+=1
print(list2)
list1.append(-1)
print(list2)