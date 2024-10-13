class data:
    def __init__(self,name,phone):
        self.name=name
        self.phone=phone

"""
def quadratic_probing():
    size=int(input("Enter the size of the hash table:"))
    hashtable=[None for i in range(size)]
    n=int(input("Enter the no of records:"))
    for i in range(n):
        name=input("Enter the name of the record:")
        phone=int(input("Enter the phone no of the record:"))
        hashvalue=phone%size
        if(hashtable[hashvalue] is None):
            hashtable[hashvalue]=hashtable(name,phone)
        elif(hashtable[hashvalue] is not None):

return hashtable
"""
def display_hash(hashtable):
    print("Name:\tPhone:\t")
    for i in hashtable:
        if(i is None):
            print("--\t--")
        if(i is not None):
            print(i.name,"\t",i.phone)


def double_hash():
    size=int(input("Enter the size of the hash table:"))
    hashtable1=[None for i in range(size)]
    hashtable2=[None for i in range(size)]
    n=int(input("Enter the no of records:"))
    for i in range(n):
        name=input("Enter the name of the record:")
        phone=int(input("Enter the phone no of the record:"))
        hashkey1=phone%size
        hashkey2=((hashkey1+7)*(hashkey1+7)+11)%size
        if(hashtable2[hashkey2] is None):
            hashtable2[hashkey2]=data(name,phone)
        else:
            for i in range(1,10):
                hashkey2=(hashkey1+i)%size
                if(hashtable2[hashkey2] is None):
                    hashtable2[hashkey2]=data(name,phone)
                    break
    return hashtable2



def linear_probing():
    size=int(input("Enter the size of the hash table:"))
    hashtable=[None for i in range(size)]
    n=int(input("Enter the no of records:"))
    for i in range(n):
        name=input("Enter the name of the record:")
        phone=int(input("Enter the phone no:"))
        hashvalue=phone%size
        if(hashtable[hashvalue] is None):
            hashtable[hashvalue]=data(name,phone)
        else:
            for i in range(1,10):
                hashvalue=(phone+i)%size
                if(hashtable[hashvalue] is None):
                    hashtable[hashvalue]=data(name,phone)
                    break
    return hashtable


def main():
    while True:
        hash1=[None for i in range(10)]
        choice=input("Enter your option(L/D/E):")
        if(choice=='L'):
            hash1=linear_probing()
            display_hash(hash1)
        elif(choice=='D'):
            hash1=double_hash()
            display_hash(hash1)
        elif(choice=='E'):
            quit()
        else:
            print("Wrong choice")




main()