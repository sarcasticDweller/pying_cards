# I beg of you PLEASE test me! At some time that isn't 1 in the morning! 2 in the morning doesn't count!

from pying_cards.decks import Collection
from pying_cards.cards import Suit, Rank, RankType, Card
from enum import IntEnum
from typing import Callable, Any, List, Tuple, Dict
from functools import lru_cache # tell me: is this even worth it for the kind of work we're doing here?

POKER_HAND_SIZE = 5 # no matter the game, you build a hand of five cards. even if three of those were randomly pulled from the river.

class HandValue(IntEnum):
    """Golf rules"""
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

card_data: Callable[[List[Card]], Tuple[List[Suit], List[RankType]]] = lambda cards: Collection.get_card_data_as_lists(cards)

def _validate_hand_size(func: Callable[[Any], Any]):
    def wrapper(cards: List[Any]):
        if len(cards) != POKER_HAND_SIZE:
            raise Exception("Invalid amount of cards used for a poker hand")
        return func(cards)
    return wrapper

def _validate_group_of_pairs(cards: Collection, *pairs_sizes: int) -> bool:
    """Takes pair-sizes as arguments and confirms there is one of each present in a card collection. Forgive me, future self, for I wrote this at 1am on New Years Day."""
    groups = _get_paired_up_cards(*cards)

    # decide how many groups we expect to see and enforce it
    expected_groups: int
    card_count = sum(pairs_sizes)
    expected_pairs = len(pairs_sizes)
    """
    Theory: the below if-elif-else tree could be rewritten as thus:
    
    if card_count > POKER_HAND_SIZE:
        raise ValueError(f"Expected to find more cards than can be in a poker hand (5 cards). Pair sizes passed: {pairs_sizes}")
    expected_groups = expected_pairs + POKER_HAND_SIZE - card_count
    
    This is on the vague principle that if card_count == POKER_HAND_SIZE, then expected_pairs and card_count will cancel out.

    However, it is 1:21 in the morning as of writing, and I certainly cannot do math right now. Goodnight, and hopefully 2026 is going well or a fond memory by now.
    """
    if card_count == POKER_HAND_SIZE:
        expected_groups = expected_pairs
    elif card_count < POKER_HAND_SIZE:
        expected_groups = expected_pairs + POKER_HAND_SIZE - card_count # one per unaccounted card!
    else: # card_count > POKER_HAND_SIZE
        raise ValueError(f"Expected to find more cards than can be in a poker hand (5 cards). Pair sizes passed: {pairs_sizes}")
    if len(groups) != expected_groups:
        return False
    
    # now really make sure there's no wily wabbits hiding in the groups!
    for k in groups:
        if len(groups[k]) not in pairs_sizes:
            return False
    return True

@lru_cache(maxsize=None)
def _get_paired_up_cards(*cards: Card) -> Dict[int, List[Card]]:
    ranks_dict: Dict[int, List[Card]] = {}
    for card in cards:
        ranks_dict.setdefault(card.rank, []).append(card)
    return ranks_dict

@lru_cache(maxsize=None)
def _is_sequential(*ranks: RankType) -> bool:
    # for any list of sequential integers, the difference between the last and first values is always equal to one less than the length of the sequence. in this case, that length is POKER_HAND_SIZE
    # unfortunately, we're working with RankType, which from our POV is just an obfuscation of ints...
    return len(set(ranks)) == POKER_HAND_SIZE and ranks[-1] - ranks[0] == POKER_HAND_SIZE - 1

@_validate_hand_size
def is_royal_flush(cards: Collection) -> bool:
    suits, ranks = card_data(cards)
    if len(suits) != 1:
        return False
    return Rank.ACE in ranks and Rank.KING in ranks and Rank.QUEEN in ranks and Rank.JACK in ranks and Rank.TEN in ranks

@_validate_hand_size
def is_straight_flush(cards: Collection) -> bool:
    suits, ranks = card_data(cards)
    if len(suits) != 1:
        return False
    ranks.sort()
    return _is_sequential(*ranks)

@_validate_hand_size
def is_four_of_a_kind(cards: Collection) -> bool:
    return _validate_group_of_pairs(cards, 4)

@_validate_hand_size
def is_full_house(cards: Collection) -> bool: # 3 pair and 2 pair
    return _validate_group_of_pairs(cards, 3, 2)

@_validate_hand_size
def is_flush(cards: Collection) -> bool:
    suits, _ = card_data(cards)
    return len(suits) == 1

@_validate_hand_size
def is_straight(cards: Collection) -> bool:
    _, ranks = card_data(cards)
    return _is_sequential(*ranks)

@_validate_hand_size
def is_three_of_a_kind(cards: Collection) -> bool:
    return _validate_group_of_pairs(cards, 3)

@_validate_hand_size
def is_two_pair(cards: Collection) -> bool:
    return _validate_group_of_pairs(cards, 2, 2)

@_validate_hand_size
def is_pair(cards: Collection) -> bool:
    return _validate_group_of_pairs(cards, 2)

@_validate_hand_size
def get_high_card(cards: Collection) -> Card: # pyright: ignore[reportReturnType]
    _, ranks = card_data(cards)
    ranks.sort()
    for card in cards:
        if card.rank == ranks[-1]:
            return card
