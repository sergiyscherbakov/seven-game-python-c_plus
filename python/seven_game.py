#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Гра "Сім" - карткова гра для 2-4 гравців

Розробник: Сергій Щербаков
Email: sergiyscherbakov@ukr.net
Telegram: @s_help_2010
"""

import random
from typing import List, Dict, Tuple, Optional
from enum import Enum


class Suit(Enum):
    """Масті карт"""
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3


SUIT_SYMBOLS = {
    Suit.HEARTS: "♥",
    Suit.DIAMONDS: "♦",
    Suit.CLUBS: "♣",
    Suit.SPADES: "♠"
}

SUIT_NAMES = {
    Suit.HEARTS: "Черви",
    Suit.DIAMONDS: "Буби",
    Suit.CLUBS: "Хрести",
    Suit.SPADES: "Піки"
}


class Card:
    """Клас для представлення карти"""

    def __init__(self, rank: int, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        """Текстове представлення карти"""
        rank_str = {
            11: "J",
            12: "Q",
            13: "K",
            14: "A"
        }.get(self.rank, str(self.rank))

        return f"{rank_str}{SUIT_SYMBOLS[self.suit]}"

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other):
        """Порівняння для сортування"""
        if self.suit.value != other.suit.value:
            return self.suit.value < other.suit.value
        return self.rank < other.rank


class Deck:
    """Клас колоди карт"""

    def __init__(self):
        """Створюємо колоду з 36 карт (від 6 до туза)"""
        self.cards = []
        for suit in Suit:
            for rank in range(6, 15):  # 6-10, J(11), Q(12), K(13), A(14)
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        """Перемішуємо колоду"""
        random.shuffle(self.cards)

    def deal_cards(self, count: int) -> List[Card]:
        """Роздаємо карти"""
        dealt = []
        for _ in range(min(count, len(self.cards))):
            dealt.append(self.cards.pop())
        return dealt

    def is_empty(self) -> bool:
        """Перевірка чи колода порожня"""
        return len(self.cards) == 0


class Player:
    """Базовий клас гравця"""

    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []

    def add_cards(self, cards: List[Card]):
        """Додаємо карти до руки"""
        self.hand.extend(cards)
        self.sort_hand()

    def sort_hand(self):
        """Сортуємо карти в руці"""
        self.hand.sort()

    def show_hand(self):
        """Показуємо карти гравця"""
        print(f"\n{self.name} має {len(self.hand)} карт(и):")
        for i, card in enumerate(self.hand, 1):
            print(f"{i}. {card}  ", end="")
            if i % 9 == 0:
                print()
        print()

    def has_cards(self) -> bool:
        """Перевірка чи є карти у гравця"""
        return len(self.hand) > 0

    def get_card_count(self) -> int:
        """Кількість карт у гравця"""
        return len(self.hand)

    def get_valid_moves(self, table: Dict[Suit, Tuple[int, int]]) -> List[int]:
        """Отримуємо список можливих ходів"""
        valid = []

        for i, card in enumerate(self.hand):
            # Перевірка чи можна зіграти сімку
            if card.rank == 7:
                if card.suit not in table:
                    valid.append(i)
                    continue

            # Перевірка чи можна зіграти іншу карту
            if card.suit in table:
                min_rank, max_rank = table[card.suit]

                if card.rank == min_rank - 1 or card.rank == max_rank + 1:
                    valid.append(i)

        return valid

    def select_card(self, table: Dict[Suit, Tuple[int, int]], can_play_seven: bool) -> int:
        """Вибір карти для ходу (має бути перевизначений у підкласах)"""
        raise NotImplementedError

    def play_card(self, index: int) -> Optional[Card]:
        """Грає карту з руки"""
        if 0 <= index < len(self.hand):
            return self.hand.pop(index)
        return None


class HumanPlayer(Player):
    """Людський гравець"""

    def select_card(self, table: Dict[Suit, Tuple[int, int]], can_play_seven: bool) -> int:
        """Вибір карти людиною"""
        self.show_hand()

        valid_moves = self.get_valid_moves(table)

        if not valid_moves:
            print("У вас немає можливих ходів. Пропускаєте хід.")
            input("Натисніть Enter для продовження...")
            return -1

        print(f"Можливі ходи: {[i + 1 for i in valid_moves]}")

        while True:
            try:
                choice = input("Виберіть карту (номер) або 0 для пропуску ходу: ")
                choice = int(choice)

                if choice == 0:
                    return -1

                choice -= 1  # Перетворюємо в індекс масиву

                if choice in valid_moves:
                    return choice

                print("Неправильний вибір! Спробуйте ще раз.")
            except (ValueError, KeyboardInterrupt):
                print("Неправильний ввід! Введіть число.")


class ComputerPlayer(Player):
    """Комп'ютерний гравець"""

    def select_card(self, table: Dict[Suit, Tuple[int, int]], can_play_seven: bool) -> int:
        """Вибір карти комп'ютером"""
        valid_moves = self.get_valid_moves(table)

        if not valid_moves:
            print(f"{self.name} пропускає хід.")
            return -1

        # Проста стратегія: вибираємо випадковий хід
        selected_idx = random.choice(valid_moves)
        print(f"{self.name} грає карту: {self.hand[selected_idx]}")

        return selected_idx


