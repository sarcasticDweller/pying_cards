from random import shuffle
from enum import IntEnum, auto
from typing import List, Dict, Tuple
from pying_cards.cards import Card, HighAceCard, Joker, Suit, Rank, RankType

    
class Collection(List[Card]):

    class AcePreference(IntEnum):
        LOW = auto()
        HIGH = auto()

    class AcesMode(IntEnum):
        LOW = auto()
        HIGH = auto()
        BOTH = auto()
    
    _ace_preference: AcePreference = AcePreference.LOW
    _aces_mode: AcesMode = AcesMode.BOTH

    def __init__(self, *cards: Card) -> None:
        super().__init__(cards)
    
    @classmethod
    def ace_settings(cls, mode: AcesMode | None = None, preference: AcePreference | None = None) -> None:
        cls._aces_mode = mode if mode else cls._aces_mode
        cls._ace_preference = preference if preference else cls._ace_preference
    
    @classmethod
    def standard_deck(cls, decks: int = 1, jokers: int = 0) -> "Collection":
        """
        Generates a standard 52-card deck with optional arguments for indicating how many decks to combine.
        
        :param decks: How many decks to be combined. Useful for games like Blackjack or flavors of Rummy.
        :type decks: int (optional)
        :param jokers: How many jokers to be added to the Collection
        :type jokers: int (optional)
        :return: Returns a Collection with at least 52 cards, in order.
        :rtype: Collection
        """
        cards = [Card(s, r) for _ in range(decks) for s in Suit for r in Rank]
        cards.extend([Joker() for _ in range(jokers)])
        return cls(*cards)

    @classmethod
    def get_card_data_as_lists(cls, cards: List[Card]) -> Tuple[List[Suit], List[RankType]]:
        suits: List[Suit] = []
        ranks: List[RankType] = []
        for card in cards:
            suits.append(card.suit)
            ranks.append(card.rank)
        return suits, ranks
    
    @classmethod
    def get_ranks_as_list_of_ints(cls, cards: List[Card]) -> List[int]:
        return [int(card.rank) for card in cards]

    @classmethod
    def is_straight(cls, cards: List[Card], length: int = 3) -> bool:
        if len(cards) != length:
            return False
        suits, ranks = cls.get_card_data_as_lists(cards)
        if len(set(suits)) != 1:
            return False
        ranks = sorted(set(ranks))
        if len(ranks) != length:
            return False
        return ranks[-1] - ranks[0] == length - 1
    
    @classmethod
    def is_pair(cls, cards: List[Card], length: int = 2) -> bool:
        if len(cards) != length:
            return False
        return len(set(cls.get_ranks_as_list_of_ints(cards))) == 1
    
    def shuffle(self) -> None:
        shuffle(self)

    def draw(self, count: int = 1) -> List[Card]:
        """Will draw `count` cards from the top of the Collection and return them as a list of `Card` objects. Will error if there are not enough cards in the Collection."""
        return [self.pop() for _ in range(count)]

    def draw_several_specific(self, card_indexes: List[int]) -> List[Card]:
        drawn_cards: List[Card] = []
        for i in card_indexes:
            drawn_cards.append(self[i - 1])
        self.cards = list(set(self).symmetric_difference(drawn_cards)) # removes drawn cards from Collection
        return drawn_cards
    
    def empty_Collection(self) -> List[Card]:
        """Returns the contents of the Collection. Designed to easily pipe contents from A to B."""
        old_cards = list(self)
        self.clear()
        return old_cards
    
    def contains_pairs(self, size_of_pair: int = 2) -> Tuple[bool, List[List[Card]]]:
        """Checks the Collection for pairs of a given length. Supports two-of-a-kind, three-of-a-kind, etc.

        :param size_of_pair: The length of the pairs to check for. Defaults to 2 to search for standard pairs. I'd like to make this cacheable, but that's a smarter person's job.
        :type size_of_pair: int, (optional)
        :return: A tuple containing:
                - A `bool` indicating whether any pairs of the specified length (`size_of_pair`) were found.
                - A `list` of lists, where each inner `list` contains `Card` objects representing a pair.
        :rtype: Tuple[bool, List[List[Card]]]
        """
        ranks_dict: Dict[int, List[Card]] = {}
        pairs: List[List[Card]] = []
        for card in self:
            ranks_dict.setdefault(card.rank, []).append(card)
        for rank in ranks_dict:
            # there may be multiple pairs in the rank
            cards = ranks_dict[rank]

            # worst case first:
            if len(cards) < size_of_pair:
                continue

            # happy case next:
            if len(cards) == size_of_pair: 
                pairs.append(cards)
                continue

            # oh good, there's at least one pair in there

            # neutral case: two+ pairs in the rank
            pairs.extend(cards[i:i + size_of_pair] for i in range(0, len(cards), size_of_pair))

        return len(pairs) > 0, pairs

    def contains_straights(self, size_of_straight: int = 3) -> tuple[bool, List[List[Card]]]:
        """Checks the Collection for straights of a given length. Supports three-card straights, four-card straights, etc. Supports high/low aces (read more below) and duplicates.

        **IMPORTANT**: If you want to customize how aces work, make sure you `Collection.set_aces_preference` and `Collection.set_aces_mode` before running `Collection.contains_straights`

        **IMPORTANT**: In its current state, this supports duplicate cards for every type of card... except aces.


        :param size_of_straight: The length of the straights to check for. Defaults to 3 to search for standard straights.
        :type size_of_straight: int (optional)
        :return: A tuple containing:
            - A boolean indicating whether any straights of the specified length were found.
            - A list of lists, where each inner list contains `Card` objects representing a straight
        :rtype: tuple[bool, List[List[Card]]]
        """
        print(f"Begin examining for straights of length {size_of_straight}")

        suits_dict: dict[Suit, List[Card]] = {}
        straights: List[List[Card]] = []

        # group by suit
        for card in self:
            suits_dict.setdefault(card.suit, []).append(card)
        print(f"Grouped all cards by suit:\n{suits_dict}")
        for suit in suits_dict:
            suited_cards = sorted(suits_dict[suit])
            if len(suited_cards) < size_of_straight:
                print(f"Chucking entire suit: {suit}")
                continue

            # happy case 
            if len(suited_cards) == size_of_straight and suited_cards[-1].rank - suited_cards[0].rank == size_of_straight - 1:
                print(f"Suit {suit} contains a perfect straight:\n{suited_cards}")
                straights.append(suited_cards)
                continue # to next suit

            # this high-ace implementation is not duplicate-friendly! sigh...
            first_card = suited_cards[0]
            ace_present = first_card.rank == Rank.ACE
            imaginary_ace: HighAceCard | None = None # it will only be used in scopes where i know it exists, but this is clearer?

            if ace_present:
                print(f"Ace detected in suit {suit}")
                imaginary_ace = HighAceCard(suit)
                suited_cards.append(imaginary_ace)
            
            # analyze each card directly, saving the need to convert them into ints and back again
            possible_straights: List[List[Card]] = [[]]
            for card in suited_cards:
                next: List[Card] = []
                for s in possible_straights:
                    if len(s) == 0 or int(card.rank) - 1 == int(s[-1].rank): 
                        s.append(card)
                    else:
                        next.append(card)
                possible_straights.extend([c] for c in next)
            found_straights = [s[:size_of_straight] for s in possible_straights if len(s) >= size_of_straight]
            if not found_straights:
                continue

            #low_ace_used, high_ace_used = found_straights[0][0].rank == int(Rank.ACE), found_straights[-1][-1].rank == HIGH_ACE
            low_ace_used, high_ace_used = isinstance(found_straights[0][0], HighAceCard), isinstance(found_straights[-1][-1], HighAceCard)
            if low_ace_used and high_ace_used:
                if Collection._ace_preference == Collection.AcePreference.LOW:
                    found_straights.pop(-1)
                if Collection._ace_preference == Collection.AcePreference.HIGH:
                    found_straights.pop(0)
            elif high_ace_used and not low_ace_used: # convert imaginary high-ace into a real ace
                found_straights[-1][-1] = first_card # which must be an ace, because an ace is present
            
            straights.extend(found_straights)

        return len(straights) > 0, straights
    

def find_unique_sequences(master_sequence: List[int], sequence_length: int) -> List[List[int]]:
    """Depricated"""
    working_sequences: List[List[int]] =[[]]
    for value in master_sequence:
        next: List[int] = []
        for sequence in working_sequences:
            if len(sequence) == 0 or value - 1 == sequence[-1]: 
                sequence.append(value)
            else:
                next.append(value)
        working_sequences.extend([v] for v in next)
    return [sequence[:sequence_length] for sequence in working_sequences if len(sequence) >= sequence_length]
