from tkinter import *
from tkinter.font import Font
import threading
import BoardClass
import GraphicClass
import TextClass
import DebuggingClass
import LogicClass
import CardClass
import CVClass


# Klasse som er GUI
class GUI:
    def __init__(self, debugMode, gpuMode):
        self.tk = Tk()  # Opretter GUI
        self.tk.title("Solitaire")  # Navngiver GUI
        self.tk.resizable(False, False)  # gør at gui window ikke kan blive større eller mindre
        self.cmd = None
        self.debugMode = debugMode

        # opretter forskellige klasser (forskellige Canvases som vises i gui)
        self.board = BoardClass.Board(self, debugMode)
        self.graphicCanvas = GraphicClass.Graphic(self.tk, self.board, self, 800, 600)
        self.textCanvas = TextClass.Text(self.tk, self.board, self, 500, 120)
        self.logic = LogicClass.Logic(self.board)
        self.debug = DebuggingClass.Debugging(self.board)
        self.webcam = CVClass.CV(self.tk, self, 1280, 720, gpuMode)

        # Opretter knapper
        self.toggleButton = Button(self.tk, text="Border\nsettings", command=self.toggleBorder)
        self.updateButton = Button(self.tk, text="Update\nboard", command=self.updateBoard)
        self.calcButton = Button(self.tk, text="Calculate\nnext move", command=self.calcMove)
        self.rulesButton = Button(self.tk, text="Correct error\non board", command=self.missingCard)
        self.infoButton = Button(self.tk, text="Info", command=self.showInfo)
        self.exitButton = Button(self.tk, text="Exit", command=self.exit)
        self.toggleButton.grid(column=15, row=6, sticky=NSEW)

        # opstiller board hvis debugmode
        if self.debugMode:
            print("test")
            self.debug.setupBoardRandom()

        # sætter placering for klasser og knapper
        self.webcam.panel.grid(column=0, row=0, columnspan=10, rowspan=8)
        self.graphicCanvas.canvas.grid(column=10, row=0, columnspan=8, rowspan=6)
        self.textCanvas.canvas.grid(column=10, row=6, columnspan=5, rowspan=2)
        self.updateButton.grid(column=16, row=6, sticky=NSEW)
        self.calcButton.grid(column=17, row=6, sticky=NSEW)
        self.rulesButton.grid(column=15, row=7, sticky=NSEW)
        self.infoButton.grid(column=16, row=7, sticky=NSEW)
        self.exitButton.grid(column=17, row=7, sticky=NSEW)

        # Flag som bruges til at holder styr på om kommando er opdateret
        self.CMDFlag = False

        # opretter og starter thread som håndtere webcam input
        self.cvThread = threading.Thread(target=self.webcam.videoStream)
        self.cvThread.start()

        self.update_GUI()  # Update GUI function kaldes hvert 20. milisekundt

    # knap funktion
    def toggleBorder(self):
        top = Toplevel(self.tk)  # opretter nyt window
        borderClass(top, self)  # opretter klasse

    # knap funktion
    def updateBoard(self):
        webcam = self.webcam
        if self.debugMode:
            self.debug.moveCards(self.cmd)  # Function som flytter kort
        else:
            self.board.inputProcessing(webcam.getDataList(), webcam.sizeX, webcam.sizeY, webcam.intervalY, self.cmd)

        self.setCMD(None)

    # knap funktion
    def calcMove(self):
        cmd = self.logic.calcCMD()  # Function som beregner nu kommandoo
        print(cmd)  # til debugging
        self.setCMD(cmd)  # Function som fortæller div. klasse at kommando er opdateret

    # knap funktion
    def missingCard(self):
        top = Toplevel(self.tk)  # opretter window
        missingCardClass(top, self)  # opretter klasse

    # knap funktion
    def showInfo(self):
        top = Toplevel(self.tk)  # opretter window
        Info(top, self)  # opretter klasse

    # knap funktion
    def exit(self):
        self.tk.quit()  # lukker gui

    # master function som opdatere gui
    def update_GUI(self):
        self.graphicCanvas.update()  # Updatere grafik
        self.textCanvas.update()  # Updatere text

        self.tk.after(20, self.update_GUI)  # Fortæller hvor langt tid der skal gå før function skal kaldes

    # Function som fortæller div. klasse at kommando er opdateret
    def setCMD(self, cmd):
        self.cmd = cmd
        self.graphicCanvas.drawFlag = True
        self.textCanvas.drawFlag = True

    # deler cmd om i strings og int som kan bruges at samtlige funktioner
    def translateCMD(self, cmd):
        temp = cmd.split("-")
        start = temp[0]
        temp = temp[1].split(",")
        index = int(temp[0])
        target = temp[1]

        return [start, index, target]


