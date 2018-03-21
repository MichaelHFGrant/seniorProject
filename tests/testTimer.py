#! /usr/bin/python3.5
import timer
import threading
#def timer():
#   print 'Timer Function'
#   return

def main():
   if __name__=='__main__':
      for i in range(3):
         t= threading.Thread(target=timer.timer)
         t.start()

main()   
