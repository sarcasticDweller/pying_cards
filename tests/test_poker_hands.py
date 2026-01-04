from unittest import TestCase
from pying_cards.cards import Card, Suit, Rank
from pying_cards.poker_hands import *

cards, hand = 0, 1
class TestAnalyzeHand(TestCase):
    def setUp(self):
        self.validRF = (
            (
                Card(Suit.HEART, Rank.ACE),
                Card(Suit.HEART, Rank.TEN),
                Card(Suit.HEART, Rank.JACK),
                Card(Suit.HEART, Rank.QUEEN),
                Card(Suit.HEART, Rank.KING),
            ),
            RoyalFlush
        )
        self.validSF = (
            (
                Card(Suit.HEART, Rank.NINE),
                Card(Suit.HEART, Rank.TEN),
                Card(Suit.HEART, Rank.JACK),
                Card(Suit.HEART, Rank.QUEEN),
                Card(Suit.HEART, Rank.KING),
            ),
            StraightFlush
        )
        # i would use variables to make it clearer what the index numbers mean later on, but it gives me weird squigglies when i try. this is test code, why bother?
    def test_validRF_thusTrue(self):
        self.assertIsInstance(
            analyze_hand(*self.validRF[0]),
            self.validRF[1]
        )
    def test_validsF_thusTrue(self):
        hand = analyze_hand(*self.validSF[0])
        self.assertIsInstance(hand, self.validSF[1])