# funktion der står for border in stillinger
class borderClass:
    def __init__(self, master, gui):
        self.master = master
        self.gui = gui
        self.master.title("Border")  # title på window
        self.master.geometry("207x92")  # størrelse på window
        self.master.resizable(False, False)  # window kan ikke gøre større eller mindre
        self.val = IntVar(
            value=self.gui.webcam.sizeY - self.gui.webcam.intervalY)  # opretter int variable (bruges af spinbox)

        # opretter klasser
        self.spin = Spinbox(self.master, from_=0, to=self.gui.webcam.sizeY, width=8, wrap=True, textvariable=self.val,
                            font=Font(family='Helvetica', size=30, weight='bold'))
        self.setButton = Button(self.master, text="Set", height=2, command=self.saveValue)
        self.onOffButton = Button(self.master, text="On/Off", height=2, command=self.onoff)
        self.cancelButton = Button(self.master, text="Cancel", height=2, command=self.close)

        # sætter positioner
        self.spin.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=NSEW)
        self.setButton.grid(column=0, row=2, sticky=NSEW)
        self.onOffButton.grid(column=1, row=2, sticky=NSEW)
        self.cancelButton.grid(column=2, row=2, sticky=NSEW)

    # knap funktion (gemmer værdi fra spinbox)
    def saveValue(self):
        self.gui.webcam.intervalY = self.gui.webcam.sizeY - int(self.spin.get())

    # knap funktion (lukker window)
    def close(self):
        self.master.destroy()
        self.master.update()

    # knap funktion (ændre om border skal tegnes eller ej)
    def onoff(self):
        if self.gui.webcam.drawBorderFlag:
            self.gui.webcam.drawBorderFlag = False
        else:
            self.gui.webcam.drawBorderFlag = True


