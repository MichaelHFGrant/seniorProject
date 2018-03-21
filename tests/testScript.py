#! /usr/bin/python3.5

import queue

newItem = 'hello'
nextItem = 'bye'
newQueue = queue.queue(newItem)
newQueue.push(nextItem)
x=0
while (x<10): 
   newQueue.push(x)
   x=x+1
item = newQueue.pop()
print(item)
item = newQueue.pop()
print(item)
item = newQueue.pop()
print(item)
item = newQueue.pop()
print(item)
item = newQueue.pop()
print(item)
item = newQueue.pop()
print(item)
