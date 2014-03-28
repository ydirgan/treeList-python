import os
class treeList:
   #constants no to be modified
   MLEVEL  = 0
   MITEMS  = 1  
   ##Aditional information can be added here ###
   MACTIVE = 2
   NEXTFIELD = 3
   #############################################
   MLABEL  = NEXTFIELD
   MACTION = NEXTFIELD+1
   MOFFSET = NEXTFIELD+1
  
   MAXLEVEL = 0  
   INACTIVE=False  
   ROOT = 'Root'
   CMD = 'Command'

######################################################################################
## INIT class treelist                                                              ##
## Creates a empty list that is defined to have only a root entry                   ##
## Structure: [level, number of items, label/list]                                  ##
## Example: List with a second level which contains 4 entries                       ##
## [0, 4, 'Root', [1, 0, 'File'], [1, 0, 'Edit'], [1, 0, 'Tools'], [1, 0, 'Help']]  ##
## Example: Open, Save Items added to File Entry                                    ##
## [1, 2, 'File', [2, -1, 'Open', 'command'], [2, -1, 'Save', 'command']]           ##
######################################################################################
   def __init__(self):
      self.menu = [0,0,self.INACTIVE,self.ROOT] #mod
      self.CURRENTLEVEL = self.menu
      self.CURRELEMENT = self.MOFFSET   
      self.ACTIVEITEM = list()     
      self.CURRENTLEVELTYPE = self.ROOT
      self.trace = list()
      self.EMPTY = True;
      self.MAINCOUNT = 0
      self.INIT = False
     
      self.PUSHDATA=[self.CURRENTLEVEL, self.CURRELEMENT, self.ACTIVEITEM]    


######################################################################################
##  This is a dummy method for demostration purposes                                ##
######################################################################################
   def dummyMethod(self):
      pass

######################################################################################
##  Set active the first element of the first level                                 ##
######################################################################################
   def goTop(self):
      self.setActiveOff()
      self.CURRENTLEVEL = self.menu
      self.trace = list()
      self.goItemIndex(0)
      self.setActiveOn()
     
           
######################################################################################
##  Fill dummy list using a menu as example                                         ##
######################################################################################
   def fillDummyItems(self):
      self.addItem(self.ROOT,'File')
      self.addItem('File','Open', self.dummyMethod)
      self.addItem('File','Save', self.dummyMethod)
      self.addItem('File','Save as...', self.dummyMethod)

      self.addItem(self.ROOT,'Edit')
      self.addItem('Edit','Copy', self.dummyMethod)
      self.addItem('Copy','Copy to', self.dummyMethod)
      self.addItem('Copy to','To a file', self.dummyMethod)
      self.addItem('Copy to','To dropbox', self.dummyMethod)
      self.addItem('Copy','Copy from', self.dummyMethod)
      self.addItem('Copy from','From file')
      self.addItem('Copy from','From dropbox', self.dummyMethod)

      self.addItem('Edit','Cut', self.dummyMethod)
      self.addItem('Edit','Paste')

      self.addItem(self.ROOT,'Tools')
      self.addItem(self.ROOT,'Help')

      self.addItem('Help','About...')

######################################################################################
##  Add item finding its parent recursively                                         ##
##  restriction: items added must have a unique label                               ##
##                                                                                  ##
##  example: additem(object.ROOT, 'File')                                           ##
##           add item to a object.ROOT (first level)                                ##
##  example: additem('File', 'Save', saveCommand)                                   ##
##           add item to File entry and assign a procedure to it                    ##
##                                                                                  ##
######################################################################################
   def addItem(self,parent,item,*command):
      if len(command) == 0:
         cmd=''
      else:
         cmd=command[0]

      self.find2add(self.menu, parent, item, cmd)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   def find2add(self, array, parent, item, command):
      if array[self.MLABEL] == parent:   
         #Have a command already?
         if array[self.MITEMS] == -1:
            del array[-1]
            array[self.MITEMS] = 0
              
         #append item
         if command == '':
            array.append([array[self.MLEVEL]+1,0,self.INACTIVE,item])
         else:
            array.append([array[self.MLEVEL]+1,-1,self.INACTIVE,item,command])

         #update maxlevel actually appended
         if array[self.MLEVEL]+1 > self.MAXLEVEL:
            self.MAXLEVEL = array[self.MLEVEL]+1

         array[self.MITEMS] +=1

         self.EMPTY = False
         if parent == self.ROOT: self.MAINCOUNT += 1
         if not self.INIT:
            self.INIT = True
            self.CURRELEMENT = self.MOFFSET
            self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
            self.setActiveOn()

      else:    
         for entry in array[self.MOFFSET:]:
            #if found it
            if entry[self.MLABEL] == parent:
               #Have a command already?
               if entry[self.MITEMS] == -1:
                  del entry[-1]
                  entry[self.MITEMS] = 0
              
               #append item
               if command == '':
                  entry.append([entry[self.MLEVEL]+1,0,self.INACTIVE,item])
               else:
                  entry.append([entry[self.MLEVEL]+1,-1,self.INACTIVE,item,command])

               if entry[self.MLEVEL]+1 > self.MAXLEVEL:
                  self.MAXLEVEL = entry[self.MLEVEL]+1

               entry[self.MITEMS] +=1

               self.EMPTY = False
               if parent == self.ROOT: self.MAINCOUNT += 1
               if not self.INIT:
                  self.INIT = True
                  self.CURRELEMENT = self.MOFFSET
                  self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
                  self.setActiveOn()

            else: #keep looking
               if entry[self.MITEMS] > 0:
                  self.find2add(entry,parent,item, command)