# klasse der tilføjer eller fjerner kort fra board
class missingCardClass:
    def __init__(self, master, gui):
        self.master = master
        self.gui = gui

        self.master.title("Card Error")  # title på window
        self.master.geometry("414x142")  # størelse på window
        self.master.resizable(False, False)  # window kan ikke gøres større eller mindre

        # opretter string og int variabler som bruges at spinbox og optionMenu
        self.cardPileVal = StringVar()
        self.cardindex = IntVar(value=1)
        self.cardType = StringVar()
        self.cardNum = IntVar(value=1)

        # opretter font til spinbox og optionMenu
        fontSpin = Font(family='Helvetica', size=30, weight='bold')
        fontDrop = Font(family='Helvetica', size=12, weight='bold')

        # opretter lister til optionMenu
        cardPileOptions = [
            "Talon",
            "Tableau Row 1",
            "Tableau Row 2",
            "Tableau Row 3",
            "Tableau Row 4",
            "Tableau Row 5",
            "Tableau Row 6",
            "Tableau Row 7",
            "Foundation Spades",
            "Foundation Hearts",
            "Foundation Clubs",
            "Foundation Diamonds"
        ]
        typeOptions = [
            "Spades",
            "Hearts",
            "Clubs",
            "Diamonds",
            "Face down"
        ]
        # sætter default værdi
        self.cardPileVal.set(cardPileOptions[0])
        self.cardType.set(typeOptions[0])

        # opretter optionMenu
        self.cardPileMenu = OptionMenu(self.master, self.cardPileVal, *cardPileOptions)
        self.cardPileMenu.config(font=fontDrop, width=18)
        self.typeMenu = OptionMenu(self.master, self.cardType, *typeOptions)
        self.typeMenu.config(font=fontDrop, width=18)

        # opretter spinbex
        self.indexSpin = Spinbox(self.master, from_=1, to=20, width=8, wrap=True, textvariable=self.cardindex,
                                 font=fontSpin)
        self.numSpin = Spinbox(self.master, from_=1, to=13, width=8, wrap=True, textvariable=self.cardNum,
                               font=fontSpin)

        # opretter knapper
        self.createButton = Button(self.master, text="Create\nCard", height=2, command=self.createCard)
        self.removeButton = Button(self.master, text="Remove\nCard", height=2, command=self.removeCard)
        self.cancelButton = Button(self.master, text="Cancel", height=2, command=self.close)

        # sætter klassers placering
        self.cardPileMenu.grid(column=0, row=0, columnspan=4, sticky=NSEW)
        self.typeMenu.grid(column=0, row=2, columnspan=4, sticky=NSEW)
        self.indexSpin.grid(column=4, row=0, columnspan=3, sticky=NSEW)
        self.numSpin.grid(column=4, row=2, columnspan=3, sticky=NSEW)
        self.createButton.grid(column=4, row=3, sticky=NSEW)
        self.removeButton.grid(column=5, row=3, sticky=NSEW)
        self.cancelButton.grid(column=6, row=3, sticky=NSEW)

    # knap funktion (skaber nyt kort og tilføjer til bunke)
    def createCard(self):
        choice, pile, index = self.getinfo()  # henter info

        # opretter kort som skal tilføjes
        if self.cardType.get() == "Face down":
            card = None
        else:
            card = CardClass.Card(self.cardNum.get(), self.cardType.get(), None, None, None)

        # tilføjer kort til bunke
        size = len(pile)
        if choice == "Talon" and card is not None:
            if index == 0:
                pile.append(card)
            elif index < 3:
                pile.insert(size - index, card)
        elif choice[0:7] == "Tableau":
            if index < len(pile):
                pile.insert(index, card)
            else:
                pile.append(card)
        elif choice[0:10] == "Foundation" and card is not None:
            pile.append(card)

        self.gui.setCMD(None)   # sætter cmd til None da der ellers godt kan ske mærkelige bugs

    # knap funktion (fjerner kort fra bunke)
    def removeCard(self):
        choice, pile, index = self.getinfo()    # henter info

        # opretter kort som bruges til at tjekke om dt rigtige kort fjernes
        if self.cardType.get() == "Face down":
            card = None
        else:
            card = CardClass.Card(self.cardNum.get(), self.cardType.get(), None, None, None)
        size = len(pile)

        # Fjerner kort i den valgte bunke hvis kortet passer
        if choice == "Talon":
            if self.checkRemoveCards(card, pile[size - index - 1]) and card is not None:
                if index == 0:
                    pile.pop()
                elif index < 3:
                    pile.pop(size - index - 1)
        elif choice[0:7] == "Tableau":
            if self.checkRemoveCards(card, pile[index]):
                if index < len(pile):
                    pile.pop(index)
                else:
                    pile.pop()
        elif choice[0:10] == "Foundation":
            if self.checkRemoveCards(card, pile[size - 1]) and card is not None:
                pile.pop()

        self.gui.setCMD(None)   # sætter cmd til None da der ellers godt kan ske mærkelige bugs

    # knap funktion (lukker window)
    def close(self):
        self.master.destroy()
        self.master.update()

    # funktion som tjekker om det er det rigtige kort bliver fjernet
    def checkRemoveCards(self, card1, card2):
        if card1 is None and card2 is None:
            return True
        if card1 is None or card2 is None:
            return False
        elif card1.num == card2.num and card1.type == card2.type:
            return True
        else:
            return False

    # function som returnere pointer til bunke
    def getPile(self, choice):
        board = self.gui.board
        if choice == "Talon":
            return board.areaA[1]
        elif choice == "Tableau Row 1":
            return board.areaB[0]
        elif choice == "Tableau Row 2":
            return board.areaB[1]
        elif choice == "Tableau Row 3":
            return board.areaB[2]
        elif choice == "Tableau Row 4":
            return board.areaB[3]
        elif choice == "Tableau Row 5":
            return board.areaB[4]
        elif choice == "Tableau Row 6":
            return board.areaB[5]
        elif choice == "Tableau Row 7":
            return board.areaB[6]
        elif choice == "Foundation Spades":
            return board.areaC[0]
        elif choice == "Foundation Hearts":
            return board.areaC[1]
        elif choice == "Foundation Clubs":
            return board.areaC[2]
        elif choice == "Foundation Diamonds":
            return board.areaC[3]

    # returnere værdier skal variabler
    def getinfo(self):
        choice = self.cardPileVal.get()
        pile = self.getPile(choice)
        index = self.cardindex.get() - 1

        return choice, pile, index


# klasse der viser regler og hvordan spillet spilles
class Info:
    def __init__(self, master, gui):
        self.master = master
        self.gui = gui
        self.master.title("Info")   # title på window
        self.master.geometry("670x400")     # størrelse på window
        self.master.resizable(False, False)     # window kan ikke gøres større eller mindre

        # opretter klasser
        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.textbox = Text(master)
        self.textbox.pack()

        # henter string fra fil
        file = open("files/Rules.txt", "r")
        ruletxt = file.readlines()
        file.close()
        rtxt = " ".join(str(elem) for elem in ruletxt)

        # henter string fra fil
        file = open("files/Guide.txt", "r")
        guidetxt = file.readlines()
        file.close()
        gtxt = " ".join(str(elem) for elem in guidetxt)

        # concatenere de 2 strings
        txt = rtxt + gtxt

        # indsætter string i textbox
        self.textbox.insert(END, txt)

        # instillinger for textbox og scrollbars
        self.textbox.config(yscrollcommand=self.scrollbar.set, state=DISABLED)
        self.scrollbar.config(command=self.textbox.yview)
