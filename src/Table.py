from src.Deck import Deck
from src.Card import CardColor, Zone

class Table:
    def __init__(self, deck:Deck):
        self.zones = [Zone(CardColor.NONE)]
        self.certifications = [Zone(CardColor.NONE)] # TODO: cambiare in certificazione

        card_zone = None
        for _ in deck.get_cards():
            card = deck.draw_cards(self, 1)[0]
            if not card.is_zone():
                self.certifications.append(card)
                continue
            else:
                card_zone = card
                break
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        if card_zone is None:
            card_zone = Zone(CardColor.NONE)
        self.zones.append(card_zone)
    
    def get_zones(self):
        return self.zones
    
    def set_zones(self, zones):
        self.zones = zones
    
    def get_certifications(self):
        return self.certifications
    
    def set_certifications(self, certifications):
        self.certifications = certifications

    def get_top_zone(self):
        return self.get_zones()[-1]

    def get_top_certification(self):
        return self.get_certifications()[-1]
    
    def reset_certifications(self):
        self.set_certifications([])

    def reset_zones(self):
        self.set_zones([])

    def has_top_zone(self, zone_card):
        if zone_card == self.get_top_zone():
            return True
        return False
    
    def play_zone(self, zone_card):
        self.get_zones().append(zone_card)

    def play_certification(self, certification_card):
        self.get_certifications().append(certification_card)

    def remake(self, deck:Deck):
        cards = []
        cards.extend(deck.get_cards())
        deck.set_cards([])
        
        zone = self.get_top_zone()
        top_zone = [Zone(CardColor.NONE), zone]
        
        zones = self.get_zones()
        zone_temp = zones[:-1] if len(zones) > 1 else zones
        for card in zone_temp:
            if card != Zone(CardColor.NONE):
                cards.append(card) 
            
        for card in self.get_certifications():
            if card != Zone(CardColor.NONE):
                cards.append(card) 

        self.reset_zones()
        self.set_zones(top_zone)
        
        self.reset_certifications()
        self.set_certifications([Zone(CardColor.NONE)])

        return cards

    def __str__(self):
        return str(self.get_top_zone()) + ' ' + str(self.get_top_certification())