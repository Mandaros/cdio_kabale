from tkinter import *


class Text:
    def __init__(self, tk, board, gui, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY

        self.board = board

        self.tk = tk
        self.canvas = Canvas(self.tk, width=sizeX, height=sizeY, bg="Black")    # opretter Canvas

        self.gui = gui
        self.drawFlag = True    # Flag som hlder styr på om noget nyt skal skrives

        self.update()

    # funktion som opdatere tekst i text canvas
    def update(self):
        if self.drawFlag:
            self.drawFlag = False
            self.canvas.delete('all')
            text = self.calcText()
            self.canvas.create_text(self.sizeX / 2, self.sizeY / 2, fill="yellow", font=10, text=text)

    # master funktion som samler alle tekst generator funktioner
    def calcText(self):
        text = ""
        if self.gui.cmd is not None:
            [start, index, target] = self.gui.translateCMD(self.gui.cmd)
            text += self.textAreaA(start, target)
            text += self.textAreaB(start, index, target)
            text += self.textWinEnd(start)
        else:
            text = "Press \"Calculate next Move\" when ready"

        return text

    # funktion som er ansvarlig for at generer tekst hvis der sker handlig i/fra areaA
    def textAreaA(self, start, target):
        text = ""
        if start == "A0":
            size = len(self.board.areaA[0])
            if size >= 3:
                i = 3
            else:
                i = size
            text += "Move " + str(i) + " cards from the Stoke to the Talon"
        elif start == "A1":
            if target == "A0":
                text += "Reset the Stoke, by turning over the Talon"
            else:
                card = self.board.areaA[1][len(self.board.areaA[1]) - 1]
                text += ("Move " + self.getNum(card.num) + " of " + card.type + " from the Talon to ")

                if target[0] == "B":
                    text += "the Tableau (Row " + str(target[1]) + ")"
                elif target[0] == "C":
                    if target[1] == "0":
                        text += card.type + " "
                    elif target[1] == "1":
                        text += card.type + " "
                    elif target[1] == "2":
                        text += card.type + " "
                    elif target[1] == "3":
                        text += card.type + " "
                    text += "Foundation"

        return text

    # funktion som er ansvarlig for at generer tekst hvis der sker handlig i/fra areaB
    def textAreaB(self, start, index, target):
        text = ""
        if start[0] == "B":
            pile = self.board.areaB[int(start[1])]
            card = pile[index]
            size = len(pile)

            if start == target:
                text += "Turn over last card in the Tableau (Row " + str(int(start[1]) + 1) + ")"
            else:
                text += "Move "

                if index < size - 1:
                    text += self.getNum(card.num) + " of " + card.type + " and above laying card(s) in the Tableau (Row " + str(
                        int(start[1]) + 1) + ") "

                elif index == size - 1:
                    text += self.getNum(card.num) + " of " + card.type + " in the Tableau (Row " + str(int(start[1]) + 1) + ") "

                text += "\n"

                if target[0] == "B":
                    text += "to Row " + str(int(target[1]) + 1) + " in the Tableau"

                elif target[0] == "C":
                    text += "to the " + card.type + " Foundation"

        return text

    # genere win/end tekst
    def textWinEnd(self, start):
        text = ""
        if start == "WIN":
            text += "You have solved the Solitaire! ^^ Congratulations!"
        elif start == "END":
            text += "The Solitaire couldn't be solved... Better luck next time."

        return text

    # return navn på kort
    def getNum(self, num):
        if num == 11:
            return "Jack"
        elif num == 12:
            return "Queen"
        elif num == 13:
            return "King"
        elif num == 1:
            return "Ace"
        else:
            return str(num)
