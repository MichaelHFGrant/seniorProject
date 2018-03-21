class node:
   def __init__(self,item):
      self.data = item
      self.next = 'null'

   def setData(item):
      self.data = item

   def setNext(item):
      self.next = item

   def getData():
      return self.data


class queue:
   def __init__(self,item):
      self.head =  node(item)
      self.head.setNext('null')
      self.tail = node(item)  
      self.tail.setnext('null')


   def pop(self):
      value = self.head.getData()
      self.head = self.next
      return value

   def push(self,newItem):
      newNode = node(newItem)
      self.next = newNode
      self.tail = self.next
        
      
