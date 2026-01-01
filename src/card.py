from enum import Enum, IntEnum
class Suit(Enum):
    SPADE = "spade"
    HEART = "heart"
    CLUB = "club"
    DIAMOND = "diamond"

class Rank(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class _SpecialRank(IntEnum):
    ACEHIGH = 14

RankType = Rank | _SpecialRank # its hacky, but its the only way i could think to get high-ace support. and i might have to change it later!


class Card:
    """
    Contains a suit and rank enum value that can be used for playing-card games. Supports high and low aces.
    
    :var suit: simple enumerated suit data. Under the hood, it's a `str` (for now).
    :vartype suit: Suit
    :var rank: simple enumerated rank data. Under the hood, it's an `int`.
    :vartype rank: Rank
    """
    def __init__(self, suit: Suit, rank: RankType) -> None:
        self.suit = suit
        self.rank = rank
    
    def __repr__(self) -> str:
        return f"Card {self.rank.name} of {self.suit.name}"
    
    def __lt__(self, other: "Card") -> bool:
        #return self.rank < other.rank
        return True if self.rank == Rank.KING and other.rank == Rank.ACE else self.rank < other.rank
    
    def __gt__(self, other: "Card") -> bool:
        #return self.rank > other.rank
        return True if self.rank == Rank.ACE and other.rank == Rank.KING else self.rank > other.rank

class HighAceCard(Card):
    def __init__(self, suit: Suit):
        super().__init__(suit, _SpecialRank.ACEHIGH)