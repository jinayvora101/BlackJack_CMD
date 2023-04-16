from random import shuffle

class deck:
    
    def __init__(self):
        self.deck = []
        for i in ["\u2661", "\u2664", "\u2662", "\u2667"]:
            for j in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                self.deck.append(j+i)
        shuffle(self.deck)
        self.write_deck()
        # self.deck = 
    
    def deal_card(self):
        return self.deck.pop()

    def burn_card(self):
        self.deck.pop()

    def write_deck(self):
        with open("deck.txt", "a", encoding="utf-16") as f:
            f.write("[\"" + "\" , \"".join(self.deck) + "\"]\n")


class player:
    
    def __init__(self, name):
        self.hand = []
        self.sum = 0
        self.bust = False
        self.name = name
        self.hit = True
        self.ace = 0
        
    def change_hit_status(self, other):
        if self.name == "Dealer":
            if self.sum >= 17 and self.ace == False and self.sum > other.sum: self.hit = False
            if self.sum >= other.sum and other.hit == False: self.hit = False
            if self.sum == 21: self.hit = False
        else:
            self.hit = False if input("enter h for hit and s for stand: ") == "s" else True
    
    def collect_card(self, card):
        self.hand.append(card)
        if card[0] == "A": self.ace = self.ace + 1
        self.calculate_hand()
        self.check_bust()
        
    def calculate_hand(self):
        self.sum = 0
        for i in self.hand:
            i = i[: -1]
            try: self.sum = self.sum + int(i)
            except:
                if i in ["J", "Q", "K"]: self.sum = self.sum + 10
                elif i == "A": self.sum = self.sum + 11
        
        count = self.ace
        while count > 0 and self.sum > 21:
            count = count - 1
            self.sum = self.sum - 10
            
    def check_bust(self):
        if self.sum > 21: self.bust = True
        
    def display_hand(self):
        print(self.name, "'s hand: ", "  ".join(self.hand), "\tvalue: ", self.sum, sep="")


deal_deck = deck()
player1 = player("JinayV")
dealer = player("Dealer")

deal_deck.burn_card()
player1.collect_card(deal_deck.deal_card())
dealer.collect_card(deal_deck.deal_card())
player1.collect_card(deal_deck.deal_card())

print("\n---Round---")
player1.display_hand()
dealer.display_hand()
print("-----------")

player1.change_hit_status(dealer)
while True:
    if dealer.hit:
        dealer.change_hit_status(player1)

    if player1.hit:
        player1.collect_card(deal_deck.deal_card())
        player1.display_hand()
        if player1.bust: break
    if dealer.hit:
        dealer.collect_card(deal_deck.deal_card())
        dealer.display_hand()
        if dealer.bust: break
    print("-----------")
    
    if player1.hit:
        player1.change_hit_status(dealer)
        
    if not(player1.hit or dealer.hit): break

print("\n---Results---")
player1.display_hand()
dealer.display_hand()
if player1.bust: print("Dealer wins by busting ", player1.name)
elif dealer.bust: print(player1.name, "wins by busting the dealer")
elif player1.sum > dealer.sum: print(player1.name, "wins by higher hand")
elif player1.sum < dealer.sum: print("Dealer wins by higher hand")
elif player1.sum == dealer.sum: print("Tie due to equal hand")