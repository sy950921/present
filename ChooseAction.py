import random
import json

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
    def printbuycard(card):
        out = {}
        out["purchase_card"] = card[0].getCard()
        print(json.dumps(out))

    @staticmethod
    def printbuyreservedcard(card):
        out = {}
        out["purchase_card"] = card[0].getCard()
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
        if len(out) == 0:
            Action.printno_action()
        else:
            print(json.dumps(out))

    @staticmethod
    def printreservedcard(card):
        out = {}
        out["purchase_reserved_card"] = card.getCard()
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
            if card[0] in self.player1.reservedCards:
                Action.printbuyreservedcard(card)
            else:
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
            if len(self.player1.reservedCards)<3:#reserve没满
                card=self.choose_reserved_card(match=True)
                if card!=None:
                    Action.printreservedcard(card)
                else:
                    cards_need=self.has_need_card()
                    if cards_need==[]:
                        gems=self.choose_gems(num_of_can_take)
                        Action.printgems(gems)
                    else:
                        card_to_buy=self.purchase_card(cards_need,True)
                        if card_to_buy!=[]:
                            if card_to_buy in self.player1.reservedCards:
                                Action.printbuyreservedcard(card_to_buy)
                            else:
                                Action.printbuycard(card_to_buy)
                        else:
                            card_cloest=self.find_cloest_card()
                            gems=self.need_gems(card_cloest)
                            Action.printgems(gems)
            else:
                card_to_buy=self.purchase_card(self.table.cards,hasreserved=True)
                if card_to_buy!=None:
                    if card_to_buy in self.player1.reservedCards:
                        Action.printbuyreservedcard(card_to_buy)
                    else:
                        Action.printbuycard(card_to_buy)
                    # Action.printbuycard(card_to_buy)
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
        return [choose_card]

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
        # TODO 二等级卡只留一张
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
        need_color = []
        if self.player1.reservedCards != []:
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
                if self.player1.bonus[color]+self.player1.gems.data[color]-num==2 and self.table.gems.data[color]>=4:
                    gems = {"red": 0, "green": 0, "blue": 0, "white": 0, "black": 0}
                    gems[color]=2
                    break
                else:
                    gems[color]=1
                    num_take=num_take+1
                    if num_take>=3:
                        break
        return gems
