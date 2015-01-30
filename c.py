__author__ = 'anandhakumar'


def fib():
    a=0
    b=1
    print a,b,
    for i in range(20):
        c=a+b
        a=b
        b=c
        print c,


fib()

num=6

for i in range(2,num):
    if (num % i) == 0:
        print(num,"is not a prime number")
        print(i,"times",num//i,"is",num)
        break
else:
    print "on"


num=7
c=1
for i in range(1,num+1):
    c*=i
print c

x=range(30)
print x
print x[::-1]

x=['annad','aaaaaadddddd','ffffff','rrllll']
print x
x.reverse()
print x
print x[::-1]
print [x[i][::-1] for i in range(len(x))]


# bfs
# linked list
# tree
