x=int(input("Enter the number="))
i=0
j=1
sum=0
count=0
while(count<x):
    print(sum,end=" ")
    i=j
    j=sum
    sum=i+j
    count=count+1


