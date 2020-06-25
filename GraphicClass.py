from tkinter import *
import ImgDataClass


# Graphic klasse som står for at optegne spillerbrættet i GUI
class Graphic:
    def __init__(self, tk, board, gui, sizeX, sizeY):
        self.board = board  # pointer to board

        # Window størrelse
        self.sizeX = sizeX
        self.sizeY = sizeY

        # intervaller bruges til at placere kort
        self.intervalX = sizeX / (len(board.areaB) + 1)
        self.intervalY = sizeY / 5

        # Offset til forskellige areas - bruges til at forskyde kort
        self.areaAOffset = 10
        self.areaBOffset = 16

        self.tk = tk  # pointer til GUI
        self.canvas = Canvas(self.tk, width=sizeX, height=sizeY, bg="Green")  # opretter window til grafik

        self.gui = gui  # variable til kommando
        self.drawFlag = True  # flag som bruges til at styre om der skal tegnes noget nyt
        self.aniCards = []  # liste som indeholder kort som skal flytte sig

        # styre opdatering af kort som er en animation
        self.turnDelay = 2
        self.turnDelayCount = 0

        # Laver billed objekter (laves i starten da dette kan tage langt tid)
        self.backSide = PhotoImage(file="images/Misc/Card_Back.gif")
        self.empty = PhotoImage(file="images/Misc/Empty.gif")
        self.frame = PhotoImage(file="images/Misc/Frame.gif")
        self.c_empty = PhotoImage(file="images/Misc/C_Empty.gif")
        self.d_empty = PhotoImage(file="images/Misc/D_Empty.gif")
        self.h_empty = PhotoImage(file="images/Misc/H_Empty.gif")
        self.s_empty = PhotoImage(file="images/Misc/S_Empty.gif")
        self.win = PhotoImage(file="images/Misc/WIN.gif")
        self.end = PhotoImage(file="images/Misc/END.gif")

        self.turn = []
        self.turn.append(PhotoImage(file="images/Misc/Turn_card0.gif"))
        self.turn.append(PhotoImage(file="images/Misc/Turn_card15.gif"))
        self.turn.append(PhotoImage(file="images/Misc/Turn_card30.gif"))
        self.turn.append(PhotoImage(file="images/Misc/Turn_card45.gif"))
        self.turn.append(PhotoImage(file="images/Misc/Turn_card60.gif"))
        self.turn.append(PhotoImage(file="images/Misc/Turn_card75.gif"))

        self.Clubs = []
        self.Clubs.append(PhotoImage(file="images/Clubs/C_1.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_2.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_3.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_4.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_5.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_6.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_7.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_8.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_9.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_10.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_11.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_12.gif"))
        self.Clubs.append(PhotoImage(file="images/Clubs/C_13.gif"))

        self.Diamonds = []
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_1.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_2.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_3.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_4.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_5.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_6.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_7.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_8.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_9.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_10.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_11.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_12.gif"))
        self.Diamonds.append(PhotoImage(file="images/Diamonds/D_13.gif"))

        self.Hearts = []
        self.Hearts.append(PhotoImage(file="images/Hearts/H_1.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_2.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_3.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_4.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_5.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_6.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_7.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_8.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_9.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_10.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_11.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_12.gif"))
        self.Hearts.append(PhotoImage(file="images/Hearts/H_13.gif"))

        self.Spades = []
        self.Spades.append(PhotoImage(file="images/Spades/S_1.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_2.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_3.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_4.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_5.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_6.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_7.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_8.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_9.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_10.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_11.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_12.gif"))
        self.Spades.append(PhotoImage(file="images/Spades/S_13.gif"))

        self.drawAreas()  # Optegner spillerbræt
        self.update()  # Optegner kort som skal flytte sig ud fra kommando

    # master funktion der tegne samtlige områder. Tegner de stille stående kort
    def drawAreas(self):
        self.drawAreaA()
        self.drawAreaB()
        self.drawAreaC()

    # optegner AreaA
    def drawAreaA(self):
        # optegner A0 (stoke)
        pile = self.board.areaA[0]
        pileSize = len(pile)
        # optegner 3 kort med bagsiden op hvis size er over eller lig 3
        if pileSize >= 3:
            for i in range(3):
                self.canvas.create_image(self.intervalX + self.areaAOffset * i, self.intervalY, image=self.backSide,
                                         anchor="center")
        # optegner mellem 1 eller 2 kort med bagsiden op afhæning af size
        elif 0 < pileSize < 3:
            for i in range(pileSize):
                self.canvas.create_image(self.intervalX + self.areaAOffset * i, self.intervalY, image=self.backSide,
                                         anchor="center")
        # optegner empty pile hvis size er 0
        else:
            self.canvas.create_image(self.intervalX, self.intervalY, image=self.empty, anchor="center")

        # optegner A0 (talon)
        pile = self.board.areaA[1]
        pileSize = len(pile)
        # optegner 3 kort hvis size er over eller lig 3
        if pileSize >= 3:
            for i in range(3):
                card = pile[pileSize - 3 + i]
                img = self.chooseCard(card)
                self.canvas.create_image(self.intervalX * 2 + self.areaAOffset * i, self.intervalY, image=img,
                                         anchor="center")
        # optegner mellem 1 eller 2 kort afhæning af size
        elif 0 < pileSize < 3:
            for i in range(pileSize):
                card = pile[i]
                img = self.chooseCard(card)
                self.canvas.create_image(self.intervalX * 2 + self.areaAOffset * i, self.intervalY, image=img,
                                         anchor="center")
        # optegner tomt frame hvis der ikke er nogen kort
        else:
            self.canvas.create_image(self.intervalX * 2, self.intervalY, image=self.frame, anchor="center")

    # optegner AreaB
    def drawAreaB(self):
        # går samtlige rækker igennem i areaB og tegner hvert kort med det Y coord offset forskelligt fra det tidligere kort
        for i in range(len(self.board.areaB)):
            pile = self.board.areaB[i]

            # hvis bunken er tom tegnes der tomt felt
            if len(pile) == 0:
                self.canvas.create_image(self.intervalX * (i + 1), self.intervalY * 2, image=self.frame,
                                         anchor="center")
            else:
                for j in range(len(pile)):

                    card = pile[j]
                    # hvis kort er nope tegnes der et kort med bagsiden op
                    if card is None:
                        self.canvas.create_image(self.intervalX * (i + 1), self.intervalY * 2 + self.areaBOffset * j,
                                                 image=self.backSide, anchor="center")
                    # ellers tegnes kortet
                    else:
                        img = self.chooseCard(card)
                        self.canvas.create_image(self.intervalX * (i + 1), self.intervalY * 2 + self.areaBOffset * j,
                                                 image=img, anchor="center")

    # optegner AreaC
    def drawAreaC(self):
        # går samtlige rækker igennem i areaC og tegner kun det sidste kort i listen da der ikke er offset
        for i in range(len(self.board.areaC)):
            img = None
            pile = self.board.areaC[i]
            pileSize = len(pile)

            if pileSize != 0:
                card = pile[pileSize - 1]
                img = self.chooseCard(card)
            else:
                if i == 0:
                    img = self.s_empty
                elif i == 1:
                    img = self.h_empty
                elif i == 2:
                    img = self.c_empty
                elif i == 3:
                    img = self.d_empty
                else:
                    print("Error drawAreaC!")

            self.canvas.create_image(self.intervalX * (i + 4), self.intervalY, image=img, anchor="center")

    # funktion som stå at udvælger hvilken kort der skal flytte sig ud fra cmd og ligge kortene i en speciel liste
    def cardAnimation(self):
        self.aniCards = []

        # bearbejde cmd
        [start, index, target] = self.gui.translateCMD(self.gui.cmd)
        # skaffer pointer til lister
        startPile = self.switchPile(start)
        targetPile = self.switchPile(target)

        cardCount = 0

        # Turn card animation
        if start == target and start[0] == "B":
            img = self.turn[0]  # sætter start img
            index = len(startPile[0]) - 1   # finder placering hvor animation skal tegnes
            # sætter coordinater
            xStart = startPile[1]
            yStart = startPile[2] + self.areaBOffset * index
            self.aniCards.append(ImgDataClass.ImgData(self.canvas, img, False, True, xStart, yStart, None, None))

        # hvis kort skal flyttes fra/i areaA
        elif start[0] == "A":
            # opsætning til for loop
            if len(startPile[0]) >= 3:
                s = len(startPile[0]) - 3
                e = len(startPile[0])
            else:
                s = 0
                e = len(startPile[0])

            # hvis kort flyttes i areaA
            if target[0] == "A":
                for i in range(s, e):
                    # hvis kort flyttes fra A0 til A1, kort med bagside op
                    if start == "A0":
                        img = self.backSide
                    # hvis kort flyttes fra A1 til A0, kort med front op
                    else:
                        card = startPile[0][i]
                        img = self.chooseCard(card)

                    # finder coordinater
                    xStart = startPile[1] + self.areaAOffset * cardCount
                    yStart = startPile[2]
                    xEnd = targetPile[1] + self.areaAOffset * cardCount
                    yEnd = targetPile[2]

                    # opretter klasser
                    self.aniCards.append(
                        ImgDataClass.ImgData(self.canvas, img, True, False, xStart, yStart, xEnd, yEnd))

                    cardCount += 1

            # hvis kort flyttes fra A til B eller C (kun et kort flyttes)
            else:
                # finder kort og sætter img
                card = startPile[0][len(startPile[0]) - 1]
                img = self.chooseCard(card)

                # bruges til at finde start coordinat
                size = len(startPile[0])
                if size >= 3:
                    buffer = 3
                else:
                    buffer = size

                # sætter coordinater
                xStart = startPile[1] + self.areaAOffset * buffer
                yStart = startPile[2]
                xEnd = targetPile[1]
                yEnd = 0

                # sætter y coordinat alt efter hvilken bunke kortet skal flyttes til
                if target[0] == "B":
                    yEnd = targetPile[2] + self.areaBOffset * len(targetPile[0])
                elif target[0] == "C":
                    yEnd = targetPile[2]

                self.aniCards.append(ImgDataClass.ImgData(self.canvas, img, True, False, xStart, yStart, xEnd, yEnd))

        # hvis kort skal flyttes fra/i areaB eller areaC
        elif start[0] == "B" or start[0] == "C":
            # bearbejder kort som skal gennemgp i række
            for i in range(index, len(startPile[0])):
                card = startPile[0][i]

                # tjekker om kort er None (ekstra fejl tjek (behøves enlig ikke))
                if card is not None:
                    # sætter koordinater
                    img = self.chooseCard(card)
                    xStart = startPile[1]
                    yStart = startPile[2] + self.areaBOffset * i
                    xEnd = targetPile[1]
                    if target[0] == "C":
                        yEnd = targetPile[2]
                    else:
                        yEnd = targetPile[2] + self.areaBOffset * (len(targetPile[0]) + cardCount)
                    self.aniCards.append(
                        ImgDataClass.ImgData(self.canvas, img, True, False, xStart, yStart, xEnd, yEnd))

                    cardCount += 1

        # hvis WIN
        elif start == "WIN":
            img = self.win
            self.aniCards.append(
                ImgDataClass.ImgData(self.canvas, img, False, False, self.sizeX / 2, self.sizeY / 2, None, None))

        # hvis End
        elif start == "END":
            img = self.end
            self.aniCards.append(
                ImgDataClass.ImgData(self.canvas, img, False, False, self.sizeX / 2, self.sizeY / 2, None, None))

    # update funktion der kaldes i mainloop
    def update(self):
        # hvis drawFlag er sat optegnes stillestående kort
        if self.drawFlag:
            self.drawFlag = False
            self.canvas.delete('all')
            self.drawAreas()

            # hvis der er cmd findes kort som skal animeres
            if self.gui.cmd is not None:
                self.cardAnimation()

        # der er cmd skal animations kort flyttes
        elif self.gui.cmd is not None:
            # gennemgår liste at animations kort
            for i in self.aniCards:
                # hvis kortet flyttes sig
                if i.moveFlag:
                    # flyttes kort x og y coordinat frem
                    if i.pauseFlag is False:
                        self.canvas.move(i.img, i.xMove, i.yMove)

                    # gemmer position af kort
                    pos = self.canvas.coords(i.img)
                    # kort stadig er mellem start og end position
                    if i.xMove > 0 and pos[0] >= i.xEnd or i.xMove < 0 and pos[0] <= i.xEnd or i.yMove > 0 and \
                            pos[1] >= i.yEnd or i.yMove < 0 and pos[1] <= i.yEnd:
                        i.pauseFlag = True

                        # reset kort efter pause
                        if i.pauseCount == i.pauseDelay:
                            i.standStillFlag = False
                            i.pauseFlag = False
                            i.pauseCount = 0
                            self.canvas.moveto(i.img, i.xStart - i.width / 2, i.yStart - i.height / 2)

                        # giver delay på kort som skal flytte sig
                        else:
                            i.pauseCount += 1
                            if i.standStillFlag is not True:
                                self.canvas.moveto(i.img, i.xEnd - i.width / 2, i.yEnd - i.height / 2)
                                i.standStillFlag = True

                # bruges til animation hvor billed skal skiftes ud med et andet billed (turn card)
                if i.aniFlag:
                    # når delay er ovre
                    if self.turnDelayCount == self.turnDelay:
                        self.turnDelayCount = 0

                        # vælger nyt billed
                        img = self.turn[i.turnImgCount]
                        i.changeImg(self.canvas, img)

                        # ændre hvilket billed der skal vises
                        if i.turnImgCount == len(self.turn) - 1:
                            i.turnImgCount = 0
                        else:
                            i.turnImgCount += 1

                    # giver delay
                    else:
                        self.turnDelayCount += 1

    # Function som returner billed af kort
    def chooseCard(self, card):
        img = None
        if card.type == "Clubs":
            img = self.Clubs[card.num - 1]
        elif card.type == "Diamonds":
            img = self.Diamonds[card.num - 1]
        elif card.type == "Hearts":
            img = self.Hearts[card.num - 1]
        elif card.type == "Spades":
            img = self.Spades[card.num - 1]
        else:
            print("Error chooseCard!")

        return img

    # Function som returnere bunke samt bunkens coordinater
    def switchPile(self, cmd):
        if cmd == "A0":
            return [self.board.areaA[0], self.intervalX, self.intervalY]
        elif cmd == "A1":
            return [self.board.areaA[1], self.intervalX * 2, self.intervalY]
        elif cmd == "B0":
            return [self.board.areaB[0], self.intervalX, self.intervalY * 2]
        elif cmd == "B1":
            return [self.board.areaB[1], self.intervalX * 2, self.intervalY * 2]
        elif cmd == "B2":
            return [self.board.areaB[2], self.intervalX * 3, self.intervalY * 2]
        elif cmd == "B3":
            return [self.board.areaB[3], self.intervalX * 4, self.intervalY * 2]
        elif cmd == "B4":
            return [self.board.areaB[4], self.intervalX * 5, self.intervalY * 2]
        elif cmd == "B5":
            return [self.board.areaB[5], self.intervalX * 6, self.intervalY * 2]
        elif cmd == "B6":
            return [self.board.areaB[6], self.intervalX * 7, self.intervalY * 2]
        elif cmd == "C0":
            return [self.board.areaC[0], self.intervalX * 4, self.intervalY]
        elif cmd == "C1":
            return [self.board.areaC[1], self.intervalX * 5, self.intervalY]
        elif cmd == "C2":
            return [self.board.areaC[2], self.intervalX * 6, self.intervalY]
        elif cmd == "C3":
            return [self.board.areaC[3], self.intervalX * 7, self.intervalY]
        else:
            return None
