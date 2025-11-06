#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <string>
#include <map>
#include <ctime>

using namespace std;

// Масті карт
enum Suit { HEARTS, DIAMONDS, CLUBS, SPADES };
const string SUIT_NAMES[] = {"♥", "♦", "♣", "♠"};
const string SUIT_NAMES_FULL[] = {"Черви", "Буби", "Хрести", "Піки"};

// Структура карти
struct Card {
    int rank;      // Ранг: 6-14 (6-10, J=11, Q=12, K=13, A=14)
    Suit suit;

    string toString() const {
        string rankStr;
        if (rank <= 10) rankStr = to_string(rank);
        else if (rank == 11) rankStr = "J";
        else if (rank == 12) rankStr = "Q";
        else if (rank == 13) rankStr = "K";
        else if (rank == 14) rankStr = "A";
        return rankStr + SUIT_NAMES[suit];
    }
};

// Клас для колоди карт
class Deck {
private:
    vector<Card> cards;

public:
    Deck() {
        // Створюємо колоду з 36 карт (від 6 до туза)
        for (int suit = HEARTS; suit <= SPADES; suit++) {
            for (int rank = 6; rank <= 14; rank++) {
                cards.push_back({rank, static_cast<Suit>(suit)});
            }
        }
    }

    void shuffle() {
        random_device rd;
        mt19937 g(rd());
        std::shuffle(cards.begin(), cards.end(), g);
    }

    vector<Card> dealCards(int count) {
        vector<Card> dealt;
        for (int i = 0; i < count && !cards.empty(); i++) {
            dealt.push_back(cards.back());
            cards.pop_back();
        }
        return dealt;
    }

    bool isEmpty() const {
        return cards.empty();
    }
};

// Клас гравця
class Player {
protected:
    string name;
    vector<Card> hand;

public:
    Player(const string& n) : name(n) {}

    virtual ~Player() {}

    void addCards(const vector<Card>& cards) {
        hand.insert(hand.end(), cards.begin(), cards.end());
        sortHand();
    }

    void sortHand() {
        sort(hand.begin(), hand.end(), [](const Card& a, const Card& b) {
            if (a.suit != b.suit) return a.suit < b.suit;
            return a.rank < b.rank;
        });
    }

    void showHand() const {
        cout << "\n" << name << " має " << hand.size() << " карт(и):\n";
        for (size_t i = 0; i < hand.size(); i++) {
            cout << i + 1 << ". " << hand[i].toString() << "  ";
            if ((i + 1) % 9 == 0) cout << "\n";
        }
        cout << "\n";
    }

    bool hasCards() const {
        return !hand.empty();
    }

    int getCardCount() const {
        return hand.size();
    }

    string getName() const {
        return name;
    }

    virtual int selectCard(const map<Suit, pair<int, int>>& table, bool canPlaySeven) = 0;

    bool playCard(int index, vector<Card>& played) {
        if (index >= 0 && index < hand.size()) {
            played.push_back(hand[index]);
            hand.erase(hand.begin() + index);
            return true;
        }
        return false;
    }

    vector<int> getValidMoves(const map<Suit, pair<int, int>>& table) const {
        vector<int> valid;

        for (size_t i = 0; i < hand.size(); i++) {
            const Card& card = hand[i];

            // Перевірка чи можна зіграти сімку
            if (card.rank == 7) {
                if (table.find(card.suit) == table.end()) {
                    valid.push_back(i);
                    continue;
                }
            }

            // Перевірка чи можна зіграти іншу карту
            auto it = table.find(card.suit);
            if (it != table.end()) {
                int minRank = it->second.first;
                int maxRank = it->second.second;

                if (card.rank == minRank - 1 || card.rank == maxRank + 1) {
                    valid.push_back(i);
                }
            }
        }

        return valid;
    }
};

// Людський гравець
class HumanPlayer : public Player {
public:
    HumanPlayer(const string& n) : Player(n) {}

    int selectCard(const map<Suit, pair<int, int>>& table, bool canPlaySeven) override {
        showHand();

        vector<int> validMoves = getValidMoves(table);

        if (validMoves.empty()) {
            cout << "У вас немає можливих ходів. Пропускаєте хід.\n";
            return -1;
        }

        cout << "Можливі ходи: ";
        for (int idx : validMoves) {
            cout << (idx + 1) << " ";
        }
        cout << "\n";

        int choice;
        while (true) {
            cout << "Виберіть карту (номер) або 0 для пропуску ходу: ";
            cin >> choice;

            if (choice == 0) return -1;

            choice--;  // Перетворюємо в індекс масиву

            if (find(validMoves.begin(), validMoves.end(), choice) != validMoves.end()) {
                return choice;
            }

            cout << "Неправильний вибір! Спробуйте ще раз.\n";
        }
    }
};

// Комп'ютерний гравець
class ComputerPlayer : public Player {
public:
    ComputerPlayer(const string& n) : Player(n) {}

    int selectCard(const map<Suit, pair<int, int>>& table, bool canPlaySeven) override {
        vector<int> validMoves = getValidMoves(table);

        if (validMoves.empty()) {
            cout << name << " пропускає хід.\n";
            return -1;
        }

        // Проста стратегія: вибираємо випадковий хід з можливих
        random_device rd;
        mt19937 g(rd());
        uniform_int_distribution<> dis(0, validMoves.size() - 1);

        int selectedIdx = validMoves[dis(g)];
        cout << name << " грає карту: " << hand[selectedIdx].toString() << "\n";

        return selectedIdx;
    }
};

