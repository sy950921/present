import random


class Action():
    def __init__(self,Environment):
        self.gems_types=["red","green","bleu","white","black","gold"]
        self.player1=Environment.player1
        self.player2=Environment.player2
        self.player3=Environment.player3
        self.table=Environment.table

    def __call__(self):
        over_gems,num_of_can_take=self.can_take_gems()
        if over_gems!=False:
            self.take_action(num_of_can_take)
        else:
            self.buy_card()

    def can_take_gems(self):
        sum_gems=0
        for gem,num in self.player1.gems.items():
            sum_gems=sum_gems+num
        if sum_gems>=10:
            return False, 0
        else:
            num_of_can_take=10-sum_gems
            return True, num_of_can_take

    def buy_card(self):
        table_cards=self.table["cards"]
        card=self.purchase_card(table_cards)
        if card!=[]:
            printbuycard(card)
        else:
            printno_action()

    def take_action(self,num_of_can_take):
        if self.player1.reserved_cards==[]:
            card=self.choose_reserved_card()
            if card==None:
                gems=self.choose_gems(num_of_can_take)
                printgems(gems)
            else:
                printreservedcard(card)
        else:
            if len(self.player1.reserved_cards)<3:#reserve没满
                card=self.choose_reserved_card(match=True)
                if card!=None:
                    printreservedcard(card)
                else:
                    cards_need=self.has_need_card()
                    if cards_need==[]:
                        gems=self.choose_gems()
                        printgems(gems)
                    else:
                        card_to_buy=self.purchase_card(cards_need,True)
                        if card_to_buy!=[]:
                            printbuycard(card_to_buy)
                        else:
                            card_cloest=find_cloest_card(cards_need)
                            gems=self.need_gems(card_cloest)
                            printgems(gems)
            else:
                card_to_buy=self.purchase_card(self.table["cards"],hasreserved=True)
                if card_to_buy!=None:
                    printbuycard(card_to_buy)
                else:
                    gems=self.choose_gems(num_of_can_take)
                    printgems(gems)




    def purchase_card(self,table_cards,hasreserved=False):
        def cards_can_buy(table_cards,hasreserved):
            cards=[]

            if hasreserved:
                table_cards.extend(hasreserved)
                need_color_list=self.need_color()

            for card in table_cards:
                if hasreserved:
                    if card["color"] not in need_color_list:
                        continue
                num_gold = self.player1.gems["gold"]
                for color in self.gems_types:
                    if (card["costs"][color]>(self.player1.gems[color]+self.bonus[color])):
                        num_gold=num_gold-\
                                 (card["costs"][color]-self.player1.gems[color]-self.bonus[color])
                    if num_gold<0:
                        break
                    else:
                        continue
                cards.append(card)
            return cards

        cards=cards_can_buy(table_cards,hasreserved)
        if cards==[]:
            return cards
        else:
            choose_card=cards[0]
            top_score=choose_card["score"]
            for card in cards:
                score=card["score"]
                if score>top_score:
                    choose_card=card
                    top_score=score
        return choose_card

    def choose_gems(self,num_of_can_take):
        if num_of_can_take>3:
            num_of_can_take=3

        gems_can_take_in_table=["red","green","blue","white","black"]
        for color,num in self.table.gems.items():
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
            for color,num in card.reserved_cards["requirements"].items():
                if color not in need_color:
                    extend_numcolor=extend_numcolor+1
            if len(need_color)==2 and extend_numcolor==0: return True
            if len(need_color)==1 and extend_numcolor<=1 \
                    and len(card.reserved_cards["requirements"])==2: return True
            return False

        for card in self.table.cards:
            if match:
                if card["level"]!=1 and len(card["costs"])<=2 and matchcolor(need_color,card):
                    return card
            else:
                if card["level"]!=1 and len(card["costs"])<=2:
                    return card
        return None

    def need_color(self):
        need_color = [color for color, num in self.player1.reserved_cards[0]["requirements"].items()]
        if self.player1.reserved_cards!=[] and \
                        self.player1.reserved_cards[0]["color"] not in need_color:
            need_color.append(self.player1.reserved_cards[0]["color"])
        return need_color

    def has_need_card(self):
        cards_need=[]
        need_color_list=self.need_color()
        for card in self.table.cards:
            if card["color"] in need_color_list:
                cards_need.append(card)
        return cards_need

    def find_cloest_card(self):
        priosity_card={}
        for card in self.table.cards:
            priosity=1000
            for color,num in card.requirements.items():
                if self.table.gems["color"]+self.player1.gems["color"]<num:
                    priosity=1000
                else:
                    priosity=priosity+self.player1.gems["color"]-self.table.gems["color"]
            priosity_card[priosity]=card

        priosity_sort = sorted(priosity_card.items(), key=lambda item: item[0])
        return priosity_sort[0][1]

    def need_gems(self,card_cloest):
        num_take=1
        gems = {"red": 0, "green": 0, "blue": 0, "white": 0, "black": 0}
        for color,num in card_cloest["costs"].items():
            if num<self.player1.bonus[color]+self.player1.gems[color]:
                if self.player1.bonus[color]+self.player1.gems[color]-num==2:
                    gems = {"red": 0, "green": 0, "blue": 0, "white": 0, "black": 0}
                    gems[color]=2
                    break
                else:
                    gems[color]=1
                    num_take=num_take+1
                    if num_take>=3:
                        break
        return gems

        return gems