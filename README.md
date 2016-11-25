# treeList-python
Treelist library on python

What is a TreeList?. A treelist is a special kind of list which can manage unlimited levels of nested lists in an organized way, useful for creating hierarchical structures that can be maintained and navigated using some simple methods. This library was originally design as a menu enabler, but can be used for any other purpose.

Creating a empty list:

(1) menu = treelist()

When we create this list, it is actually not really empty. What we do is creates the base structure of the list that contains one element called 'Root' that is referenced as ROOT constant. This first list created has only one element.

In this example we will be creating a menu as illustration. The following list depicts what we want to achieve.

        Root --
          | ++1-picture (current)
          | @shoot
          | ++list
                 | @scan
                 | @share
                 | @pictures
                 | @erase all
                 | ++settings
                       | @set folder
                       | @set exposure
            | ++time lapsed
                 | @start
                 | @stop
                 | @status
                 | ++list
                        | @scan
                        | @share
                        | @pictures
                        | @erase all
                 | ++settings
                        | @set folder
                        | @set exposure
                        | @set interval
             | ++system
                        | @date&time
                        | @reboot
                        | @poweroff
                        | @exit
This is a menu for working with Pi Camera. Let's start with 1-picture entry and its items.

        (2)   menu.addItem(menu.ROOT, '1-picture')
        (3)   menu.addItem('1-picture','shoot')
        (4)   menu.addItem('1-picture','list')
        (5)   menu.find('list', '1-picture')
        (6)   menu.addItem2Current('scan')
        (7)   menu.addItem2Current('share')
        (8)   menu.addItem2Current('pictures')
        (9)   menu.addItem2Current('erase all')
        (10)   menu.addItem('1-picture','settings')
        (11)   menu.find('settings', '1-picture')
        (12)   menu.addItem2Current('set folder')
        (13)   menu.addItem2Current('set exposure')
(2) add an item to the Root element, which in this case is the first element created in the list using the constructor of the class treeList. addItem() is a method that add an item to the element indicated in the first argument, called parent. if the parent doesn't exists the method don't do anything. If parent exists it creates the element, called child, as an item of the parent. We can add as many items as we need to create a hierarchical structure in several layers.

(3), (4) creates two items that pertain to 1-picture parent. (5) find() executes a recursive tree navigation looking for 'list' whose parent has to be ' 1-picture'. Once we find the item 'list' it becomes active. Some navigation methods activate the item to set it current that can be manipulated later. (6) adds 'scan' to the current item that in this case is 'list' which is child of ' 1-picture'. This method of adding items need to be done this way to overcome the ambiguity of having several equal items. In this case, we identify the item by its parent so after doing it we can use addItem2Current(). (6,7,8,9) executes item addition to the current element ' list'.

(10) Because 1-picture is unique in the tree list, we can use addItem() again to add ' settings'. To add 'set folder' and 'set exposure' to 'settings' we can add them using addItem() because 'settings' so far is unique, but to maintain homogeneity we decided to use the methodology explained above. The rest of items can be added in the same way as '1-picture' and its items.

        (14)   menu.addItem(menu.ROOT, 'time lapsed')
        (15)   menu.addItem('time lapsed', 'start')
        (16)   menu.addItem('time lapsed', 'stop')
        (17)   menu.addItem('time lapsed', 'status')
        (18)   menu.addItem('time lapsed', 'list')
        (19)   menu.find('list', 'time lapsed')
        (20)   menu.addItem2Current('scan')
        (21)   menu.addItem2Current('share')
        (22)   menu.addItem2Current('pictures')
        (23)   menu.addItem2Current('erase all')
        (24)   menu.addItem('time lapsed','settings')
        (25)   menu.find('settings', 'time lapsed')
        (26)   menu.addItem2Current('set folder')
        (27)   menu.addItem2Current('set exposure')
        (28)   menu.addItem2Current('set interval')
        (29)   menu.addItem(menu.ROOT, 'system')
        (30)   menu.addItem('system','date&time')
        (31)   menu.addItem('system','reboot')
        (32)   menu.addItem('system','poweroff')
        (33)   menu.addItem('system','exit    ') 
addItem() and addItem2Current() methods accept three arguments (parent item, child item, *commad). Parent is a string describing the parent in which we need to add child items described as string. command is the pointer of a python function that we can create to give the child a behavior. Command argument is optional so If we don't pass this argumen, addItem() interprets the child is going to be a label or a future parent.

Any item with ++ prefix (listed above) indicates it has child items. Any item with @ prefix indicates it is a label which not contain a command associated.

(33) menu.printList(), will output

        Root
        ++1-picture (current)
           @shoot
           ++list
              @scan
              @share
              @pictures
              @erase all
           ++settings
              @set folder
              @set exposure
        ++time lapsed
           @start
           @stop
           @status
           ++list
              @scan
              @share
              @pictures
              @erase all
           ++settings
              @set folder
              @set exposure
              @set interval
        ++system
           @date&time
           @reboot
           @poweroff
           @exit