######################################################################################
##  Add item to current activated item                                              ##
##                                                                                  ##
##  example: additem('File')                                                        ##
##           add item 'File' to a active item                                       ##
##  example: additem('Save', saveCommand)                                           ##
##           add item 'Save' to current item and assign a procedure to it           ##
##                                                                                  ##
######################################################################################
   def addItem2Current(self,item,*command):
      if len(command) == 0:
         cmd=''
      else:
         cmd=command[0]

      currentItem = self.CURRENTLEVEL[self.MOFFSET+self.activeIndex()]

      #Have a command already?
      if currentItem[self.MITEMS] == -1:
         del currentItem[-1]
         currentItem[self.MITEMS] = 0
              
      #append item
      if cmd == '':
         currentItem.append([currentItem[self.MLEVEL]+1,0,self.INACTIVE,item])
      else:
         currentItem.append([currentItem[self.MLEVEL]+1,-1,self.INACTIVE,item,cmd])

      #update maxlevel actually appended
      if currentItem[self.MLEVEL]+1 > self.MAXLEVEL:
         self.MAXLEVEL = currentItem[self.MLEVEL]+1

      currentItem[self.MITEMS] +=1

      self.EMPTY = False
      if self.parentName() == self.ROOT: self.MAINCOUNT += 1
      if not self.INIT:
         self.INIT = True
         self.CURRELEMENT = self.MOFFSET
         self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
         self.setActiveOn()
 
                           
######################################################################################
##  reset the list to have only the root. All entries and items are eliminated      ##
##  the result is an empty list                                                     ##
######################################################################################
   def emptyList(self):
      if not self.EMPTY:
         self.CURRENTLEVEL = self.menu
         self.goItemIndex(0)
         self.trace=list()
         for i in range(self.numberOfItems()):
            self.last()
            self.deleteItem(self.activeLabel())

######################################################################################
##  remove all subitems of active entry                                             ##
##  then set the active entry to its ancestor                                       ##
######################################################################################
   def removeAllSubItemsOfActiveEntry(self):
      if not self.EMPTY:
         if self.typeOfActiveItem() == 'SubMenu':
            self.goDown()
            totalItems=self.numberOfItems()
            for i in reversed(range(totalItems)):
                self.CURRENTLEVEL.remove(self.CURRENTLEVEL[self.MOFFSET+i])
            self.CURRENTLEVEL[self.MITEMS]=0
            self.goUp()
      else:
         print 'This list is empty'

######################################################################################
##  remove all subitems of entry entryName                                          ##
##  set entryName as the active entry                                               ##
######################################################################################
   def removeAllSubItemsOfEntry(self, entryName):
      if not self.EMPTY:
        self.savePosition()
        if self.find(entryName):
           self.removeAllSubItemsOfActiveEntry()
           self.find(entryName)
        else:
           print '%s NOT FOUND'%entryName
           self.restorePosition()
      else:
         print 'This list is empty'

######################################################################################
##  delete item itemName (this action remove all subitems too                       ##
######################################################################################        
   def deleteItem(self,itemName):
      self.goTop()
      self.find2delete(self.menu, itemName)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   def find2delete(self, array, item):
      for entry in array[self.MOFFSET:]:
         #if found it
         if entry[self.MLABEL] == item:
            self.count = 0    
            for i in array[self.MOFFSET:]:
               if i[self.MLABEL] == item:
                  break
               self.count += 1
            del array[self.count+3]

            array[self.MITEMS] -= 1
           
            if array[self.MLABEL] == self.ROOT: self.MAINCOUNT -= 1
            if self.MAINCOUNT == 0:
               self.EMPTY = True
               self.INIT = False
           
         else: #keep looking
            if entry[self.MITEMS] > 0:
               self.find2delete(entry,item)


