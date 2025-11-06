#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI для гри "Сім" з використанням C++ бібліотеки через Python wrapper

Розробник: Сергій Щербаков
Email: sergiyscherbakov@ukr.net
Telegram: @s_help_2010
"""

import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys

# Додаємо шлях до модуля
sys.path.insert(0, os.path.dirname(__file__))

from seven_game_engine import SevenGameEngine, Card


class SevenGameGUI:
    """GUI для гри Сім"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎴 Гра 'Сім' - Python + C++")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        # Налаштування стилю
        self.setup_styles()

        # Гра
        self.engine = None
        self.num_players = 2
        self.is_ai_game = True
        self.player_names = ["Гравець 1", "Комп'ютер"]

        # Показуємо меню вибору
        self.show_menu()

    def setup_styles(self):
        """Налаштування стилів"""
        style = ttk.Style()
        style.theme_use('clam')

        # Кольори
        self.bg_color = "#2c3e50"
        self.card_bg = "#ecf0f1"
        self.table_bg = "#27ae60"
        self.player_bg = "#34495e"

        self.root.configure(bg=self.bg_color)

    def show_menu(self):
        """Показати меню вибору режиму гри"""
        # Очищуємо вікно
        for widget in self.root.winfo_children():
            widget.destroy()

        # Рамка меню
        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Заголовок
        title = tk.Label(
            menu_frame,
            text="🎴 ГРА 'СІМ' 🎴",
            font=("Arial", 32, "bold"),
            bg=self.bg_color,
            fg="#ecf0f1"
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            menu_frame,
            text="Python GUI + C++ Engine",
            font=("Arial", 14),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        subtitle.pack(pady=5)

        # Автор
        author_frame = tk.Frame(menu_frame, bg=self.bg_color)
        author_frame.pack(pady=20)

        tk.Label(
            author_frame,
            text="Розробник: Сергій Щербаков",
            font=("Arial", 11),
            bg=self.bg_color,
            fg="#ecf0f1"
        ).pack()

        tk.Label(
            author_frame,
            text="Email: sergiyscherbakov@ukr.net",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#95a5a6"
        ).pack()

        tk.Label(
            author_frame,
            text="Telegram: @s_help_2010",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#95a5a6"
        ).pack()

        # Кнопки вибору режиму
        button_frame = tk.Frame(menu_frame, bg=self.bg_color)
        button_frame.pack(pady=30)

        tk.Button(
            button_frame,
            text="🤖 Гра проти комп'ютера",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=25,
            height=2,
            command=self.start_ai_game,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="👥 Гра проти гравця",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            width=25,
            height=2,
            command=self.start_pvp_game,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        ).pack(pady=10)

    def start_ai_game(self):
        """Почати гру проти комп'ютера"""
        self.is_ai_game = True
        self.num_players = 2
        self.player_names = ["Ви", "Комп'ютер"]
        self.start_game()

    def start_pvp_game(self):
        """Почати гру проти іншого гравця"""
        self.is_ai_game = False
        self.num_players = 2
        self.player_names = ["Гравець 1", "Гравець 2"]
        self.start_game()

    def start_game(self):
        """Почати нову гру"""
        # Створюємо новий движок
        self.engine = SevenGameEngine(self.num_players)
        self.engine.deal_cards()

        # Показуємо ігрове поле
        self.show_game_board()

    def show_game_board(self):
        """Показати ігрове поле"""
        # Очищуємо вікно
        for widget in self.root.winfo_children():
            widget.destroy()

        # Верхня панель
        top_panel = tk.Frame(self.root, bg=self.bg_color, height=60)
        top_panel.pack(fill=tk.X, padx=10, pady=5)
        top_panel.pack_propagate(False)

        # Назва та кнопка виходу
        tk.Label(
            top_panel,
            text="🎴 ГРА 'СІМ'",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            top_panel,
            text="← Вихід в меню",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            command=self.show_menu,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=10)

        # Панель іншого гравця (зверху)
        other_player = 1 if self.engine.get_current_player() == 0 else 0
        self.create_player_panel(other_player, "top")

        # Стіл
        self.create_table()

        # Панель поточного гравця (знизу)
        current_player = self.engine.get_current_player()
        self.create_player_panel(current_player, "bottom")

        # Оновлюємо інтерфейс
        self.update_game_state()

    def create_player_panel(self, player_id, position):
        """Створити панель гравця"""
        if position == "top":
            panel = tk.Frame(self.root, bg=self.player_bg, height=150)
            panel.pack(fill=tk.X, padx=10, pady=5)
            panel.pack_propagate(False)
            setattr(self, 'top_player_panel', panel)
            setattr(self, 'top_player_id', player_id)
        else:
            panel = tk.Frame(self.root, bg=self.player_bg, height=180)
            panel.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
            panel.pack_propagate(False)
            setattr(self, 'bottom_player_panel', panel)
            setattr(self, 'bottom_player_id', player_id)

    def create_table(self):
        """Створити стіл"""
        table_frame = tk.Frame(self.root, bg=self.table_bg)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(
            table_frame,
            text="СТІЛ",
            font=("Arial", 16, "bold"),
            bg=self.table_bg,
            fg="white"
        ).pack(pady=10)

        self.table_cards_frame = tk.Frame(table_frame, bg=self.table_bg)
        self.table_cards_frame.pack(expand=True)

    def update_game_state(self):
        """Оновити стан гри"""
        state = self.engine.get_state()

        # Оновлюємо верхню панель
        self.update_player_panel(self.top_player_panel, self.top_player_id, False)

        # Оновлюємо нижню панель
        self.update_player_panel(self.bottom_player_panel, self.bottom_player_id, True)

        # Оновлюємо стіл
        self.update_table()

        # Перевіряємо переможця
        winner = self.engine.check_winner()
        if winner != -1:
            messagebox.showinfo(
                "Гра закінчена!",
                f"🎉 {self.player_names[winner]} виграв! 🎉"
            )
            self.show_menu()
            return

        # Якщо хід комп'ютера
        current_player = self.engine.get_current_player()
        if self.is_ai_game and current_player == 1:
            self.root.after(1000, self.ai_move)

    def update_player_panel(self, panel, player_id, show_cards):
        """Оновити панель гравця"""
        # Очищуємо панель
        for widget in panel.winfo_children():
            widget.destroy()

        state = self.engine.get_state()
        current_player = self.engine.get_current_player()

        # Ім'я гравця
        is_active = (player_id == current_player)
        bg_color = "#27ae60" if is_active else self.player_bg

        panel.configure(bg=bg_color)

        header = tk.Frame(panel, bg=bg_color)
        header.pack(pady=5)

        tk.Label(
            header,
            text=f"{self.player_names[player_id]}",
            font=("Arial", 14, "bold"),
            bg=bg_color,
            fg="white"
        ).pack(side=tk.LEFT, padx=10)

        cards_count = state.player_cards_count[player_id]
        tk.Label(
            header,
            text=f"Карт: {cards_count}",
            font=("Arial", 12),
            bg=bg_color,
            fg="white"
        ).pack(side=tk.LEFT)

        if is_active:
            tk.Label(
                header,
                text="← Ваш хід",
                font=("Arial", 12, "bold"),
                bg=bg_color,
                fg="#f39c12"
            ).pack(side=tk.LEFT, padx=10)

        # Карти
        if show_cards:
            cards_frame = tk.Frame(panel, bg=bg_color)
            cards_frame.pack(pady=5)

            cards = self.engine.get_player_cards(player_id)
            for card in cards:
                can_play = self.engine.can_play_card(player_id, card)
                self.create_card_button(cards_frame, card, player_id, can_play and is_active)

    def create_card_button(self, parent, card, player_id, can_play):
        """Створити кнопку карти"""
        card_text = str(card)

        # Колір масті
        suit_colors = {
            0: "#e74c3c",  # Черви - червоний
            1: "#e74c3c",  # Буби - червоний
            2: "#2c3e50",  # Хрести - чорний
            3: "#2c3e50",  # Піки - чорний
        }

        color = suit_colors.get(card.suit, "#2c3e50")

        btn = tk.Button(
            parent,
            text=card_text,
            font=("Arial", 16, "bold"),
            width=4,
            height=2,
            bg=self.card_bg if can_play else "#95a5a6",
            fg=color,
            relief=tk.RAISED if can_play else tk.FLAT,
            bd=3 if can_play else 1,
            cursor="hand2" if can_play else "arrow",
            state=tk.NORMAL if can_play else tk.DISABLED,
            command=lambda c=card: self.play_card(player_id, c)
        )
        btn.pack(side=tk.LEFT, padx=2, pady=2)

    def update_table(self):
        """Оновити стіл"""
        # Очищуємо стіл
        for widget in self.table_cards_frame.winfo_children():
            widget.destroy()

        state = self.engine.get_state()

        if all(state.table_card_count[i] == 0 for i in range(4)):
            tk.Label(
                self.table_cards_frame,
                text="Стіл порожній\nПочніть з сімки!",
                font=("Arial", 14),
                bg=self.table_bg,
                fg="white"
            ).pack(pady=20)
            return

        # Показуємо карти кожної масті
        for suit in range(4):
            if state.table_card_count[suit] > 0:
                suit_frame = tk.Frame(self.table_cards_frame, bg=self.table_bg)
                suit_frame.pack(pady=5)

                # Назва масті
                suit_names = ["♥ Черви", "♦ Буби", "♣ Хрести", "♠ Піки"]
                tk.Label(
                    suit_frame,
                    text=suit_names[suit] + ":",
                    font=("Arial", 12, "bold"),
                    bg=self.table_bg,
                    fg="white",
                    width=12
                ).pack(side=tk.LEFT, padx=5)

                # Карти
                cards_in_suit_frame = tk.Frame(suit_frame, bg=self.table_bg)
                cards_in_suit_frame.pack(side=tk.LEFT)

                for i in range(state.table_card_count[suit]):
                    card = state.table_state[suit][i]
                    self.create_table_card(cards_in_suit_frame, card)

    def create_table_card(self, parent, card):
        """Створити картку на столі"""
        card_text = str(card)

        suit_colors = {
            0: "#e74c3c", 1: "#e74c3c",
            2: "#2c3e50", 3: "#2c3e50"
        }

        tk.Label(
            parent,
            text=card_text,
            font=("Arial", 14, "bold"),
            width=4,
            bg="#ecf0f1",
            fg=suit_colors.get(card.suit, "#2c3e50"),
            relief=tk.RIDGE,
            bd=2
        ).pack(side=tk.LEFT, padx=2)

    def play_card(self, player_id, card):
        """Зіграти карту"""
        if self.engine.play_card(player_id, card):
            self.update_game_state()
        else:
            messagebox.showwarning("Помилка", "Не можна зіграти цю карту!")

    def ai_move(self):
        """Хід комп'ютера"""
        card = self.engine.computer_move()
        if card:
            # Показуємо що зіграв комп'ютер
            pass  # Карта вже зіграна
        else:
            # Комп'ютер пропустив хід
            pass

        self.update_game_state()


def main():
    """Головна функція"""
    root = tk.Tk()
    app = SevenGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
