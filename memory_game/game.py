"""Логика игры Memory."""

import random
from typing import List


class MemoryGame:
    """Класс игры Memory (Найди пару)."""
    
    # Набор эмодзи для карточек (60 штук для поля до 20x20)
    EMOJIS = [
        "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯",
        "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🐤", "🦆",
        "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋",
        "🐌", "🐞", "🐜", "🦟", "🦗", "🕷️", "🦂", "🐢", "🐍", "🦎",
        "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟",
        "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧",
        "🐘", "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🐃", "🐂", "🐄",
        "🐎", "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🦮",
        "🐈", "🐓", "🦃", "🦚", "🦜", "🦢", "🦩", "🕊️", "🐇", "🦝",
        "🦨", "🦡", "🦦", "🦥", "🐁", "🐀", "🐿️", "🦔", "🌸", "🌺",
    ]
    
    def __init__(self, size: int = 6):
        """
        Инициализация игры.
        
        Args:
            size: Размер поля (size x size). Должно быть чётное количество клеток.
        """
        self.size = size
        self.total_cards = size * size
        self.pairs_count = self.total_cards // 2
        
        # Состояние игры
        self.board: List[str] = []  # Эмодзи на позициях
        self.revealed: List[bool] = []  # Какие карточки открыты
        self.matched: List[bool] = []  # Какие пары найдены
        self.flipped: List[int] = []  # Индексы текущих открытых карт (макс 2)
        self.moves = 0  # Количество ходов
        self.game_over = False
        
        self._setup_board()
    
    def _setup_board(self):
        """Создание игрового поля."""
        # Выбираем нужное количество эмодзи
        selected_emojis = self.EMOJIS[:self.pairs_count]
        
        # Создаём пары
        cards = selected_emojis * 2
        random.shuffle(cards)
        
        self.board = cards
        
        self.revealed = [False] * len(self.board)
        self.matched = [False] * len(self.board)
        self.flipped = []
        self.moves = 0
        self.game_over = False
    
    def flip_card(self, index: int) -> bool:
        """
        Переворот карточки.

        Args:
            index: Индекс карточки на поле.

        Returns:
            True если карточка перевернулась, False если нет.
        """
        # Нельзя переворачивать, если уже 2 открыты или карточка уже открыта/найдена
        if len(self.flipped) >= 2:
            return False
        if index in self.flipped:
            return False
        if self.matched[index]:
            return False

        self.revealed[index] = True
        self.flipped.append(index)

        # Если открыли вторую карточку - проверяем совпадение
        if len(self.flipped) == 2:
            self.moves += 1
            self._check_match()

        return True
    
    def _check_match(self):
        """Проверка совпадения двух открытых карточек."""
        idx1, idx2 = self.flipped[0], self.flipped[1]
        
        if self.board[idx1] == self.board[idx2]:
            # Совпадение!
            self.matched[idx1] = True
            self.matched[idx2] = True
            self.flipped = []
            
            # Проверка на победу
            if all(self.matched):
                self.game_over = True
        else:
            # Не совпали - карточки перевернутся позже
            pass
    
    def reset_flipped(self):
        """Сброс открытых карточек (после анимации)."""
        for idx in self.flipped:
            self.revealed[idx] = False
        self.flipped = []
    
    def restart(self, new_size: int | None = None):
        """
        Перезапуск игры.

        Args:
            new_size: Новый размер поля (опционально).
        """
        if new_size and new_size != self.size:
            self.size = new_size
            self.total_cards = self.size * self.size
            self.pairs_count = self.total_cards // 2
        
        self._setup_board()
    
    def get_emoji(self, index: int) -> str:
        """Получить эмодзи карточки по индексу."""
        return self.board[index]
    
    def is_revealed(self, index: int) -> bool:
        """Проверить, открыта ли карточка."""
        return self.revealed[index] or self.matched[index]
    
    def is_matched(self, index: int) -> bool:
        """Проверить, найдена ли пара."""
        return self.matched[index]
    
    def should_hide(self, index: int) -> bool:
        """Проверить, нужно ли скрыть карточку (открыта, но не найдена и не в текущих flipped)."""
        return self.revealed[index] and index not in self.flipped and not self.matched[index]