######################################################################################
##  find itemName and set it active                                                 ##
######################################################################################
   def find(self,itemName, *parentName):
      self.found = False
      self.savePosition()
      self.goTop()
     
      if parentName:
         self.find2activate(parentName[0])
         self.found=False
         self.goDown()

      self.find2activate(itemName) 
 
      if not self.found:
         self.restorePosition()
      return self.found
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   def find2activate(self, item):
      for i in self.itemsOfCurrentList():
         #if found it
         if i == item:
            self.goItemName(item)
            self.found = True
         else:
            if self.found: break
            if self.typeOfActiveItem() == 'SubMenu':
               self.goDown()
               self.find2activate(item)
               if not self.found:
                  self.goUp()
                  self.goNext()
            else:  
               if not self.found:
                  self.goNext()   

######################################################################################
##  Save the current position for go back purposes                                  ##
######################################################################################
   def savePosition(self):
      self.PUSHDATA=[self.CURRENTLEVEL, self.CURRELEMENT, self, self.ACTIVEITEM]

######################################################################################
##  Restore de active position saved previosly with savePosition                    ##
######################################################################################
   def restorePosition(self):
      self.setActiveOff()
      self.CURRENTLEVEL = self.PUSHDATA[0]
      self.CURRELEMENT = self.PUSHDATA[1]
#      self.ACTIVEITEM = self.PUSHDATA[2]
      self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
      self.setActiveOn()
     
 
######################################################################################
##  Print list with their hierarquical structure                                    ##
######################################################################################
   def printList(self):
      if self.EMPTY:
         print 'This list is empty'
      else:  
         print self.menu[self.MLABEL]       
         self.printListRec(self.menu)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   def printListRec(self, array):
      if not self.EMPTY:        
         for entry in array[self.MOFFSET:]:
            if entry[self.MACTIVE]:
               activeLabel = ' (current)'
            else:  
               activeLabel = ''
            if entry[self.MITEMS] > 0:
               print "%s++%s%s" % (' '*(entry[self.MLEVEL]+1),entry[self.MLABEL], activeLabel)
               self.printListRec(entry)
            elif entry[self.MITEMS] == 0:
               print "%s@%s%s" % (' '*(entry[self.MLEVEL]+1),entry[self.MLABEL], activeLabel)
            elif entry[self.MITEMS] == -1:
               print "%s--%s%s" % (' '*(entry[self.MLEVEL]+1),entry[self.MLABEL], activeLabel)
   
######################################################################################
##  return active item and its attributes as string                                 ##
######################################################################################
   def activeItemInfo(self):
      if not self.EMPTY:
         if self.typeOfActiveItem() == 'SubMenu':
            return '%s: %s: %s (items)'%(self.activeLabel(),self.typeOfActiveItem(), self.ACTIVEITEM[self.MITEMS])
         else:
            return '%s: %s'%(self.activeLabel(),self.typeOfActiveItem())

######################################################################################
##  return active item as its were a menu entry                                     ##
######################################################################################
   def activeItemString(self):
      returnValue = ''
      if not self.EMPTY:
         if self.typeOfActiveItem() == 'SubMenu':
            returnValue='[%s]'%(self.activeLabel())
         if self.typeOfActiveItem() == 'Label':
            returnValue='<%s>'%(self.activeLabel())
         if self.typeOfActiveItem() == 'Command':
            returnValue='(%s)'%(self.activeLabel())  
      return returnValue

######################################################################################
##  returns current action of active entry                                          ##
######################################################################################
   def activeAction(self):
      returnValue=''
      if not self.EMPTY and self.typeOfActiveItem() == 'Command':
         returnValue=self.ACTIVEITEM[self.MACTION]           
      return returnValue

######################################################################################
##  returns current active list                                                     ##
######################################################################################
   def activeList(self):
      returnValue=list()
      if not self.EMPTY:
         returnValue=self.CURRENTLEVEL
      return returnValue  

######################################################################################
##  returns the active entry                                                        ##
######################################################################################
   def activeItem(self):
      returnValue=list()
      if not self.EMPTY:
         self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]     
         returnValue=self.ACTIVEITEM
      return returnValue  

