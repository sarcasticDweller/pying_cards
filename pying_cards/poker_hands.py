from pying_cards.decks import Collection
from pying_cards.cards import Suit, Rank, RankType, Card
from enum import IntEnum
from typing import Callable, Any, List, Tuple, Dict
from functools import lru_cache # tell me: is this even worth it for the kind of work we're doing here?

"""
Hello future me,

I got a third of the way through an idea and then realized it was almost bedtime and I spent all afternoon doing math... so I put a pin in it. 

You should see a bunch of red squigglies. Start by reading the definition of PokerHand, and then proceed from there.

Goodnight!
"""

POKER_HAND_SIZE = 5 # no matter the game, you build a hand of five cards. even if three of those were randomly pulled from the river.
def _validate_hand_size(func: Callable[[Any], Any]): # pyright: ignore[reportUnusedFunction] #validation decorator to enforce POKER_HAND_SIZE
    def wrapper(cards: List[Any]):
        if len(cards) != POKER_HAND_SIZE:
            raise Exception("Invalid amount of cards used for a poker hand")
        return func(cards)
    return wrapper

class HandValue(IntEnum):
    """Base point values for score calculations. Current values are PLACEHOLDERS."""
    ROYAL_FLUSH = 1
    STRAIGHT_FLUSH = 2
    FOUR_OF_A_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 7
    THREE_OF_A_KIND = 7
    TWO_PAIR = 8
    PAIR = 9
    HIGH_CARD = 10
    NO_POINTS = 0

class PokerHand(Collection): # remember that a Collection is just a fancier list
    def __init__(self, *cards: Card):
        super().__init__(*cards)
        self.points_cards: List[Card] = self._validate(*cards) # the cards that actually make up the meat of the card
        assert(self.points_cards)
        self.other_cards: List[Card] # everything else in the hand, useful for high-card scoring
        self.points: HandValue
        #self.points will require further calculation as high cards act as tie-breakers

    def __repr__(self):
        return f"{self.__class__.__name__} containing {list(self)}"
    
    @classmethod
    def _validate(cls, *cards: Card) -> List[Card]:
        '''Returns the list of cards that make the hand "valid"''' # hey, i know im breaking my docstring formatting. but i wanted double-quotes darnit! 
        ... #id rather use pass, but this makes pyright happy

    @property
    def _high_card(self) -> Card:
        return sorted(self)[-1]

ROYAL_FLUSH_RANKS = [Rank.ACE, Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING] # im used elsewhere, dont change my scope!
THE_ROYAL_STRAIGHT: Callable[..., bool] = lambda *ranks: Rank.ACE in ranks and Rank.TEN in ranks and Rank.JACK in ranks and Rank.QUEEN in ranks and Rank.KING in ranks  
class RoyalFlush(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)

    @classmethod
    def _validate(cls, *cards: Card) -> List[Card]:
        hand_cards: List[Card] = []
        suits, ranks = _card_data(Collection(*cards))
        ranks.sort()
        if THE_ROYAL_STRAIGHT(ranks) and _is_flush(*suits):
            hand_cards = list(cards)
        return hand_cards 

class StraightFlush(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)

    @classmethod
    def _validate(cls, *cards: Card) -> List[Card]:
        hand_cards: List[Card] = []
        suits, ranks = _card_data(Collection(*cards))
        ranks.sort()
        if _is_sequential(*ranks) and _is_flush(*suits):
            hand_cards = list(*cards)
        return hand_cards


class FourOfAKind(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)

    @classmethod
    def _validate(cls, *cards: Card) -> List[Card]:
        hand_cards: List[Card] = []
        if _is_group_of_pairs(Collection(*cards), 4, 1):
            ...
        return hand_cards
    
class FullHouse(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)
    
    @classmethod
    def _validate(cls, *cards: Card) -> bool: # 3 pair and 2 pair
        return _is_group_of_pairs(Collection(*cards), 3, 2)

class Flush(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)
    
    @classmethod
    def _validate(cls, *cards: Card) -> bool:
        suits, _ = _card_data(Collection(*cards))
        return _is_flush(*suits)

class Straight(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)
    
    @classmethod
    def _validate(cls, *cards: Card) -> bool:
        _, ranks = _card_data(Collection(*cards))
        return _is_sequential(*ranks)

class ThreeOfAKind(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)

    @classmethod
    def _validate(cls, *cards: Card) -> bool:
        return _is_group_of_pairs(Collection(*cards), 3)

class TwoPair(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)

    @classmethod
    def _validate(cls, *cards: Card) -> bool:
        return _is_group_of_pairs(Collection(*cards), 2, 2)

class Pair(PokerHand):
    def __init__(self, *cards: Card):
        super().__init__(*cards)
    
    @classmethod
    def _validate(cls, *cards: Card) -> bool:
        return _is_group_of_pairs(Collection(*cards), 2)

