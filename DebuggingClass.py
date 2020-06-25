import random
import CardClass


class Debugging:
    def __init__(self, board):
        self.board = board

    # Function der flytter kort
    def moveCards(self, cmd):
        if cmd is not None:
            [start, index, target] = self.translateCMD(cmd)
            self.checkAreaA(start, target)
            self.checkAreaB(start, index, target)

    # Function som udføre cmd kommando hvis kommandoen starter med A
    def checkAreaA(self, start, target):
        if start == "A0" and target == "A1":  # Flytter et/flere kort fra AreaA[0] til AreaA[1] (trækker 3 nye kort)
            numCards = len(self.board.areaA[0])
            if numCards > 0:
                if numCards > 3:
                    numCards = 3
                for i in range(numCards):
                    self.board.areaA[1].append(self.board.unknownAreaA[0])
                    self.board.unknownAreaA.pop(0)
                    self.board.areaA[0].pop(0)
        elif start == "A1":
            if target == "A0":  # Flytter alle kort fra AreaA[1] til AreaA[0] (Vender bunken)
                self.board.areaA[1].reverse()

                for i in range(len(self.board.areaA[1])):
                    card = self.board.areaA[1][i]
                    self.board.unknownAreaA.append(card)

                self.board.areaA[1].clear()
                size = len(self.board.unknownAreaA)
                for i in range(size):
                    self.board.areaA[0].append(None)

            elif target[0] == "B":  # Flytter et kort fra AreaA[0] til AreaB
                num = int(target[1])
                card = self.board.areaA[1].pop()
                self.board.areaB[num].append(card)

            elif target[0] == "C":  # Flytter et kort fra AreaA[0] til AreaC
                num = int(target[1])
                card = self.board.areaA[1].pop()
                self.board.areaC[num].append(card)

    # Function som udføre cmd kommando hvis kommandoen starter med B
    def checkAreaB(self, start, index, target):
        if start[0] == "B":
            numS = int(start[1])
            numT = int(target[1])

            if start == target:  # Vender kort med bagsiden op ad i areaB
                self.board.areaB[numS].pop()
                card = self.board.unknownAreaB.pop()
                self.board.areaB[numS].append(card)
            else:  # Fytter kort fra AreaB til AreaB eller AreaC
                size = len(self.board.areaB[numS])
                if target[0] == "B":
                    for i in range(index, size):
                        card = self.board.areaB[numS][i]
                        self.board.areaB[numT].append(card)
                    for i in range(index, size):
                        self.board.areaB[numS].pop()

                elif target[0] == "C":
                    for i in range(index, size):
                        card = self.board.areaB[numS][i]
                        self.board.areaC[numT].append(card)
                    for i in range(index, size):
                        self.board.areaB[numS].pop()

    # translate function der deler kommandoen op i 2 strings og 1 int
    def translateCMD(self, cmd):
        temp = cmd.split("-")
        start = temp[0]
        temp = temp[1].split(",")
        index = int(temp[0])
        target = temp[1]

        return [start, index, target]

    # setup board function opstilt tilfældigt
    # Alle kort med bagsiden op er objekt "None", alle kort med forsiden er er kort objekt
    # Alle kort som ikke er i areaB men ikke kan ses af bruger er i bunke unknownAreaB
    # Alle andre kort som ikke kan ses er i bunke unknownAreaB
    # AreaA[0] er fyldt med ligeså mange "None" som der er kort i unknownAreaB
    def setupBoardRandom(self):
        # Adds and creates all cards to unknownAreaA
        self.board.unknownAreaA.append(CardClass.Card(1, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(2, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(3, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(4, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(5, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(6, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(7, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(8, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(9, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(10, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(11, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(12, "Clubs", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(13, "Clubs", None, None, None))

        self.board.unknownAreaA.append(CardClass.Card(1, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(2, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(3, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(4, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(5, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(6, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(7, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(8, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(9, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(10, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(11, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(12, "Diamonds", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(13, "Diamonds", None, None, None))

        self.board.unknownAreaA.append(CardClass.Card(1, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(2, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(3, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(4, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(5, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(6, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(7, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(8, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(9, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(10, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(11, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(12, "Spades", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(13, "Spades", None, None, None))

        self.board.unknownAreaA.append(CardClass.Card(1, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(2, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(3, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(4, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(5, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(6, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(7, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(8, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(9, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(10, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(11, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(12, "Hearts", None, None, None))
        self.board.unknownAreaA.append(CardClass.Card(13, "Hearts", None, None, None))

        random.shuffle(self.board.unknownAreaA)

        limit = 1
        for i in self.board.areaB:
            for j in range(limit):
                if j == limit - 1:
                    i.append(self.board.unknownAreaA[0])
                    limit += 1
                else:
                    i.append(None)
                    self.board.unknownAreaB.append(self.board.unknownAreaA[0])
                self.board.unknownAreaA.pop(0)

        for i in range(len(self.board.unknownAreaA)):
            self.board.areaA[0].append(None)