######################################################################################
##  returns the active Label                                                        ##
######################################################################################
   def activeLabel(self):
      returnValue=''
      if not self.EMPTY:
         self.activeItem()
         returnValue=self.ACTIVEITEM[self.MLABEL]
      return returnValue  

######################################################################################
##  returns the active Index                                                        ##
######################################################################################
   def activeIndex(self):
      returnValue=-1
      if not self.EMPTY:
         returnValue=self.CURRELEMENT-self.MOFFSET
      return returnValue  
  
######################################################################################
##  returns the active position related to its level                                ##
######################################################################################
   def activePosition(self):
      returnValue=''
      if not self.EMPTY:
         returnValue=str(self.CURRELEMENT-self.MOFFSET+1)+'/'+str(self.CURRENTLEVEL[self.MITEMS])
      return returnValue  

######################################################################################
##  return True if the active Item has sub items                                    ##
######################################################################################
   def activeEntryHasItems(self):
      returnValue = False
      if not self.EMPTY and self.typeOfActiveItem() == 'SubMenu': returnValue = True
      return returnValue
     
######################################################################################
##  returns number of items of current level                                        ##
######################################################################################
   def numberOfItems(self):
      return self.CURRENTLEVEL[self.MITEMS]

######################################################################################
##  returns number of subItems of current Item                                      ##
######################################################################################
   def numberOfSubItems(self):
      if self.ACTIVEITEM[self.MITEMS]>=0:
         returnValue = self.ACTIVEITEM[self.MITEMS]
      else:
         returnValue = 0
        
      return returnValue

######################################################################################
##  set current element active (only for internal use)                              ##
######################################################################################
   def setActiveOn(self):
      if not self.EMPTY:
         self.ACTIVEITEM[self.MACTIVE]=True

######################################################################################
##  set current element inactive (only for internal use)                            ##
######################################################################################
   def setActiveOff(self):
      if not self.EMPTY:
         self.ACTIVEITEM[self.MACTIVE]=False

######################################################################################
##  go and set active the first entry of current level                              ##
######################################################################################
   def goFirst(self):
      if not self.EMPTY:
         self.setActiveOff()
         self.CURRELEMENT = self.MOFFSET
         self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
         self.setActiveOn()
     
######################################################################################
##  set active the item indicated by index relative to the current level            ##
######################################################################################
   def goItemIndex(self, index):
      if not self.EMPTY:
         self.setActiveOff()
         self.CURRELEMENT = (index % self.numberOfItems()) + self.MOFFSET
         self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
         self.setActiveOn()

######################################################################################
##  set active the item indicated by itemName relative to the current level         ##
######################################################################################
   def goItemName(self, itemName):
      if not self.EMPTY:
         self.setActiveOff()
         count=0
         for i in self.CURRENTLEVEL[self.MOFFSET:]:
            if i[self.MLABEL] == itemName:
               self.CURRELEMENT = count + self.MOFFSET
            count += 1
           
         self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
         self.setActiveOn()

######################################################################################
##  go to the next entry in the current level and set active it active              ##
######################################################################################
   def goNext(self):
      if not self.EMPTY:
         self.setActiveOff()
         if self.CURRELEMENT < (self.numberOfItems()+self.MOFFSET-1):
            self.CURRELEMENT += 1
         else:
            self.CURRELEMENT = self.MOFFSET
     
         self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
         self.setActiveOn()

######################################################################################
##  go to the prev entry in the current level and set active it active              ##
######################################################################################
   def goPrev(self):
      if not self.EMPTY:
         self.setActiveOff()
         if self.CURRELEMENT > self.MOFFSET:
           self.CURRELEMENT -= 1
         else:
            self.CURRELEMENT = (self.numberOfItems()+self.MOFFSET-1)
     
         self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
         self.setActiveOff()

######################################################################################
##  go to the last entry in the current level and set active it active              ##
######################################################################################
   def goLast(self):
      if not self.EMPTY:
         self.setActiveOff()
         self.CURRELEMENT = self.numberOfItems()+self.MOFFSET-1
         self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
         self.setActiveOn()

######################################################################################
##  if entry has subitems go to the next child level and set the first item active  ##
######################################################################################
   def goDown(self):
      if not self.EMPTY:
         if self.typeOfActiveItem() == 'SubMenu':
            self.setActiveOff()
            self.trace.append([self.CURRELEMENT,self.CURRENTLEVEL])
            self.CURRENTLEVEL = self.CURRENTLEVEL[self.CURRELEMENT]
            self.CURRELEMENT = self.MOFFSET
            self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
            self.setActiveOn()