// Головний клас гри
class SevenGame {
private:
    vector<Player*> players;
    map<Suit, pair<int, int>> table;  // Для кожної масті: мінімальний та максимальний ранг на столі
    int currentPlayer;
    vector<int> consecutivePasses;

public:
    SevenGame() : currentPlayer(0) {}

    ~SevenGame() {
        for (auto player : players) {
            delete player;
        }
    }

    void addPlayer(Player* player) {
        players.push_back(player);
        consecutivePasses.push_back(0);
    }

    void dealCards() {
        Deck deck;
        deck.shuffle();

        int cardsPerPlayer = 36 / players.size();

        for (auto player : players) {
            player->addCards(deck.dealCards(cardsPerPlayer));
        }
    }

    void showTable() const {
        cout << "\n========== СТІЛ ==========\n";

        if (table.empty()) {
            cout << "Стіл порожній. Грайте сімку для початку!\n";
        } else {
            for (const auto& entry : table) {
                Suit suit = entry.first;
                int minRank = entry.second.first;
                int maxRank = entry.second.second;

                cout << SUIT_NAMES_FULL[suit] << ": ";
                for (int rank = minRank; rank <= maxRank; rank++) {
                    Card temp = {rank, suit};
                    cout << temp.toString() << " ";
                }
                cout << "\n";
            }
        }
        cout << "==========================\n\n";
    }

    bool makeMove() {
        Player* player = players[currentPlayer];

        cout << "\n>>> Хід гравця: " << player->getName() << " ("
             << player->getCardCount() << " карт) <<<\n";

        showTable();

        bool canPlaySeven = true;
        for (const auto& entry : table) {
            if (entry.second.first == 7 && entry.second.second == 7) {
                // Якщо всі масті вже мають сімку
                canPlaySeven = false;
            }
        }

        int selectedCard = player->selectCard(table, canPlaySeven);

        if (selectedCard == -1) {
            consecutivePasses[currentPlayer]++;
            currentPlayer = (currentPlayer + 1) % players.size();
            return true;
        }

        vector<Card> played;
        if (player->playCard(selectedCard, played)) {
            Card card = played[0];

            // Оновлюємо стіл
            if (table.find(card.suit) == table.end()) {
                // Нова масть на столі (має бути сімка)
                table[card.suit] = {card.rank, card.rank};
            } else {
                // Розширюємо діапазон для існуючої масті
                if (card.rank < table[card.suit].first) {
                    table[card.suit].first = card.rank;
                }
                if (card.rank > table[card.suit].second) {
                    table[card.suit].second = card.rank;
                }
            }

            consecutivePasses[currentPlayer] = 0;

            cout << player->getName() << " зіграв карту: " << card.toString() << "\n";

            // Перевірка на перемогу
            if (!player->hasCards()) {
                cout << "\n🎉 " << player->getName() << " ВИГРАВ! 🎉\n";
                return false;
            }
        }

        currentPlayer = (currentPlayer + 1) % players.size();
        return true;
    }

    bool allPlayersPassed() const {
        for (int passes : consecutivePasses) {
            if (passes == 0) return false;
        }
        return true;
    }

    void play() {
        cout << "\n🎴 === ГРА 'СІМ' РОЗПОЧАЛАСЯ! === 🎴\n\n";

        dealCards();

        while (true) {
            if (!makeMove()) {
                break;
            }

            if (allPlayersPassed()) {
                cout << "\nВсі гравці пропустили ход. Гра закінчена!\n";

                // Знаходимо гравця з найменшою кількістю карт
                int minCards = players[0]->getCardCount();
                int winner = 0;

                for (size_t i = 1; i < players.size(); i++) {
                    if (players[i]->getCardCount() < minCards) {
                        minCards = players[i]->getCardCount();
                        winner = i;
                    }
                }

                cout << "\n🏆 Переможець: " << players[winner]->getName()
                     << " (залишилось " << minCards << " карт) 🏆\n";
                break;
            }
        }

        cout << "\nДякуємо за гру!\n";
    }
};

int main() {
    // Встановлюємо локаль для підтримки українських символів
    setlocale(LC_ALL, "");

    cout << "╔════════════════════════════════════════╗\n";
    cout << "║       🎴 ГРА 'СІМ' 🎴                 ║\n";
    cout << "║                                        ║\n";
    cout << "║  Розробник: Сергій Щербаков           ║\n";
    cout << "║  Email: sergiyscherbakov@ukr.net      ║\n";
    cout << "║  Telegram: @s_help_2010               ║\n";
    cout << "╚════════════════════════════════════════╝\n\n";

    cout << "Оберіть режим гри:\n";
    cout << "1. Гра проти комп'ютера\n";
    cout << "2. Гра проти іншого гравця\n";
    cout << "Ваш вибір: ";

    int mode;
    cin >> mode;

    SevenGame game;

    if (mode == 1) {
        cout << "\nВведіть ваше ім'я: ";
        string playerName;
        cin >> playerName;

        game.addPlayer(new HumanPlayer(playerName));
        game.addPlayer(new ComputerPlayer("Комп'ютер"));
    } else if (mode == 2) {
        cout << "\nВведіть ім'я першого гравця: ";
        string player1Name;
        cin >> player1Name;

        cout << "Введіть ім'я другого гравця: ";
        string player2Name;
        cin >> player2Name;

        game.addPlayer(new HumanPlayer(player1Name));
        game.addPlayer(new HumanPlayer(player2Name));
    } else {
        cout << "Неправильний вибір!\n";
        return 1;
    }

    game.play();

    return 0;
}
