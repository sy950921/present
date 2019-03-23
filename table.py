from gem import Gems
from card import Card,Noble

class Table():
    def __init__(self, tableData):
        """
        :param env: 输入环境信息

        """
        if "gems" in tableData:
            gems = tableData["gems"]
            self.gems = Gems(gems)
        if "cards" in tableData:
            cards = tableData["cards"]
            self.cards = []
            for card in cards:
                self.cards.append(Card(card))
        if "nobles" in tableData:
            nobles = tableData["nobles"]
            self.nobles = []
            for noble in nobles:
                self.nobles.append(Noble(noble))