from __future__ import print_function


class Board:
    def __init__(self, gui, mode):
        self.gui = gui

        # Create lists used
        self.unknownAreaA = []
        self.unknownAreaB = []

        self.areaA = []
        self.buffAreaA1 = []
        for i in range(2):
            row = []
            self.areaA.append(row)

        # Opretter lister hvor kort holdes, samt buffer lister som bruges til at bearbejde input fra CV
        self.areaB = []
        self.buffAreaB = []
        for i in range(7):
            row0 = []
            row1 = []
            self.buffAreaB.append(row0)
            self.areaB.append(row1)

        self.areaC = []
        self.buffAreaC = []
        for i in range(4):
            row0 = []
            row1 = []
            self.buffAreaC.append(row0)
            self.areaC.append(row1)

        # Indsætter kort med bagsiden opad i areaB
        if mode is False:
            limit = 0
            for i in self.areaB:
                for j in range(limit):
                    i.append(None)
                limit += 1

        #self.boardWidth = 0
        #self.boardHeight = 0

        #self.CoordAreaA = [2]
        #self.CoordAreaB = [7]
        #self.CoordAreaC = [4]

        self.sizeAreaACount = [24, 0]

    # Master funktion som bearbejder input fra CV og indsætter på board
    def inputProcessing(self, list, width, height, verticalBorder, cmd):
        if cmd is not None:
            self.cmdChanges(cmd)

        list = self.sortOutDoubles(list)
        self.sortIntoAreas(list, width, height, verticalBorder)
        self.sortAreas()

    # function som ændre tæller og flytter kort rundet alt efter hvad cmd er
    def cmdChanges(self, cmd):
        start, index, target = self.gui.translateCMD(cmd)
        if start[0] == "B":
            startNum = int(start[1])
            targetNum = int(target[1])
            if start == target:  # tjekker om kort skal vendes i area B
                self.areaB[startNum].pop(0)
            elif target[0] == "B":  # flytter kort rundt fra areaB til areaB
                size = len(self.areaB[startNum])
                for i in range(index, size):
                    card = self.areaB[startNum][i]
                    self.areaB[targetNum].append(card)
                for i in range(size - 1, index - 1, -1):
                    self.areaB[startNum].pop(i)
            elif target[0] == "C":  # flytter kort fra areaB til areaC
                card = self.areaB[startNum].pop(index)
                self.areaC[targetNum].append(card)

        elif start == "A0" and target == "A1":  # ændre tæller som holder styr på hvor mange kort som er i areaA
            n = self.sizeAreaACount[0]
            if n >= 3:
                self.sizeAreaACount[0] -= 3
                self.sizeAreaACount[1] += 3
            else:
                self.sizeAreaACount[0] -= n
                self.sizeAreaACount[1] += n
        elif start == "A1" and target == "A0":  # nulstiller areaA
            self.sizeAreaACount[0] = self.sizeAreaACount[1]
            self.sizeAreaACount[1] = 0
            self.areaA[1].clear()
        elif start == "A1": # flytter kort fra areaA til areaB eller areaC
            self.sizeAreaACount[1] -= 1
            if target[0] == "B":
                card = self.areaA[1].pop()
                self.areaB[int(start[1])].append(card)
            if target[0] == "C":
                card = self.areaA[1].pop()
                self.areaC[int(start[1])].append(card)

    # funktion som sortere kort ud hvis samme kort står flere gange i listen
    # et kort bliver sortere fra hvis der er en mindre sandsynlighed
    def sortOutDoubles(self, list):
        buffer = [None] * (52 + 1)
        placement = 0
        for i in list:
            if i.type == "Clubs":
                placement = 13 * 0
            elif i.type == "Diamonds":
                placement = 13 * 1
            elif i.type == "Spades":
                placement = 13 * 2
            elif i.type == "Hearts":
                placement = 13 * 3

            if buffer[i.num + placement] is None:
                buffer[i.num + placement] = i
            elif buffer[i.num + placement].prob < i.prob:
                buffer[i.num + placement] = i

        result = []
        for i in buffer:
            if i is not None:
                result.append(i)

        return result

    # sortere kort ind i forskellige lister baseret på kortets x og y koordinat
    def sortIntoAreas(self, list, width, height, verticalBorder):
        wI = int(width / 7)
        hI = verticalBorder
        for i in list:
            x = i.xCoord
            y = i.yCoord
            if 0 <= y <= hI:
                if wI <= x <= wI * 3:
                    self.buffAreaA1.append(i)
                elif wI * 3 < x <= wI * 4 and i.type == "Spades":
                    self.buffAreaC[0].append(i)
                elif wI * 4 < x <= wI * 5 and i.type == "Hearts":
                    self.buffAreaC[1].append(i)
                elif wI * 5 < x <= wI * 6 and i.type == "Clubs":
                    self.buffAreaC[2].append(i)
                elif wI * 6 < x <= width and i.type == "Diamonds":
                    self.buffAreaC[3].append(i)
            elif hI < y <= height:
                if 0 <= x <= wI:
                    self.buffAreaB[0].append(i)
                elif wI < x <= wI * 2:
                    self.buffAreaB[1].append(i)
                elif wI * 2 < x <= wI * 3:
                    self.buffAreaB[2].append(i)
                elif wI * 3 < x <= wI * 4:
                    self.buffAreaB[3].append(i)
                elif wI * 4 < x <= wI * 5:
                    self.buffAreaB[4].append(i)
                elif wI * 5 < x <= wI * 6:
                    self.buffAreaB[5].append(i)
                elif wI * 6 < x <= width:
                    self.buffAreaB[6].append(i)

    # Funktion som flytter elementer fra buffer lister til area lister
    def sortAreas(self):
        # sletter alle elementer i areaA[0] og tilføjer den mængde at kort som er i bunken
        self.areaA[0].clear()
        for i in range(self.sizeAreaACount[0]):
            self.areaA[0].append(None)

        self.buffAreaA1.sort(key=self.xSort)  # Sortere kort efter X coordinat
        self.compareAndAdd(self.areaA[1], self.buffAreaA1)  # tilføjer nye kort fra buffer til area liste som ikke allerede er i area liste
        self.buffAreaA1.clear() # nulstiller buffer

        for i in self.buffAreaB:  # Sortere kort efter Y coordinat
            i.sort(key=self.ySort)
        for i in range(len(self.areaB)):    # tilføjer nye kort fra buffer til area liste som ikke allerede er i area liste
            self.compareAndAdd(self.areaB[i], self.buffAreaB[i])
        for i in self.buffAreaB:    # nulstiller buffer
            i.clear()

        for i in range(len(self.areaC)):    # tilføjer nye kort fra buffer til area liste som ikke allerede er i area liste
            self.compareAndAdd(self.areaC[i], self.buffAreaC[i])
        for i in self.buffAreaC:    # nulstiller buffer
            i.clear()

    # funktion som sammeligner to lister og tilføjer elementer fra buffer til boardArea som ikke er i boardarea
    def compareAndAdd(self, boardArea, buffer):
        temp = []
        for j in buffer:
            cond = True
            for n in boardArea:
                if n is not None:
                    if j.type == n.type and j.num == n.num:
                        cond = False
            if cond:
                temp.append(j)

        for j in temp:
            boardArea.append(j)

    def xSort(self, i):
        return i.xCoord

    def ySort(self, i):
        return i.yCoord
