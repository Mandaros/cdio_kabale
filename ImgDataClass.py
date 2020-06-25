# Klasse som bruger til at vise billed i GUI
class ImgData:
    def __init__(self, canvas, img, moveFlag, aniFlag, xStart, yStart, xEnd, yEnd):
        self.img = canvas.create_image(xStart, yStart, image=img, anchor="center")

        self.width = img.width()  # gemmer billed bredte
        self.height = img.height()  # gemmer billed højde

        self.moveFlag = moveFlag  # flag som fortæller om billed and flytte sig eller være stillestående
        self.aniFlag = aniFlag

        self.pauseFlag = False
        self.pauseDelay = 30
        self.pauseCount = 0
        self.standStillFlag = False

        self.xStart = xStart  # start x coordinat
        self.yStart = yStart  # start y coordinat

        self.xEnd = xEnd  # mål x coordinat
        self.yEnd = yEnd  # mål y coordinat

        if self.moveFlag:  # beregner x og y vektor hvis billed skal flytte sig
            vector = self.calcVector()
            self.xMove = vector[0]
            self.yMove = vector[1]

        if self.aniFlag:  # sætter count hvis billed er animation som er stillestående
            self.turnImgCount = 0

    # skifter billed ved at slette gammelt billed og lave et nyt billed
    def changeImg(self, canvas, img):
        canvas.delete(self.img)
        self.img = canvas.create_image(self.xStart, self.yStart, image=img, anchor="center")

    # Beregner x og y vektor baseret på hvilken retning billedet flytter sig.
    # Billedet kan max flytte sig 2.5 pixel pga. limit = 2.5
    def calcVector(self):
        limit = 2.5
        n = 1
        cond = True

        xDiff = self.xEnd - self.xStart
        yDiff = self.yEnd - self.yStart

        xTemp = 0
        yTemp = 0

        if xDiff > 0 and yDiff > 0:
            while cond:
                xTemp = xDiff / n
                yTemp = yDiff / n
                if xTemp <= limit and yTemp <= limit:
                    cond = False
                else:
                    n += 1

        elif xDiff < 0 and yDiff > 0:
            while cond:
                xTemp = xDiff / n
                yTemp = yDiff / n
                if xTemp >= -limit and yTemp <= limit:
                    cond = False
                else:
                    n += 1

        elif xDiff < 0 and yDiff < 0:
            while cond:
                xTemp = xDiff / n
                yTemp = yDiff / n
                if xTemp >= -limit and yTemp >= -limit:
                    cond = False
                else:
                    n += 1

        elif xDiff > 0 and yDiff < 0:
            while cond:
                xTemp = xDiff / n
                yTemp = yDiff / n
                if xTemp <= limit and yTemp >= -limit:
                    cond = False
                else:
                    n += 1

        elif xDiff > 0 and yDiff == 0:
            while cond:
                xTemp = xDiff / n
                yTemp = yDiff / n
                if xTemp <= limit:
                    cond = False
                else:
                    n += 1

        elif xDiff < 0 and yDiff == 0:
            while cond:
                xTemp = xDiff / n
                yTemp = yDiff / n
                if xTemp >= -limit:
                    cond = False
                else:
                    n += 1

        elif xDiff == 0 and yDiff > 0:
            while cond:
                xTemp = xDiff / n
                yTemp = yDiff / n
                if yTemp <= limit:
                    cond = False
                else:
                    n += 1

        elif xDiff == 0 and yDiff < 0:
            while cond:
                xTemp = xDiff / n
                yTemp = yDiff / n
                if yTemp >= -limit:
                    cond = False
                else:
                    n += 1

        return [xTemp, yTemp]
