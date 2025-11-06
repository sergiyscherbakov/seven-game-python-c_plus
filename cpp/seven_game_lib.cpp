/**
 * Бібліотека гри "Сім" - Реалізація
 *
 * Розробник: Сергій Щербаков
 * Email: sergiyscherbakov@ukr.net
 * Telegram: @s_help_2010
 */

#include "seven_game_lib.h"
#include <vector>
#include <algorithm>
#include <random>
#include <map>
#include <ctime>

using namespace std;

// Внутрішній клас гри
class SevenGameEngine {
public:
    int num_players;
    int current_player;
    vector<vector<Card>> player_hands;
    map<int, pair<int, int>> table;  // suit -> (min_rank, max_rank)
    vector<int> consecutive_passes;

    SevenGameEngine(int players) : num_players(players), current_player(0) {
        player_hands.resize(players);
        consecutive_passes.resize(players, 0);
    }

    void dealCards() {
        vector<Card> deck;

        // Створюємо колоду
        for (int suit = 0; suit < 4; suit++) {
            for (int rank = 6; rank <= 14; rank++) {
                deck.push_back({rank, suit});
            }
        }

        // Перемішуємо
        random_device rd;
        mt19937 g(rd());
        shuffle(deck.begin(), deck.end(), g);

        // Роздаємо карти
        int cards_per_player = 36 / num_players;
        for (int p = 0; p < num_players; p++) {
            for (int i = 0; i < cards_per_player; i++) {
                player_hands[p].push_back(deck.back());
                deck.pop_back();
            }
            // Сортуємо карти
            sort(player_hands[p].begin(), player_hands[p].end(),
                [](const Card& a, const Card& b) {
                    if (a.suit != b.suit) return a.suit < b.suit;
                    return a.rank < b.rank;
                });
        }
    }

    bool canPlayCard(int player_id, Card card) {
        // Перевірка чи є карта у гравця
        auto& hand = player_hands[player_id];
        bool has_card = false;
        for (const auto& c : hand) {
            if (c.rank == card.rank && c.suit == card.suit) {
                has_card = true;
                break;
            }
        }
        if (!has_card) return false;

        // Сімку можна грати завжди, якщо масть ще не на столі
        if (card.rank == 7) {
            return table.find(card.suit) == table.end();
        }

        // Перевірка чи можна покласти карту
        auto it = table.find(card.suit);
        if (it == table.end()) return false;

        int min_rank = it->second.first;
        int max_rank = it->second.second;

        return (card.rank == min_rank - 1) || (card.rank == max_rank + 1);
    }

    bool playCard(int player_id, Card card) {
        if (!canPlayCard(player_id, card)) return false;

        // Видаляємо карту з руки
        auto& hand = player_hands[player_id];
        for (auto it = hand.begin(); it != hand.end(); ++it) {
            if (it->rank == card.rank && it->suit == card.suit) {
                hand.erase(it);
                break;
            }
        }

        // Оновлюємо стіл
        if (table.find(card.suit) == table.end()) {
            table[card.suit] = {card.rank, card.rank};
        } else {
            if (card.rank < table[card.suit].first) {
                table[card.suit].first = card.rank;
            }
            if (card.rank > table[card.suit].second) {
                table[card.suit].second = card.rank;
            }
        }

        consecutive_passes[player_id] = 0;
        current_player = (current_player + 1) % num_players;
        return true;
    }

    void passTurn() {
        consecutive_passes[current_player]++;
        current_player = (current_player + 1) % num_players;
    }

    int checkWinner() {
        // Перевірка чи хтось виграв (закінчились карти)
        for (int i = 0; i < num_players; i++) {
            if (player_hands[i].empty()) {
                return i;
            }
        }

        // Перевірка чи всі пропустили хід
        bool all_passed = true;
        for (int passes : consecutive_passes) {
            if (passes == 0) {
                all_passed = false;
                break;
            }
        }

        if (all_passed) {
            // Знаходимо гравця з найменшою кількістю карт
            int min_cards = player_hands[0].size();
            int winner = 0;
            for (int i = 1; i < num_players; i++) {
                if (player_hands[i].size() < min_cards) {
                    min_cards = player_hands[i].size();
                    winner = i;
                }
            }
            return winner;
        }

        return -1;  // Гра продовжується
    }

    bool computerMove(Card* played_card) {
        // Проста AI: знаходимо всі можливі ходи
        vector<Card> valid_moves;

        for (const auto& card : player_hands[current_player]) {
            if (canPlayCard(current_player, card)) {
                valid_moves.push_back(card);
            }
        }

        if (valid_moves.empty()) {
            passTurn();
            return false;
        }

        // Вибираємо випадковий хід
        random_device rd;
        mt19937 g(rd());
        uniform_int_distribution<> dis(0, valid_moves.size() - 1);

        *played_card = valid_moves[dis(g)];
        playCard(current_player, *played_card);
        return true;
    }
};

// C API реалізація

void* game_create(int num_players) {
    return new SevenGameEngine(num_players);
}

void game_deal_cards(void* game) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);
    engine->dealCards();
}

void game_get_state(void* game, GameState* state) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);

    state->current_player = engine->current_player;
    state->num_players = engine->num_players;

    for (int i = 0; i < engine->num_players; i++) {
        state->player_cards_count[i] = engine->player_hands[i].size();
    }

    for (int suit = 0; suit < 4; suit++) {
        state->table_card_count[suit] = 0;

        auto it = engine->table.find(suit);
        if (it != engine->table.end()) {
            int min_rank = it->second.first;
            int max_rank = it->second.second;

            int idx = 0;
            for (int rank = min_rank; rank <= max_rank; rank++) {
                state->table_state[suit][idx].rank = rank;
                state->table_state[suit][idx].suit = suit;
                idx++;
            }
            state->table_card_count[suit] = idx;
        }
    }
}

int game_get_player_cards(void* game, int player_id, Card* cards, int max_cards) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);

    if (player_id < 0 || player_id >= engine->num_players) return 0;

    int count = min((int)engine->player_hands[player_id].size(), max_cards);
    for (int i = 0; i < count; i++) {
        cards[i] = engine->player_hands[player_id][i];
    }

    return count;
}

int game_can_play_card(void* game, int player_id, Card card) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);
    return engine->canPlayCard(player_id, card) ? 1 : 0;
}

int game_play_card(void* game, int player_id, Card card) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);
    return engine->playCard(player_id, card) ? 1 : 0;
}

void game_pass_turn(void* game) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);
    engine->passTurn();
}

int game_check_winner(void* game) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);
    return engine->checkWinner();
}

int game_get_current_player(void* game) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);
    return engine->current_player;
}

int game_computer_move(void* game, Card* played_card) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);
    return engine->computerMove(played_card) ? 1 : 0;
}

void game_destroy(void* game) {
    SevenGameEngine* engine = static_cast<SevenGameEngine*>(game);
    delete engine;
}
