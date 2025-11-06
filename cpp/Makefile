# Makefile для гри "Сім"
# Розробник: Сергій Щербаков
# Email: sergiyscherbakov@ukr.net

CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
TARGET = seven_game
SOURCE = seven_game.cpp

# Кольори для виводу
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m # No Color

.PHONY: all clean run help

all: $(TARGET)
	@echo "$(GREEN)✓ Компіляція завершена успішно!$(NC)"

$(TARGET): $(SOURCE)
	@echo "$(YELLOW)Компіляція $(SOURCE)...$(NC)"
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE)

run: $(TARGET)
	@echo "$(GREEN)Запуск гри...$(NC)"
	@./$(TARGET)

clean:
	@echo "$(YELLOW)Очищення...$(NC)"
	@rm -f $(TARGET)
	@echo "$(GREEN)✓ Очищення завершено!$(NC)"

help:
	@echo "Доступні команди:"
	@echo "  make        - Компіляція програми"
	@echo "  make run    - Компіляція та запуск програми"
	@echo "  make clean  - Видалення скомпільованих файлів"
	@echo "  make help   - Показати це повідомлення"
