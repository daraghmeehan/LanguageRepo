import pandas as pd


class FlashcardCreator:
    def __init__(self, deck_name, fields) -> None:
        self.deck_name = deck_name
        self.create_flashcard_deck(deck_name, fields)

    def create_flashcard_deck(self, fields):
        self.deck = pd.DataFrame(columns=[fields])

    def number_of_flashcards(self):
        return len(self.deck.index)