class HighCard(PokerHand):
    ... # not sure if i even want to implement this class
    # yes, i do want to implement it! just not right now

_card_data: Callable[[List[Card]], Tuple[List[Suit], List[RankType]]] = lambda cards: Collection.get_card_data_as_lists(cards)

# PokerHand validation functions
def get_high_card(cards: Collection) -> Card: # pyright: ignore[reportReturnType]
    _, ranks = _card_data(cards)
    ranks.sort()
    for card in cards:
        if card.rank == ranks[-1]:
            return card

@lru_cache
def _sort_by_attribute(attribute_name: str, *cards: Card) -> Dict[Any, List[Card]]:
    out: Dict[Any, List[Card]] = {}
    for c in cards:
        out.setdefault(getattr(c, attribute_name), []).append(c)
    return out

@lru_cache
def _is_sequential(*ranks: RankType) -> bool:
    # for any list of sequential integers, the difference between the last and first values is always equal to one less than the length of the sequence. in this case, that length is POKER_HAND_SIZE
    # unfortunately, we're working with RankType, which from our POV is just an obfuscation of ints...
    return len(set(ranks)) == POKER_HAND_SIZE and ranks[-1] - ranks[0] == POKER_HAND_SIZE - 1

def _only_numbers_in_sequence(sequence: List[int], *numbers: int) -> bool:
    for i in numbers:
        if i in sequence:
            sequence.pop(i)
        else:
            return False
    return len(sequence) == 0


def _is_group_of_pairs(cards: Collection, *pairs_sizes: int) -> bool:
    """Takes pair-sizes as arguments and confirms there is one of each present in a card collection. Forgive me, future self, for I wrote this at 1am on New Years Day."""

    # decide how many groups we expect to see and enforce it
    card_count = sum(pairs_sizes)
    expected_pairs = len(pairs_sizes)

    if sum(pairs_sizes) > POKER_HAND_SIZE:
        raise ValueError(f"Expected to find more cards than can be in a poker hand (5 cards). Pair sizes passed: {pairs_sizes}")
    expected_groups = expected_pairs + POKER_HAND_SIZE - card_count

    groups = _sort_by_attribute("rank", *cards)
    if len(groups) != expected_groups:
        return False
    
    # now really make sure there's no wily wabbits hiding in the groups!
    for k in groups:
        if len(groups[k]) not in pairs_sizes:
            return False
    return True

def _is_flush(*suits: Suit):
    return len(set(suits)) == 1

# okay, this is great and all, but what would be REALLY cool is a function that takes a collection of cards and returns the highest-ranked poker hand in that collection

@lru_cache
def analyze_hand_uisng_brain(*cards: Card) -> PokerHand | None:
    """Returns the poker hand and what cards make it up. Assumes cards are pre-sorted"""
    hand_size = len(cards)
    assert(hand_size == POKER_HAND_SIZE) # just for simplicity while we dev

    print(f"analzying {list(cards)}")

    hand: PokerHand | None = None

    pairs = _sort_by_attribute("rank", *cards)
    suits, ranks = _card_data(list(cards))
    ranks.sort()
    flush = _is_flush(*suits) # this is used all over the place. its a really simple func but it keeps the code clean
    straight = _is_sequential(*ranks)
    print(f"Is flush: {flush}")
    print(f"Is straight: {straight}")

    if flush and THE_ROYAL_STRAIGHT(*ranks):
        print("hand looks like a royal flush")
        hand = RoyalFlush(*cards)
    elif flush and straight:
        print("hand looks like a straight flush")
        hand = StraightFlush(*cards)
    elif flush:
        print("hand looks like a flush")
        hand = Flush(*cards) 
    elif straight:
        print("hand looks like a straight")
        hand = Straight(*cards)
    else:
        # analyze your pairs
        pair_sizes = sorted([len(pairs[p]) for p in pairs])
        expected_pairs: Dict[Any, List[int]] = {
            FourOfAKind: [4, 1],
            FullHouse: [3, 2],
            ThreeOfAKind: [3, 1, 1],
            TwoPair: [2, 2, 1],
            Pair: [2, 1, 1, 1]

        }
        for e in expected_pairs:
            if _only_numbers_in_sequence(pair_sizes, *expected_pairs[e]): # unfortunately, this is a triple-nested loop
                print(f"hand looks like a {e}")
                hand = e(*cards)
                break # there's no overlap between different kinds of pairs, so we can exit here
    if not hand:
        ... 
    print(f"output: {hand}")

    return hand

def analyze_hand_using_brawn(*cards: Card) -> PokerHand:
    ...
    # go through all PokerHand sublcasses in order of hand value until you find one that validates