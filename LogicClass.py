class Logic:
    def __init__(self, board):
        self.board = board

        # bruges tl at holde styr på om spillet er tabt
        self.endLimit = 3
        self.endCount = 0

        self.types = []
        self.types.append("Spades")
        self.types.append("Hearts")
        self.types.append("Clubs")
        self.types.append("Diamonds")

        self.cmdCount = -1

    # Master function som returnere cmd
    def calcCMD(self):
        tempCMD = self.Win()
        if tempCMD is not None:
            return tempCMD

        tempCMD = self.TurnCard()
        if tempCMD is not None:
            return tempCMD

        tempCMD = self.addCardBtoBnC()
        if tempCMD is not None:
            return tempCMD

        tempCMD = self.addCardAtoC()
        if tempCMD is not None:
            return tempCMD

        tempCMD = self.addCardBtoC()
        if tempCMD is not None:
            return tempCMD

        tempCMD = self.addCardAtoB()
        if tempCMD is not None:
            return tempCMD

        tempCMD = self.newCards()
        if tempCMD is not None:
            return tempCMD

        tempCMD = self.end()
        if tempCMD is not None:
            return tempCMD

        tempCMD = self.resetCards()
        if tempCMD is not None:
            return tempCMD
 
    # Funktion som tjekker om kort skal vendes i areaB (bagside -> forside)
    def TurnCard(self):
        area = self.board.areaB
        size = len(area)

        for i in range(size):
            lastCardNum = len(area[i]) - 1
            if lastCardNum >= 0:
                if area[i][lastCardNum] is None:
                    return "B" + str(i) + "-0,B" + str(i)
        return None

    # funktion som tjekker om der kan trækkes 3 nye kort
    def newCards(self):
        area = self.board.areaA
        size = len(area[0])

        if size > 0:
            return "A0-0,A1"
        return None

    # funktion som tjekker om Talon skal laves om til Stoke
    def resetCards(self):
        area = self.board.areaA
        size = len(area[0])

        if size == 0:
            self.endCount += 1
            return "A1-0,A0"
        return None

    # tjekker om spillet er tabt
    def end(self):
        if self.endCount >= 3:
            return "END-0,A0"
        return None

    # tjekker om spillet er vundet
    def Win(self):
        area = self.board.areaC

        # laver pointer til det øvreste kort i de 4 foundation bunker
        i = len(area[0]) - 1
        if i >= 0:
            sCard = area[0][i]
        else:
            return None

        i = len(area[1]) - 1
        if i >= 0:
            hCard = area[1][i]
        else:
            return None

        i = len(area[2]) - 1
        if i >= 0:
            cCard = area[2][i]
        else:
            return None

        i = len(area[3]) - 1
        if i >= 0:
            dCard = area[3][i]
        else:
            return None

        # tjekker om de 4 kort er konger af rigtig kulør
        if self.checkKing(sCard, "Spades") and self.checkKing(hCard, "Hearts") and self.checkKing(cCard,"Clubs") \
                and self.checkKing(dCard, "Diamonds"):
            return "WIN-0,A0"
        return None

    # tjekker om kort fra areaA kan tilføjes til areaB
    def addCardAtoB(self):
        # laver pointer til kort hvis der er et i bunke areaA[1]
        i = len(self.board.areaA[1])
        if i > 0:
            card = self.board.areaA[1][i - 1]
        else:
            return None

        # gennemgår lister i areaB
        j = len(self.board.areaB)
        for i in range(j):
            pile = self.board.areaB[i]
            size = len(pile)
            if size == 0:   # tjekker om kort er konge og bunke den evt kan flyttes til er tom
                if card.num == 13:
                    self.endCount = 0
                    return "A1-0,B" + str(i)
            else:   # tjekker om kort kan flyttes til bunke beseret på kort nummer og type
                target = pile[size - 1]
                if self.checkValidCardMove(card, target):
                    self.endCount = 0
                    return "A1-0,B" + str(i)
        return None

    # Tjekker om kort fra areaA kan flyttes til areaC
    def addCardAtoC(self):
        # laver pointer til kort
        i = len(self.board.areaA[1])
        if i > 0:
            card = self.board.areaA[1][i - 1]
        else:
            return None

        j = len(self.board.areaC)
        for i in range(j):
            pile = self.board.areaC[i]
            size = len(pile)
            if card.type == self.types[i]:  # tjekker om kort er den rigtige type iforhold til den bunke som kigges på
                if size == 0:   # hvis bunken er tom kan kun es kortet tilføjes
                    if card.num == 1:
                        self.endCount = 0
                        return "A1-0,C" + str(i)
                else:   # hvis bunke ikke er tom kan kun næste kort i rækken tilføjes
                    target = pile[size - 1]
                    if card.num - 1 == target.num:
                        self.endCount = 0
                        return "A1-0,C" + str(i)
        return None

    def addCardBtoBnC(self):
        sizeB = len(self.board.areaB)
        card = None

        for i in range(sizeB):  # for loop der går igennem areaB 2D array
            pile = self.board.areaB[i]  # gemmer 1D array in pile
            sizePile = len(pile)  # gemmer størrelse på pile (1D array)
            j = 0
            if sizePile > 0:  # hvis pile størrelsen er større end 0. altså der er kort i bunken
                for j in range(sizePile):  # finder det første fra toppen som ikke har bagsiden op ad
                    card = pile[j]
                    if card is not None:
                        break

                if j == sizePile - 1:  # hvis kortet har den sidste placering (Der ikke ligger nogen kort oven på kortet)
                    pileC = self.board.areaC
                    sizeC = len(pileC)
                    for n in range(sizeC):  # gennemgår areaC for at tjekke om kortet kan flyttes fra C til B
                        if card.type == self.types[n]:
                            sizeTemp = len(pileC[n])
                            if sizeTemp > 0:
                                target = pileC[n][sizeTemp - 1]
                                if card.num - 1 == target.num:
                                    self.endCount = 0
                                    return "B" + str(i) + "-" + str(j) + ",C" + str(n)
                            elif card.num == 1:
                                self.endCount = 0
                                return "B" + str(i) + "-" + str(j) + ",C" + str(n)

                for n in range(sizeB):  # gennemgår AreaB igen for at tjekke om kortet og dets tilbehør kan flyttes
                    if i == n:
                        continue
                    pileTarget = self.board.areaB[n]
                    size = len(pileTarget)
                    if j > 0 and card.num == 13 and size == 0:
                        self.endCount = 0
                        return "B" + str(i) + "-" + str(j) + ",B" + str(n)
                    elif size > 0:
                        target = pileTarget[size - 1]
                        if self.checkValidCardMove(card, target):
                            self.endCount = 0
                            return "B" + str(i) + "-" + str(j) + ",B" + str(n)
        return None

    # tjekker om kort kan flyttes fra areaB til areaC
    def addCardBtoC(self):
        j = len(self.board.areaB)
        m = len(self.board.areaC)

        # gennemgår areaB
        for i in range(j):
            pile = self.board.areaB[i]
            sizeB = len(pile)

            # laver pointer til sidste kort i bunken
            if sizeB > 0:
                card = pile[sizeB - 1]

                # gennemgår areaC
                for n in range(m):
                    targetPile = self.board.areaC[n]
                    sizeC = len(targetPile)
                    if sizeC > 0:   # hvis bunken ikke er tom tjekkes der om kortet er det tilføjes til bunken
                        targetCard = targetPile[sizeC - 1]
                        if card.type == targetCard.type and card.num - 1 == targetCard.num:
                            self.endCount = 0
                            return "B" + str(i) + "-" + str(sizeB - 1) + ",C" + str(n)
                    else:   # hvis bunken er tom tjekkes der om kort er es og rigtig type
                        if card.num == 1 and card.type == self.types[n]:
                            self.endCount = 0
                            return "B" + str(i) + "-" + str(sizeB - 1) + ",C" + str(n)

    # tjekker om et kort kan flyttes til ny bunke (gælder kun for areaB)
    def checkValidCardMove(self, card, targetCard):
        typeFlag = False
        numFlag = False

        if (card.type == "Hearts" or card.type == "Diamonds") and \
                (targetCard.type == "Clubs" or targetCard.type == "Spades"):
            typeFlag = True
        elif (card.type == "Clubs" or card.type == "Spades") and \
                (targetCard.type == "Hearts" or targetCard.type == "Diamonds"):
            typeFlag = True

        if card.num == targetCard.num - 1 and targetCard.num > 1:
            numFlag = True

        if numFlag and typeFlag:
            return True
        return False

    # tjekker om kort er konge og rigtig type
    def checkKing(self, card, cardType):
        if card.type == cardType and card.num == 13:
            return True
        return False


def noneSort(i):
    return i.num