class SevenGame:
    """Головний клас гри"""

    def __init__(self):
        self.players: List[Player] = []
        self.table: Dict[Suit, Tuple[int, int]] = {}
        self.current_player = 0
        self.consecutive_passes: List[int] = []

    def add_player(self, player: Player):
        """Додаємо гравця до гри"""
        self.players.append(player)
        self.consecutive_passes.append(0)

    def deal_cards(self):
        """Роздаємо карти"""
        deck = Deck()
        deck.shuffle()

        cards_per_player = 36 // len(self.players)

        for player in self.players:
            player.add_cards(deck.deal_cards(cards_per_player))

    def show_table(self):
        """Показуємо стан столу"""
        print("\n" + "=" * 50)
        print("СТІЛ".center(50))
        print("=" * 50)

        if not self.table:
            print("Стіл порожній. Грайте сімку для початку!".center(50))
        else:
            for suit in Suit:
                if suit in self.table:
                    min_rank, max_rank = self.table[suit]
                    cards = []
                    for rank in range(min_rank, max_rank + 1):
                        cards.append(str(Card(rank, suit)))

                    print(f"{SUIT_NAMES[suit]}: {' '.join(cards)}")

        print("=" * 50 + "\n")

    def make_move(self) -> bool:
        """Виконуємо хід поточного гравця"""
        player = self.players[self.current_player]

        print(f"\n>>> Хід гравця: {player.name} ({player.get_card_count()} карт) <<<")

        self.show_table()

        can_play_seven = len(self.table) < 4

        selected_card = player.select_card(self.table, can_play_seven)

        if selected_card == -1:
            self.consecutive_passes[self.current_player] += 1
            self.current_player = (self.current_player + 1) % len(self.players)
            return True

        card = player.play_card(selected_card)

        if card:
            # Оновлюємо стіл
            if card.suit not in self.table:
                # Нова масть на столі (має бути сімка)
                self.table[card.suit] = (card.rank, card.rank)
            else:
                # Розширюємо діапазон для існуючої масті
                min_rank, max_rank = self.table[card.suit]
                new_min = min(min_rank, card.rank)
                new_max = max(max_rank, card.rank)
                self.table[card.suit] = (new_min, new_max)

            self.consecutive_passes[self.current_player] = 0

            print(f"{player.name} зіграв карту: {card}")

            # Перевірка на перемогу
            if not player.has_cards():
                print(f"\n🎉 {player.name} ВИГРАВ! 🎉")
                return False

        self.current_player = (self.current_player + 1) % len(self.players)
        return True

    def all_players_passed(self) -> bool:
        """Перевірка чи всі гравці пропустили хід"""
        return all(passes > 0 for passes in self.consecutive_passes)

    def play(self):
        """Головний ігровий цикл"""
        print("\n🎴 === ГРА 'СІМ' РОЗПОЧАЛАСЯ! === 🎴\n")

        self.deal_cards()

        while True:
            if not self.make_move():
                break

            if self.all_players_passed():
                print("\nВсі гравці пропустили хід. Гра закінчена!")

                # Знаходимо гравця з найменшою кількістю карт
                min_cards = min(p.get_card_count() for p in self.players)
                winners = [p for p in self.players if p.get_card_count() == min_cards]

                if len(winners) == 1:
                    print(f"\n🏆 Переможець: {winners[0].name} (залишилось {min_cards} карт) 🏆")
                else:
                    print(f"\n🏆 Нічия між: {', '.join(w.name for w in winners)} 🏆")
                break

        print("\nДякуємо за гру!")


def print_header():
    """Виводимо заголовок гри"""
    print("╔" + "═" * 48 + "╗")
    print("║" + "🎴 ГРА 'СІМ' 🎴".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("║" + "Розробник: Сергій Щербаков".center(48) + "║")
    print("║" + "Email: sergiyscherbakov@ukr.net".center(48) + "║")
    print("║" + "Telegram: @s_help_2010".center(48) + "║")
    print("╚" + "═" * 48 + "╝\n")


def main():
    """Головна функція програми"""
    print_header()

    print("Оберіть режим гри:")
    print("1. Гра проти комп'ютера")
    print("2. Гра проти іншого гравця")

    try:
        mode = int(input("Ваш вибір: "))
    except ValueError:
        print("Неправильний вибір!")
        return

    game = SevenGame()

    if mode == 1:
        player_name = input("\nВведіть ваше ім'я: ")
        game.add_player(HumanPlayer(player_name))
        game.add_player(ComputerPlayer("Комп'ютер"))
    elif mode == 2:
        player1_name = input("\nВведіть ім'я першого гравця: ")
        player2_name = input("Введіть ім'я другого гравця: ")

        game.add_player(HumanPlayer(player1_name))
        game.add_player(HumanPlayer(player2_name))
    else:
        print("Неправильний вибір!")
        return

    game.play()


if __name__ == "__main__":
    main()
