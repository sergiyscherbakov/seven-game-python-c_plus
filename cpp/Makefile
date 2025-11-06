# Makefile для гри "Сім"
# Розробник: Сергій Щербаков
# Email: sergiyscherbakov@ukr.net

CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
SHARED_FLAGS = -fPIC -shared

# Файли
TARGET_CONSOLE = seven_game
TARGET_LIB = libseven_game.so
SOURCE_CONSOLE = seven_game.cpp
SOURCE_LIB = seven_game_lib.cpp
HEADER_LIB = seven_game_lib.h

# Кольори для виводу
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

.PHONY: all lib console clean run help

all: console lib
	@echo "$(GREEN)✓ Компіляція завершена успішно!$(NC)"

console: $(TARGET_CONSOLE)
	@echo "$(GREEN)✓ Консольна версія готова!$(NC)"

$(TARGET_CONSOLE): $(SOURCE_CONSOLE)
	@echo "$(YELLOW)Компіляція консольної версії...$(NC)"
	$(CXX) $(CXXFLAGS) -o $(TARGET_CONSOLE) $(SOURCE_CONSOLE)

lib: $(TARGET_LIB)
	@echo "$(GREEN)✓ Shared library готова!$(NC)"

$(TARGET_LIB): $(SOURCE_LIB) $(HEADER_LIB)
	@echo "$(YELLOW)Компіляція shared library...$(NC)"
	$(CXX) $(CXXFLAGS) $(SHARED_FLAGS) -o $(TARGET_LIB) $(SOURCE_LIB)

run: $(TARGET_CONSOLE)
	@echo "$(BLUE)Запуск консольної версії гри...$(NC)"
	@./$(TARGET_CONSOLE)

clean:
	@echo "$(YELLOW)Очищення...$(NC)"
	@rm -f $(TARGET_CONSOLE) $(TARGET_LIB)
	@echo "$(GREEN)✓ Очищення завершено!$(NC)"

help:
	@echo "Доступні команди:"
	@echo "  make          - Компіляція всього (консоль + бібліотека)"
	@echo "  make console  - Компіляція тільки консольної версії"
	@echo "  make lib      - Компіляція тільки shared library"
	@echo "  make run      - Компіляція та запуск консольної версії"
	@echo "  make clean    - Видалення скомпільованих файлів"
	@echo "  make help     - Показати це повідомлення"
