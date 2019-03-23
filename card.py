class Card():
    def __init__(self, cardData):
        """
        :param cardData: 输入卡片的数据字典

        attr:
            level(int); 等级
            score(int): 牌分（0-5）
            color(str): 颜色
            costs(dict):
                    key(str)：颜色
                    value(int)：数量
            cardValue(int): 牌的价值（1-3，3表示价值最高）

        """
        self.level = int(cardData["level"])
        if "score" not in cardData:
            self.score = 0
        else:
            self.score = int(cardData["score"])
        self.color = cardData["color"]
        self.costs = {}
        costs = cardData["costs"]
        self.allCount = 0
        for cost in costs:
            color = cost["color"]
            count = int(cost["count"])
            self.costs[color] = count
            self.allCount += count
        self.cardValue = self.getCardValue()
        self.outData = cardData

    def getCard(self):
        return self.outData

    def getCardValue(self):
        if self.level == 3:
            if self.allCount == 14:
                value = 1
            elif self.allCount == 12:
                value = 2
            else:
                value = 3
        elif self.level == 2:
            if self.score == 1:
                value = 1
            elif self.allCount <= 6:
                value = 3
            else:
                value = 2
        else:
            if self.score == 1 or self.allCount == 3:
                value = 3
            elif self.allCount == 4:
                value = 2
            else:
                value = 1
        return value


class Noble():
    def __init__(self, nobleData):
        """
        :param nobleData: 输入贵族的数据字典

        attr:
            score(int): 牌分（0-5）
            requirement(dict):
                    key(str)：颜色
                    value(int)：数量
        """
        self.score = int(nobleData["score"])
        self.requirements = {}
        requirements = nobleData["requirements"]
        for requ in requirements:
            color = requ["color"]
            count = int(requ["count"])
            self.requirements[color] = count