from gem import Gems
from card import Card, Noble

COLORS = ["red","blue","green","white","black","gold"]

class Player():
    def __init__(self, playerData):
        """
        :param env(dict): 输入数据
        :param playerID(int): 玩家ID

        out:
            name(str): 玩家姓名
            score(int): 玩家分数
            gems(list): 玩家拥有宝石
            purchasedCards(list): 玩家拥有的牌
            reservedCards(list): 玩家保留的牌
            nobles(list): 玩家拥有的贵族
        """
        data = playerData
        self.name = data["name"]
        if "score" in data:
            self.score = int(data["score"])
        if "gems" in data:
            gems = data["gems"]
            self.gems = Gems(gems)
        else:
            gems = {}
            self.gems = Gems(gems)
        if "purchasedCards" in data:
            purchasedCards = data["purchasedCards"]
            self.purchasedCards = []
            for card in purchasedCards:
                self.purchasedCards.append(Card(card))
        else:
            self.purchasedCards = []
        if "reservedCards" in data:
            reservedCards = data["reservedCards"]
            self.reservedCards = []
            for card in reservedCards:
                self.reservedCards.append(Card(card))
        else:
            self.reservedCards = []
        if "nobles" in data:
            nobles = data["nobles"]
            self.nobles = []
            for noble in nobles:
                self.nobles.append(Noble(noble))
        else:
            self.nobles = []

        self.bonus = self.getBonus()

    def getBonus(self):
        bonus = {}
        for color in COLORS:
            bonus[color] = 0
        if hasattr(self, "purchasedCards"):
            for card in self.purchasedCards:
                bonus[card.color] += 1
        return bonus
