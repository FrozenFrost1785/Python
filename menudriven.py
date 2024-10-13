a=int(input("Enter value for a : "))
b=int(input("Enter value for b : "))
while True:
    print (" \n 1.Addition")
    print (" \n 2.Subtraction")
    print (" \n 3.Exit     ")
    ch=int(input("Enter choice code: "))
    if (ch==3):
       print("PROGRAM EXECUTED")
       break
    elif (ch==1):
       print("Addition is ",a+b)
    elif (ch==2):
       print("Subtraction is ",a-b)
    else:
       print("Wrong choice code!!!")    

