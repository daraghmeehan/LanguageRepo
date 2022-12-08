import pandas as pd  # to manage flashcard data - easy manipulation and exporting
import time  # to timestamp created csvs
from pathlib import Path  # for writing flashcards to "Flashcards" folder


class FlashcardCreator:
    def __init__(self, deck_name, fields) -> None:
        self.deck_name = deck_name
        self.flashcard_fields = fields
        self.create_flashcard_deck(fields)

    def create_flashcard_deck(self, fields):
        self.deck = pd.DataFrame(columns=fields)

    def number_of_flashcards(self):
        return len(self.deck.index)

    def add_flashcard(self, card_as_dict):

        assert list(card_as_dict.keys()) == self.flashcard_fields
        assert not all([field == "" for field in card_as_dict.values()])

        new_card = pd.DataFrame([card_as_dict])

        self.deck = pd.concat([self.deck, new_card], ignore_index=True)

    def export_deck(self):

        if self.number_of_flashcards() == 0:
            print(f"No cards created for deck {self.deck_name}.")
            return

        # to timestamp csvs
        timestamp = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())

        file_name = f'({self.deck_name}) {timestamp} - {self.number_of_flashcards()} card{"s" if self.number_of_flashcards() > 1 else ""}'
        file_path = Path(f"./Flashcards/{file_name}.csv")
        file_path.parent.mkdir(
            exist_ok=True
        )  # making the "Flashcard" directory if we don't have it

        self.deck.to_csv(
            file_path, columns=self.flashcard_fields, header=False, index=False
        )

        print(
            f"{self.deck_name} saved - {self.number_of_flashcards()} card{'s' if self.number_of_flashcards() > 1 else ''}"
        )
