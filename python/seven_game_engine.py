#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python wrapper для C++ бібліотеки гри "Сім"

Цей модуль використовує C++ shared library через ctypes
для забезпечення інтеграції між Python та C++

Розробник: Сергій Щербаков
Email: sergiyscherbakov@ukr.net
Telegram: @s_help_2010
"""

import ctypes
import os
from typing import List, Tuple, Optional

# Знаходимо шлях до бібліотеки
LIB_PATH = os.path.join(os.path.dirname(__file__), '..', 'cpp', 'libseven_game.so')

# Якщо бібліотека не знайдена в стандартному місці, шукаємо в поточній директорії
if not os.path.exists(LIB_PATH):
    LIB_PATH = 'libseven_game.so'


class Card(ctypes.Structure):
    """Структура карти"""
    _fields_ = [
        ("rank", ctypes.c_int),  # 6-14
        ("suit", ctypes.c_int),  # 0-3
    ]

    def __repr__(self):
        rank_str = {
            11: "J", 12: "Q", 13: "K", 14: "A"
        }.get(self.rank, str(self.rank))

        suit_symbols = ["♥", "♦", "♣", "♠"]
        suit_str = suit_symbols[self.suit] if 0 <= self.suit < 4 else "?"

        return f"{rank_str}{suit_str}"


class GameState(ctypes.Structure):
    """Структура стану гри"""
    _fields_ = [
        ("current_player", ctypes.c_int),
        ("num_players", ctypes.c_int),
        ("player_cards_count", ctypes.c_int * 4),
        ("table_state", (Card * 9) * 4),
        ("table_card_count", ctypes.c_int * 4),
    ]


class SevenGameEngine:
    """Python wrapper для C++ движка гри"""

    SUIT_NAMES = ["Черви", "Буби", "Хрести", "Піки"]
    SUIT_SYMBOLS = ["♥", "♦", "♣", "♠"]

    def __init__(self, num_players: int = 2):
        """
        Ініціалізація гри

        Args:
            num_players: Кількість гравців (2-4)
        """
        # Завантажуємо бібліотеку
        self.lib = ctypes.CDLL(LIB_PATH)

        # Налаштовуємо типи функцій
        self._setup_function_types()

        # Створюємо гру
        self.game = self.lib.game_create(num_players)
        self.num_players = num_players

    def _setup_function_types(self):
        """Налаштування типів для функцій C API"""
        # game_create
        self.lib.game_create.argtypes = [ctypes.c_int]
        self.lib.game_create.restype = ctypes.c_void_p

        # game_deal_cards
        self.lib.game_deal_cards.argtypes = [ctypes.c_void_p]
        self.lib.game_deal_cards.restype = None

        # game_get_state
        self.lib.game_get_state.argtypes = [ctypes.c_void_p, ctypes.POINTER(GameState)]
        self.lib.game_get_state.restype = None

        # game_get_player_cards
        self.lib.game_get_player_cards.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                                     ctypes.POINTER(Card), ctypes.c_int]
        self.lib.game_get_player_cards.restype = ctypes.c_int

        # game_can_play_card
        self.lib.game_can_play_card.argtypes = [ctypes.c_void_p, ctypes.c_int, Card]
        self.lib.game_can_play_card.restype = ctypes.c_int

        # game_play_card
        self.lib.game_play_card.argtypes = [ctypes.c_void_p, ctypes.c_int, Card]
        self.lib.game_play_card.restype = ctypes.c_int

        # game_pass_turn
        self.lib.game_pass_turn.argtypes = [ctypes.c_void_p]
        self.lib.game_pass_turn.restype = None

        # game_check_winner
        self.lib.game_check_winner.argtypes = [ctypes.c_void_p]
        self.lib.game_check_winner.restype = ctypes.c_int

        # game_get_current_player
        self.lib.game_get_current_player.argtypes = [ctypes.c_void_p]
        self.lib.game_get_current_player.restype = ctypes.c_int

        # game_computer_move
        self.lib.game_computer_move.argtypes = [ctypes.c_void_p, ctypes.POINTER(Card)]
        self.lib.game_computer_move.restype = ctypes.c_int

        # game_destroy
        self.lib.game_destroy.argtypes = [ctypes.c_void_p]
        self.lib.game_destroy.restype = None

    def deal_cards(self):
        """Роздати карти"""
        self.lib.game_deal_cards(self.game)

    def get_state(self) -> GameState:
        """Отримати стан гри"""
        state = GameState()
        self.lib.game_get_state(self.game, ctypes.byref(state))
        return state

    def get_player_cards(self, player_id: int) -> List[Card]:
        """Отримати карти гравця"""
        cards = (Card * 20)()  # Максимум 20 карт
        count = self.lib.game_get_player_cards(self.game, player_id, cards, 20)
        return [cards[i] for i in range(count)]

    def can_play_card(self, player_id: int, card: Card) -> bool:
        """Перевірити чи можна зіграти карту"""
        return bool(self.lib.game_can_play_card(self.game, player_id, card))

    def play_card(self, player_id: int, card: Card) -> bool:
        """Зіграти карту"""
        return bool(self.lib.game_play_card(self.game, player_id, card))

    def pass_turn(self):
        """Пропустити хід"""
        self.lib.game_pass_turn(self.game)

    def check_winner(self) -> int:
        """Перевірити переможця (-1 якщо гра продовжується)"""
        return self.lib.game_check_winner(self.game)

    def get_current_player(self) -> int:
        """Отримати поточного гравця"""
        return self.lib.game_get_current_player(self.game)

    def computer_move(self) -> Optional[Card]:
        """Хід комп'ютера"""
        card = Card()
        if self.lib.game_computer_move(self.game, ctypes.byref(card)):
            return card
        return None

    def get_valid_moves(self, player_id: int) -> List[Card]:
        """Отримати список можливих ходів для гравця"""
        cards = self.get_player_cards(player_id)
        return [card for card in cards if self.can_play_card(player_id, card)]

    def __del__(self):
        """Очищення ресурсів"""
        if hasattr(self, 'game') and self.game:
            self.lib.game_destroy(self.game)


# Тестування модуля
if __name__ == "__main__":
    print("Тест Python wrapper для C++ бібліотеки")
    print("=" * 50)

    engine = SevenGameEngine(2)
    engine.deal_cards()

    state = engine.get_state()
    print(f"Гравців: {state.num_players}")
    print(f"Поточний гравець: {state.current_player}")

    for i in range(state.num_players):
        cards = engine.get_player_cards(i)
        print(f"\nГравець {i + 1} має {len(cards)} карт:")
        print(" ".join(str(card) for card in cards))

    print("\n✓ Тест успішний! Python використовує C++ бібліотеку!")