The nomenclature, in the figure of prefixes (++) and (@), indicates visually if items are parents or labels, these last ones can be seen as leaves of the tree. Additionally a (current) tag is printed referring the current active element. Till this far, the list is a simple list of multiple level of items.

Lets create our first python code for creating this list.

        #menu.py
        import treeList
        def initMenu(menu):
           menu.addItem(menu.ROOT, '1-picture')
           menu.addItem('1-picture','shoot')
           menu.addItem('1-picture','list')
           menu.find('list', '1-picture')
           menu.addItem2Current('scan')
           menu.addItem2Current('share')
           menu.addItem2Current('pictures')
           menu.addItem2Current('erase all')
           menu.addItem('1-picture','settings')
           menu.find('settings', '1-picture')
           menu.addItem2Current('set folder')
           menu.addItem2Current('set exposure')
           menu.addItem(menu.ROOT, 'time lapsed')
           menu.addItem('time lapsed', 'start')
           menu.addItem('time lapsed', 'stop')
           menu.addItem('time lapsed', 'status')
           menu.addItem('time lapsed', 'list')
           menu.find('list', 'time lapsed')
           menu.addItem2Current('scan')
           menu.addItem2Current('share')
           menu.addItem2Current('pictures')
           menu.addItem2Current('erase all')
           menu.addItem('time lapsed','settings')
           menu.find('settings', 'time lapsed')
           menu.addItem2Current('set folder')
           menu.addItem2Current('set exposure')
           menu.addItem2Current('set interval')
           menu.addItem(menu.ROOT, 'system')
           menu.addItem('system','date&time')
           menu.addItem('system','reboot')
           menu.addItem('system','poweroff')
           menu.addItem('system','exit    ')
           menu.goTop()

        if __name__ == '__main__':

           menu = treeList()
           initMenu()
           menu.printList()
At this point we can use this list only for showing it using printList() method or for using it with another library that we have created to use this tree list as a menu using the Adafruit CharPlate LCD for Raspberry Pi. The use of this LCD display can be easier if we can use a hierarchical list for showing information using the navigation buttons the LCD Display comes with.

But before we can go on with the LCD Menu for Adafruit 16x2 display, let me show some other actions that can be taken over our tree list.

NAVIGATION METHODS

Tree list consists on levels, where the main one is ROOT. When we add the first item to ROOT, addItem() creates the first level that becomes the active level. We can activate a level using goDown() or goUp() methods to step down or step up through the list. When a level is activated, we can go over each item of the activated level using goNext(), goPrev(), goFirst() and goLast() methods. Additionally, itemsOfCurrentList() method can give us the labels of the activated list.

When we create a list and add items to it, the first level is activated by default. So, the next lines of code shows how to navigate the first level. Assumes that we just created our list using the function previosly creted initMenu(), then show each entry label of the first level.

(34)   for label in menu.itemsOfCurrentList():
(35)      print label
The output of this two lines of code is

1-picture
time lapsed
system
We can navigate for these active list using several variants. For example, to get the same output of previous code we can do the following.

(36)   menu.goFirst()
(37)   for item in range(menu.numberOfItems()):
(38)      print menu.activeLabel()
(39)      menu.goNext()
(37) iterates over a range from 0 to menu.numberOfItems() which returns the number of entries of the active list. goFirst() and goNext() activates the item where it goes, so we can use a set of methods that can give us information about the active item. That is the case of activeLabel() and some other methods like activeIndex() and activePosition().

(40)   menu.goFirst()
(41)   for item in range(menu.numberOfItems()):
(42)      print 'Label:%s, Index: %d, Relative Position: %s'%(menu.activeLabel(), menu.activeIndex(), menu.activePosition())
(43)      menu.goNext()


output:
Label:   1-picture    Index:  0    Relative Position: 1/3
Label: time lapsed    Index:  1    Relative Position: 2/3
Label:      system    Index:  2    Relative Position: 3/3
Another two methods are specially useful for navigation purposes. savePosition() and restorePosition() that can give an extra control over our movement. Let's down over the list first to show how to use it. Let's down to 'set exposure' of '1-picture' using the navigation tool goDown() method.

(44)   menu.goTop()
(45)   menu.savePosition()
(46)   print 'Label:%12s\tIndex: %2d\tRelative Position: %s'%(menu.activeLabel(), menu.activeIndex(), menu.activePosition())
(47)   menu.goDown()
(48)   print 'Label:%12s\tIndex: %2d\tRelative Position: %s'%(menu.activeLabel(), menu.activeIndex(), menu.activePosition())
(49)   menu.goItemName('settings')
(50)   print 'Label:%12s\tIndex: %2d\tRelative Position: %s'%(menu.activeLabel(), menu.activeIndex(), menu.activePosition())
(51)   menu.goDown()
(52)   print 'Label:%12s\tIndex: %2d\tRelative Position: %s'%(menu.activeLabel(), menu.activeIndex(), menu.activePosition())
(53)   menu.goLast()
(54)   print 'Label:%12s\tIndex: %2d\tRelative Position: %s'%(menu.activeLabel(), menu.activeIndex(), menu.activePosition())
(55)   menu.restorePosition()
(56)   print 'Label:%12s\tIndex: %2d\tRelative Position: %s'%(menu.activeLabel(), menu.activeIndex(), menu.activePosition())


