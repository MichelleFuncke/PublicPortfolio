#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Michelle
#
# Created:     19/08/2014
# Copyright:   (c) Michelle 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# import tkinter for python 3 but Tkinter for python 2
import Tkinter

#this is our GUI class declaration, the class inherits from Tkinter.Tk
class simpleApp_TK(Tkinter.Tk):

    def __init__(self, parent, populateList, labelNames = [], defaultValue=[],listofguis=[]):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent #keep a reference to your parent
        self.inputsList = []; # a list of input items - each entry is a tuple of the form (label, textbox, textVariable)
        self.populateList = populateList;
        self.initialise(labelNames,defaultValue,listofguis)


    #creates all the GUI elements
    def initialise(self, listOfLabelnames, defaultValues, listofguis):
        """listofguis: tbx=textbox,cbx=checkbox,rbn=radiobutton"""
        self.grid()

        r=0
        for i in range(len(listOfLabelnames)):
            if listofguis[i] == 'tbx':
                self.addTextBox(r,listOfLabelnames[i],defaultValues[i])
                r += 1
            elif listofguis[i] == 'cbx':
                self.addCheckbox(r,listOfLabelnames[i],defaultValues[i])
                r += 1
            elif listofguis[i] == 'rbn':
                self.addRadiobutton(r,listOfLabelnames[i],defaultValues[i])
                r += len(listOfLabelnames[i])-1

        #adding a button
        button = Tkinter.Button(self,text="Continue",
                                command=self.OnButtonClick)#include a an event handler method to be called when clicked
        button.grid(column = 0, row = r)


        #configure the grid so that it resizes the first column with the window
        self.grid_columnconfigure(0,weight=1)

        #make the window resizable on the horizontal axis but not the vertical
        self.resizable(True,False)

    def addTextBox(self,r, LabelText, defaultValue = ""):
        tempLB = Tkinter.Label(self, anchor = "w",fg="white",bg="blue", text=LabelText)
        tempVA = Tkinter.StringVar()
        tempTB = Tkinter.Entry(self, textvariable=tempVA)
        #tuples of the form (label, textbox, textVariable)
        self.inputsList.append((tempLB, tempVA))

        #set the values and positions of the text box and label
        tempTB.grid(column=1,row=r,sticky="EW")

        self.inputsList[-1][0].grid(column=0,row=r,sticky="EW")
       # self.inputsList[lastIndex][1].set("Enter Text Here")
        self.inputsList[-1][1].set(defaultValue)

    def addCheckbox(self,r, LabelText, defaultValue = ""):
        tempLB = Tkinter.Label(self, anchor = "w",fg="white",bg="blue", text=LabelText)
        tempVA = Tkinter.IntVar()
        tempCB = Tkinter.Checkbutton(self,variable=tempVA)
        tempCB.grid(column=1,row=r,sticky='EW')

        self.inputsList.append((tempLB,tempVA))

        #set the values and positions of the text box and label
        self.inputsList[-1][0].grid(column=0,row=r,sticky="EW")
       # self.inputsList[lastIndex][1].set("Enter Text Here")
        self.inputsList[-1][1].set(defaultValue)

    def addRadiobutton(self,r, LabelText, defaultValue = ""):

        tempVA = Tkinter.IntVar()
        for j in range(len(LabelText)-1):
            if j==0:
                tempLB = Tkinter.Label(self, anchor = "w",fg="white",bg="blue", text=LabelText[0])
                tempRB = Tkinter.Radiobutton(self,text=LabelText[1],variable=tempVA,value=(1))
            else:
                tempLB = Tkinter.Label(self, anchor = "w",text="")
                tempRB = Tkinter.Radiobutton(self,text=LabelText[j+1],variable=tempVA,value=(j+1))
            tempLB.grid(column=0,row=r,sticky="EW")
            tempRB.grid(column=1,row=r,sticky="EW")
            r += 1
        self.inputsList.append((tempLB,tempVA))

            #set the values and positions of the text box and label
        self.inputsList[-1][1].set(defaultValue)


    #some event handling methods:
    def OnButtonClick(self):
        #self.labelVariable.set("Running")
        for aTuple in self.inputsList:
            self.populateList.append(aTuple[1].get())
        self.destroy();


    def OnPressEnter(self,event):
        pass
        #self.labelVariable.set(self.entry.get() + " (Enter)")

##################outside the class

def getInputsList(labelNames = [], defaultValue = [],listofguis = []):
    inputList = []

    app = simpleApp_TK(None,inputList,labelNames,defaultValue,listofguis) #None == no parent
    app.title("My app")

    app.mainloop()
    #sits waiting for the user the end the program

    return inputList

def main():
    labels = ['z','N','Rayleigh',['method to get PS','bin','inter','non'],'test: bin','test: inter',['timesteps:','all','non','other'],'other:','growing mode','extra delta']
    default = ['10','50',0,3,0,0,2,0,0,0]
    listgui = ['tbx','tbx','cbx','rbn','cbx','cbx','rbn','tbx','cbx','cbx']
    temp = getInputsList(labels,default,listgui)
    print(temp)
##    print('z=',temp[0])
##    print('N=',temp[1])
##    print('Rayleigh',bool(temp[2]))
##    option1 = ['bin','inter','non']
##    print('method to get PS',option1[temp[3]-1])
##    print('test: bin',bool(temp[4]))
##    print('test: inter',bool(temp[5]))
##    option2 = ['all','non','other']
##    print('timesteps:',option2[temp[6]-1])
##    print('other:',temp[7])
##    print('growing mode',bool(temp[8]))
##    print('extra delta',bool(temp[9]))

if __name__ == '__main__':
    main()