######################################################################################
##  go up to the parent level of the list and set the previous active entry         ##
######################################################################################
   def goUp(self):
      if not self.EMPTY:
         if len(self.trace) > 0:
            self.setActiveOff()
            self.CURRENTLEVEL = self.trace[-1][1]
            self.CURRELEMENT = self.trace[-1][0]
            self.ACTIVEITEM = self.CURRENTLEVEL[self.CURRELEMENT]
            del self.trace[-1]
            self.setActiveOn()

######################################################################################
##  returns the type of the active entry                                            ##
######################################################################################
   def typeOfActiveItem(self):
      returnValue=''
      if not self.EMPTY:
         returnValue=self.typeOfItem(self.ACTIVEITEM)
      return returnValue
     
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   def typeOfItem(self, item):
      returnType = ''
      if not self.EMPTY:
         self.CURRENTLEVELTYPE = item[self.MITEMS]
         if self.CURRENTLEVELTYPE > 0:
            returnType = 'SubMenu'
         elif self.CURRENTLEVELTYPE == 0:
            returnType = 'Label'
         elif self.CURRENTLEVELTYPE == -1:
            returnType = 'Command'
 
      return returnType

######################################################################################
##  print debug info                                                                ##
######################################################################################
   def printDebug(self):
      if not self.EMPTY:
         print 'BEGIN: DEBUG INFORMACION *******************************************************'
         print 'main: CURRENT LEVEL (self.CURRENTLEVEL): '
         print self.CURRENTLEVEL
         print 'main: NUMBER OF ITEMS: %d'%(self.numberOfItems())
         print 'main: ACTIVE ITEM INDEX: %d'%(self.CURRELEMENT-self.MOFFSET)
         print 'main: ACTIVE ITEM LABEL: %s'%self.activeLabel()
         print 'main: ACTIVE ITEM TYPE: %s'%(self.typeOfActiveItem())
         print 'main: ACTIVE ITEM RAW CONTENT (self.ACTIVEITEM): '
         print self.ACTIVEITEM
         print 'END: DEBUG INFORMACION *******************************************************'
      else:
         print 'This list is empty'
                 
######################################################################################
##  returns a iterable of items that belongs to current list                        ##
######################################################################################
   def itemsOfCurrentList(self):
      temp=list();
      if not self.EMPTY:
         activeItem = self.CURRELEMENT-self.MOFFSET
         self.goItemIndex(0)
         for i in range(self.numberOfItems()):
            temp.append(self.activeLabel())
            self.goNext()
         self.goItemIndex(activeItem)

      return iter(temp)
 
 
######################################################################################
##  returns the label of the parent name                                            ##
######################################################################################
   def parentName(self):
         return self.CURRENTLEVEL[self.MLABEL]

######################################################################################
##  returns a iterable of subitems                                                  ##
######################################################################################
   def subItems(self):
      temp=list()   
      if not self.EMPTY:
         if self.typeOfActiveItem() == 'SubMenu':
            self.goDown()
            temp=self.itemsOfCurrentList()
            self.goUp()

      return iter(temp)
     
######################################################################################
##  load file names as items to itemName                                            ##
######################################################################################
   def loadFiles(self,itemName,path, *ext):
      for filename in [f for f in sorted(os.listdir(path)) if os.path.isfile(os.path.join(path,f))]:
         if len(ext)>0:
            for e in ext:
               if filename.split('.')[-1] == e:
                  self.addItem(itemName,filename)
         else:        
            self.addItem(itemName,filename)

######################################################################################
##  load file names as items to active item                                         ##
######################################################################################
   def loadFiles2Current(self, path, *ext):
      for filename in [f for f  in sorted(os.listdir(path)) if os.path.isfile(os.path.join(path,f))]:
         if len(ext)>0:
            for e in ext:
               if filename.split('.')[-1] == e:
                  self.addItem2Current(filename)
         else:        
            self.addItem2Current(filename)

######################################################################################
##  load dir names as items to itemName                                            ##
######################################################################################
   def loadDirs(self,itemName,path):
      for dirname in [f for f  in sorted(os.listdir(path)) if os.path.isdir(os.path.join(path,f))]:
         self.addItem(itemName,dirname)

######################################################################################
##  load dir names as items to active item                                          ##
######################################################################################
   def loadDirs2Current(self,itemName,path):
      for dirname in [f for f  in sorted(os.listdir(path)) if os.path.isdir(os.path.join(path,f))]:
         self.addItem2Current(dirname)

##################################################################################################################        
if __name__ == '__main__':
   menu = treeList()
  
   menu.fillDummyItems()
  
   menu.printList()
