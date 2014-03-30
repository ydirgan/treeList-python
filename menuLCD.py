from treeList import treeList
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep, time
import signal
import sys
import os

class menuLCD(treeList):

   OFFTIME = 20
   EXITFILE = '/tmp/menuLCD.exit'	
   
   def __init__(self):
      sleep(.5)
      self.lcd = Adafruit_CharLCDPlate(busnum=1)
      sleep(.5)
      self.lcd.begin(16, 2)
      sleep(.5)
      self.lcd.clear()
      self.lcd.message("Menu LCD library \nversion 1.0!")
      treeList.__init__(self)      
      self.button = ((self.lcd.SELECT, 'Select'),
                     (self.lcd.LEFT  , 'Left'  ),
                     (self.lcd.UP    , 'Up'    ),
                     (self.lcd.DOWN  , 'Down'  ),
                     (self.lcd.RIGHT , 'Right' ))     
      self.elapsed = 0 
      self.time2Sleep = 0
      self.displayOn = False

      if os.path.isfile(self.EXITFILE):
         os.remove(self.EXITFILE)
         
      sleep(1) 

##################################################################################################################
   def exitMenu(self):
      if self.ynQuestion('are you sure?'):
         self.shutdown()
         sys.exit(0)

##################################################################################################################
   def ynQuestion(self, text):
      self.lcd.clear()
      sleep(.1)
      self.lcd.message(text+'\n'+'left(n) right(y)')

      response = False
      exitLoop = False
      while not exitLoop:
         for btn in self.button:
            if self.lcd.buttonPressed(btn[0]):
               if btn[0] == self.lcd.RIGHT:
                  exitLoop = True
                  response = True
               if btn[0] == self.lcd.LEFT:
                  exitLoop = True
                  response = False
         sleep(.1)
                  
      return response

##################################################################################################################
   def keyUp(self):
      response = False
      for btn in self.button:
         if self.lcd.buttonPressed(btn[0]):
            if btn[0] == self.lcd.UP:
               response=True
      return response
                  
##################################################################################################################
   def keyDown(self):
      response = False
      for btn in self.button:
         if self.lcd.buttonPressed(btn[0]):
            if btn[0] == self.lcd.DOWN:
               response=True
      return response
                  
##################################################################################################################
   def keyRight(self):
      response = False
      for btn in self.button:
         if self.lcd.buttonPressed(btn[0]):
            if btn[0] == self.lcd.RIGHT:
               response=True
      return response
                  
##################################################################################################################
   def keyLeft(self):
      response = False
      for btn in self.button:
         if self.lcd.buttonPressed(btn[0]):
            if btn[0] == self.lcd.LEFT:
               response=True
      return response
                  
##################################################################################################################
   def keySelect(self):
      response = False
      for btn in self.button:
         if self.lcd.buttonPressed(btn[0]):
            if btn[0] == self.lcd.SELECT:
               response=True
      return response
                  
##################################################################################################################
   def keyPressed(self):
      response = False
      for btn in self.button:
         if self.lcd.buttonPressed(btn[0]):
            if btn[0] == self.lcd.RIGHT or btn[0] == self.lcd.LEFT or btn[0] == self.lcd.UP or btn[0] == self.lcd.DOWN:
               response=True
      return response
                  
##################################################################################################################
   def shutdown(self):
      self.turnOnDisplay()
      self.clearLCD()         
      self.message2LCD('Exiting...')
      sleep(2)      
      self.turnOffDisplay()

##################################################################################################################
   def setTime2Sleep(self,t): 
      self.OFFTIME = t
      
##################################################################################################################
   def message2LCD(self, msn):
      self.lcd.message(msn)

##################################################################################################################
   def clearLCD(self):
      self.lcd.clear()

##################################################################################################################
   def turnOffDisplay(self):     
      if self.displayOn:
         self.lcd.noDisplay()
         self.lcd.backlight(self.lcd.OFF)
         self.displayOn = False

##################################################################################################################
   def turnOnDisplay(self):
      if not self.displayOn:
         self.lcd.display()
         self.lcd.backlight(self.lcd.ON)
         self.displayOn = True
            
##################################################################################################################
   def resetTime2Sleep(self):
      self.elapsed = time()
      self.time2Sleep = 0

##################################################################################################################
   def lcdRefresh(self):
      self.turnOnDisplay()
      self.lcd.clear()
      sleep(.1)
      menuString = '%s\n[%s]'%(treeList.activeItemString(self),treeList.activePosition(self))
      self.lcd.message(menuString)
      sleep(.1)

##################################################################################################################
   def checkButtons(self):
      for btn in self.button:
         if self.lcd.buttonPressed(btn[0]):
            self.resetTime2Sleep()
            
            if self.displayOn:

               if btn[0] == self.lcd.RIGHT:
                  treeList.goNext(self)

               if btn[0] == self.lcd.LEFT:
                  treeList.goPrev(self)

               if btn[0] == self.lcd.DOWN:
                  if treeList.activeEntryHasItems(self): 
                     treeList.goDown(self)
                  else: 
                     treeList.goNext(self) 

               if btn[0] == self.lcd.UP:
                  treeList.goUp(self)

               if btn[0] == self.lcd.SELECT:
                  if treeList.typeOfActiveItem(self) == treeList.CMD:
                     treeList.activeAction(self)() 

            self.lcdRefresh()

##################################################################################################################
   def check2Sleep(self):
      if self.time2Sleep < self.OFFTIME:
         self.time2Sleep = time() - self.elapsed
      else:
         self.turnOffDisplay()   

##################################################################################################################
   def check4Exit(self):
      returnValue = True
      
      if os.path.isfile(self.EXITFILE):
         os.remove(self.EXITFILE)
         returnValue=False

      return returnValue   

##################################################################################################################
   def play(self):
      treeList.goTop(self)
      self.lcdRefresh()     
      self.resetTime2Sleep()
            
      while self.check4Exit():
         self.check2Sleep() 
         self.checkButtons()

      self.shutdown()
      sys.exit(0)   

##################################################################################################################
   def addExitEntry(self, *parentName):
      if len(parentName)>0:
         treeList.addItem(self,parentName[0],'Exit', self.exitMenu)
      else:
         treeList.addItem(self,treeList.ROOT,'Exit', self.exitMenu)          

##################################################################################################################         
def signal_handler(signal, frame):
   menu.shutdown()
   sys.exit(0)


##################################################################################################################         
def defineMenuItems(menu):
   menu.addItem(menu.ROOT,'Camera')
   menu.addItem('Camera','Setup Camera')
   menu.addItem('Camera','One Picture')
   menu.addItem('Camera','+ Pictures')
   self.addExitEntry('Exit', menu.exitMenu)

##################################################################################################################         
if __name__ == '__main__':

   signal.signal(signal.SIGINT, signal_handler)

   menu = menuLCD()
   defineMenuItems(menu) 
   menu.setTime2Sleep(15)
   menu.play()

