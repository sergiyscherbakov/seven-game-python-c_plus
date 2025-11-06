/**
 * Бібліотека гри "Сім" - C API для інтеграції з Python
 *
 * Розробник: Сергій Щербаков
 * Email: sergiyscherbakov@ukr.net
 * Telegram: @s_help_2010
 */

#ifndef SEVEN_GAME_LIB_H
#define SEVEN_GAME_LIB_H

#ifdef __cplusplus
extern "C" {
#endif

// Структура карти
typedef struct {
    int rank;  // 6-14 (6-10, J=11, Q=12, K=13, A=14)
    int suit;  // 0-3 (Hearts, Diamonds, Clubs, Spades)
} Card;

// Структура для опису стану гри
typedef struct {
    int current_player;
    int num_players;
    int player_cards_count[4];  // Кількість карт у кожного гравця
    Card table_state[4][9];     // Стан столу для кожної масті (макс 9 карт: 6-14)
    int table_card_count[4];    // Кількість карт на столі для кожної масті
} GameState;

// Ініціалізація гри
void* game_create(int num_players);

// Роздача карт
void game_deal_cards(void* game);

// Отримання стану гри
void game_get_state(void* game, GameState* state);

// Отримання карт гравця
int game_get_player_cards(void* game, int player_id, Card* cards, int max_cards);

// Перевірка чи можна зіграти карту
int game_can_play_card(void* game, int player_id, Card card);

// Зіграти карту
int game_play_card(void* game, int player_id, Card card);

// Пропустити хід
void game_pass_turn(void* game);

// Перевірка на перемогу
int game_check_winner(void* game);

// Отримання поточного гравця
int game_get_current_player(void* game);

// Хід комп'ютера (AI)
int game_computer_move(void* game, Card* played_card);

// Очищення гри
void game_destroy(void* game);

#ifdef __cplusplus
}
#endif

#endif // SEVEN_GAME_LIB_H
