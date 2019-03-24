import sys
import random
import json

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


class Environment():
    def __init__(self, data):
        self.round = data["round"]
        self.playerName = data["playerName"]
        table = data["table"]
        players = data["players"]
        self.table = Table(table)

        assert len(players) == 3, "Number of Players should be %d, not %d!" % (int(3), len(players))

        for player in players:
            if player["name"] == self.playerName:
                self.player1 = Player(player)
            else:
                if not hasattr(self, 'player2'):
                    self.player2 = Player(player)
                else:
                    self.player3 = Player(player)
        if hasattr(self, 'player1') is None:
            print("Player: %s, not in players!" % self.playerName)
            exit()



class Action():
    def __init__(self, environment):
        self.gems_types=["red","green","blue","white","black","gold"]
        self.player1=environment.player1
        self.player2=environment.player2
        self.player3=environment.player3
        self.table=environment.table

    def __call__(self):
        over_gems,num_of_can_take=self.can_take_gems()
        if over_gems!=False:
            self.take_action(num_of_can_take)
        else:
            self.buy_card()

    @staticmethod
    def printbuycard(self, card):
        out = {}
        out["purchase_card"] = card.getCard()
        print(json.dumps(out))

    @staticmethod
    def printno_action():
        out = {}
        print(json.dumps(out))

    @staticmethod
    def printgems(gems):
        out = {}
        for color,num in gems:
            if num == 2:
                out["get_two_same_color_gems"] = color
            if num == 1:
                if len(out) == 0:
                    out["get_different_color_games"] = []
                    out["get_different_color_games"].append(color)
                else:
                    out["get_different_color_games"].append(color)

        print(json.dumps(out))

    @staticmethod
    def printreservedcard(card):
        out = {}
        out["reserve_card"] = card.getCard()
        print(json.dumps(out))

    def can_take_gems(self):
        """
        判断是否可以拿宝石
        :return:
            canTake(boolean): 是否可以拿宝石
            num_of_can_take(int): 可以拿多少宝石
        """
        sum_gems=0
        for gem,num in self.player1.gems.data.items():
            sum_gems=sum_gems+num
        if sum_gems>=10:
            return False, 0
        else:
            num_of_can_take=10-sum_gems
            return True, num_of_can_take

    def buy_card(self):
        """
        买牌
        :return: 操作
            printcard: 买牌
            printno_action: 轮空
        """
        table_cards=self.table.cards
        card=self.purchase_card(table_cards)
        if card!=[]:
            Action.printbuycard(card)
        else:
            Action.printno_action()

    def take_action(self,num_of_can_take):
        if self.player1.reservedCards==[]:
            card=self.choose_reserved_card()
            if card==None:
                gems=self.choose_gems(num_of_can_take)
                Action.printgems(gems)
            else:
                Action.printreservedcard(card)
        else:
            if len(self.player1.reserved_cards)<3:#reserve没满
                card=self.choose_reserved_card(match=True)
                if card!=None:
                    Action.printreservedcard(card)
                else:
                    cards_need=self.has_need_card()
                    if cards_need==[]:
                        gems=self.choose_gems()
                        Action.printgems(gems)
                    else:
                        card_to_buy=self.purchase_card(cards_need,True)
                        if card_to_buy!=[]:
                            Action.printbuycard(card_to_buy)
                        else:
                            card_cloest=self.find_cloest_card(cards_need)
                            gems=self.need_gems(card_cloest)
                            Action.printgems(gems)
            else:
                card_to_buy=self.purchase_card(self.table.cards,hasreserved=True)
                if card_to_buy!=None:
                    Action.printbuycard(card_to_buy)
                else:
                    gems=self.choose_gems(num_of_can_take)
                    Action.printgems(gems)

    def purchase_card(self,table_cards,hasreserved=False):
        """
        买牌
        :param table_cards(list): 桌面上所有牌
        :return:
            chooseCard(Card): 选中的牌
        """
        def cards_can_buy(table_cards,hasreserved):
            """
            找到所有可以买的牌
            :param table_cards(list): 桌面上所有的牌
            :return:
                posibleCards(list): 可选的牌
            """
            cards=[]

            if hasreserved:
                table_cards.extend(hasreserved)
                need_color_list=self.need_color()

            for card in table_cards:
                if hasreserved:
                    if card.color not in need_color_list:
                        continue
                num_gold = self.player1.gems["gold"]
                for color in self.gems_types:
                    if (card.costs[color]>self.player1.gems[color] + self.player1.bonus[color]):
                        num_gold=num_gold-(card.costs[color]-(self.player1.gems[color] + self.player1.bonus[color]))
                    if num_gold<0:
                        break
                    else:
                        continue
                cards.append(card)
            return cards

        cards = cards_can_buy(table_cards, hasreserved)
        if cards==[]:
            return cards
        else:
            choose_card=cards[0]
            top_score=choose_card.score
            for card in cards:
                score=card.score
                if score>top_score:
                    choose_card=card
                    top_score=score
        return choose_card

    def choose_gems(self,num_of_can_take):
        if num_of_can_take>3:
            num_of_can_take=3

        gems_can_take_in_table=["red","green","blue","white","black"]
        for color,num in self.table.gems.data.items():
            if num==0:
                del gems_can_take_in_table[color]

        gems={"red":0,"green":0,"blue":0,"white":0,"black":0}

        while (num_of_can_take!=0 and gems_can_take_in_table!=[]):
            i=random.randint(0,len(gems_can_take_in_table)-1)
            color=gems_can_take_in_table[i]
            gems[color]=1
            gems_can_take_in_table.remove(color)

        return gems

    def choose_reserved_card(self,match=False):
        if match:
            need_color_list=self.need_color()
        def matchcolor(need_color,card):
            extend_numcolor=0
            for color,num in card.reservedCards.costs.items():
                if color not in need_color:
                    extend_numcolor=extend_numcolor+1
            if len(need_color)==2 and extend_numcolor==0: return True
            if len(need_color)==1 and extend_numcolor<=1 \
                    and len(card.reservedCards.costs)==2: return True
            return False

        for card in self.table.cards:
            if match:
                if card.level!=1 and len(card.costs)<=2 and matchcolor(need_color_list,card):
                    return card
            else:
                if card.level!=1 and len(card.costs)<=2:
                    return card
        return None


    def need_color(self):
        """
        找到所有需要的颜色
        :return:
            need_color(list): 所有需要的颜色
        """
        need_color = [color for color, num in self.player1.reservedCards[0].costs.items()]
        if self.player1.reservedCards!=[] and \
                        self.player1.reservedCards[0].color not in need_color:
            need_color.append(self.player1.reservedCards[0].color)
        return need_color


    def has_need_card(self):
        cards_need=[]
        need_color_list=self.need_color()
        for card in self.table.cards:
            if card.color in need_color_list:
                cards_need.append(card)
        return cards_need

    def find_cloest_card(self):
        priosity_card={}
        for card in self.table.cards:
            priosity=1000
            for color,num in card.costs.items():
                if self.table.gems.data[color]+self.player1.gems.data[color]<num:
                    priosity=1000
                else:
                    priosity=priosity+self.player1.gems.data[color]-self.table.gems.data[color]
            priosity_card[priosity]=card

        priosity_sort = sorted(priosity_card.items(), key=lambda item: item[0])
        return priosity_sort[0][1]

    def need_gems(self,card_cloest):
        num_take=1
        gems = {"red": 0, "green": 0, "blue": 0, "white": 0, "black": 0}
        for color,num in card_cloest["costs"].items():
            if num<self.player1.bonus[color]+self.player1.gems.data[color]:
                if self.player1.bonus[color]+self.player1.gems.data[color]-num==2:
                    gems = {"red": 0, "green": 0, "blue": 0, "white": 0, "black": 0}
                    gems[color]=2
                    break
                else:
                    gems[color]=1
                    num_take=num_take+1
                    if num_take>=3:
                        break
        return gems


def input (filename="sample splendor request.json"):
    f =open(filename,"r")
    t = json.load(f)
    return t

if __name__ == '__main__':
    # filename = "test_input1.json"
    filename = sys.argv[1]
    data = input(filename)
    # data = sys.argv[1]
    # print(data)
    # print(type(data))
    # data = json.loads(sys.argv[1])
    # print("_________________________________________data___________________________________")
    # print(data)
    env = Environment(data)
    action=Action(env)
    action()