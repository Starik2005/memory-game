"""Виджет карточки для Memory Game."""

import tkinter as tk
from typing import Callable


class CardWidget(tk.Canvas):
    """Виджет карточки с анимацией переворота (оптимизированный)."""
    
    def __init__(
        self,
        parent,
        index: int,
        emoji: str,
        on_click: Callable[[int], None],
        size: int = 60,
    ):
        """
        Инициализация карточки.
        
        Args:
            parent: Родительский виджет.
            index: Индекс карточки на поле.
            emoji: Эмодзи на карточке.
            on_click: Callback при клике.
            size: Размер карточки в пикселях.
        """
        super().__init__(parent, width=size, height=size, highlightthickness=0, cursor="hand2")
        
        self.index = index
        self.emoji = emoji
        self.on_click = on_click
        self.card_size = size
        self.is_flipped = False
        self.is_matched = False
        
        # Настройка стиля
        self.bg_color = "#2c3e50"  # Тёмно-синий для рубашки
        self.fg_color = "#ecf0f1"  # Светлый для лицевой
        self.matched_color = "#27ae60"  # Зелёный для найденных
        
        # Рисуем рубашку
        self._draw_back()
        
        # Привязка клика
        self.bind("<Button-1>", self._on_click)
        
        # Ховер эффект
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _draw_back(self):
        """Нарисовать рубашку карточки."""
        self.delete("all")
        
        # Фон
        self.create_rectangle(0, 0, self.card_size, self.card_size, 
                             fill=self.bg_color, outline="")
        
        # Вопросительный знак
        font_size = self.card_size // 3
        self.create_text(self.card_size // 2, self.card_size // 2,
                        text="❓", font=("Segoe UI Emoji", font_size),
                        fill=self.fg_color)
        
        self._is_showing_back = True
    
    def _draw_front(self):
        """Нарисовать лицевую сторону."""
        self.delete("all")
        
        # Фон
        fill_color = self.matched_color if self.is_matched else self.fg_color
        self.create_rectangle(0, 0, self.card_size, self.card_size,
                             fill=fill_color, outline="")
        
        # Эмодзи
        font_size = self.card_size // 2
        self.create_text(self.card_size // 2, self.card_size // 2,
                        text=self.emoji, font=("Segoe UI Emoji", font_size))
        
        self._is_showing_back = False
    
    def _on_click(self, event=None):
        """Обработка клика."""
        if not self.is_flipped and not self.is_matched:
            self.on_click(self.index)
    
    def _on_enter(self, event=None):
        """Эффект при наведении."""
        if not self.is_flipped and not self.is_matched:
            self.itemconfig(1, fill="#34495e")  # Изменяем цвет фона
    
    def _on_leave(self, event=None):
        """Убрать эффект при уходе курсора."""
        if not self.is_flipped and not self.is_matched:
            self.itemconfig(1, fill=self.bg_color)
    
    def flip_show(self):
        """Показать лицевую сторону (перевернуть)."""
        self._draw_front()
        self.is_flipped = True
    
    def flip_hide(self):
        """Скрыть лицевую сторону (перевернуть обратно)."""
        self._draw_back()
        self.is_flipped = False
    
    def mark_matched(self):
        """Отметить карточку как найденную пару."""
        self._draw_front()  # Перерисовать с зелёным фоном
        self.is_matched = True
    
    def reset(self, new_emoji: str | None = None):
        """Сброс карточки в исходное состояние."""
        if new_emoji:
            self.emoji = new_emoji
        
        self.is_flipped = False
        self.is_matched = False
        self._draw_back()
