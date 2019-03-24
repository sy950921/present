COLORS = ["red","blue","green","white","black","gold"]

class Gems():
    def __init__(self, gemData):
        self.data = {}
        for gemdata in gemData:
            color = gemdata["color"]
            count = int(gemdata["count"])
            self.data[color] = count
        for color in COLORS:
            if color not in self.data:
                self.data[color] = 0
    #     self.outData = gemData
    #
    # def getGems(self):
    #     return self.outData