output:
Label:       1-picture    Index:  0    Relative Position: 1/3
Label:           shoot    Index:  0    Relative Position: 1/3
Label:        settings    Index:  2    Relative Position: 3/3
Label:      set folder    Index:  0    Relative Position: 1/2
Label:    set exposure    Index:  1    Relative Position: 2/2
Label:       1-picture    Index:  0    Relative Position: 1/3
(44) goes to the top of the list that is the first item of the first level which is '1-picture' then (45) save that position. (47) down one level and set 'shoot', which is the first item of that list, as the active item. With goItemName() method at (49) we can move in the active level looking for a item called 'settings' and set it active. (51) down one step and set 'set folder' as active. In that level we can go to the last item using goLast() method. (55) restores the position saved in (45) that was '1-picture'.

We can use goItemName() and goItemIndex() to move the active item using its name or index in the active list. For example, we can go through subtiems of list that pertains to 'time lapsed' with:

        (57)   menu.find('list','time lapsed')  
        (58)   for index in range(menu.numberOfItems()):
        (59)      menu.goItemIndex(index)
        (60)      print 'Label:%12s\tIndex: %2d\tRelative Position: %s'%(menu.activeLabel(), menu.activeIndex(), menu.activePosition())


        output:
        Label:       start    Index:  0    Relative Position: 1/5
        Label:        stop    Index:  1    Relative Position: 2/5
        Label:      status    Index:  2    Relative Position: 3/5
        Label:        list    Index:  3    Relative Position: 4/5
        Label:    settings    Index:  4    Relative Position: 5/5
(57) finds 'list' of 'time lapsed' to go down one level so we can go through each item using the index of the "for" loop.

ASSIGNING A COMMAND TO A ITEM

We can give a item a behavior assigning a command to that item. addItem() or AddItem2Current() methods give us a way to do it adding the name of the function as a parameter. Let's see another list in which we assign some behavior.

(58) from treeList import treeList
(59) import datetime
(60) import os
(61) from time import sleep


(62) def reboot():
(63)    print "\nrebooting..."
(64)    os.system('reboot')


(65) def powerOff():
(66)    print "\npowering off..."
(67)    os.system('poweroff')


(68) def updateDateTime(menu):
(69)    date=datetime.datetime.now().strftime("%y/%m/%d")
(70)    time=datetime.datetime.now().strftime("%H:%M:%S")
(71)    uname=os.uname()
(72)    menu.removeAllSubItemsOfEntry('date&time')
(73)    menu.addItem('date&time','date') 
(74)    menu.addItem('date',date) 
(75)    menu.addItem('date&time','time') 
(76)    menu.addItem('time',time) 


(77) def menuInit(menu):
(78)    menu.addItem(menu.ROOT, 'system')
(79)    menu.addItem('system','date&time')
(80)    menu.addItem('system','reboot', reboot)
(81)    menu.addItem('system','poweroff', powerOff)
(82)    menu.goTop()
(83)    updateDateTime(menu)


(84) if __name__ == '__main__':
(85)    menu = treeList()
(86)    menuInit(menu)

(87)    while True:
(88)       updateDateTime(menu)
(89)       menu.printList()
(90)       sleep(1)
(85) define a treeList as menu, then menuInit() add items to the list.(83) calls updateDateTime() that use removeAllSubItemsOfEntry() method to remove all items below 'date&time' entry. This way we can maintain lists of labels below a item for giving information. in this case we are adding 'date' label and 'time' label to 'date&time' entry. We use datetime to add the current time and current date to time and date entries.

(87) enters to a infinite while loop for showing the tree list using printList(), also we update 'date&time' item using updateDateTime() method every second.

Notice that (80) and (81) adds items reboot and poweroff and the third parameters is a function defines at (62) and (65) lineas. If this list is used in a menu context, and we need to reboot the server, we can use activeAction() method after go and set active the entry 'reboot'.

(91) menu.find('reboot')
(92) menu.activeAction()()
menu.find looks for a item called 'reboot' and set it active. menu.activeAction() methods returns the command that is executed in (92).

TreeList was originally designed for working with Adafruit CharPlate Display 16x2, so it nature is serial by default duw to the fact that a user go through a menu down and up and then select an option and execute it.
Contact GitHub API Training Shop Blog About
© 2016 GitHub, Inc. Term
