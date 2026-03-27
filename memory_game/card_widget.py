"""Виджет карточки для Memory Game."""

import tkinter as tk
from typing import Callable

from .theme import ThemeManager


class CardWidget(tk.Canvas):
    """Виджет карточки с анимацией переворота (оптимизированный)."""
    
    def __init__(
        self,
        parent,
        index: int,
        emoji: str,
        on_click: Callable[[int], None],
        size: int = 60,
        theme: ThemeManager = None,
    ):
        super().__init__(parent, width=size, height=size, highlightthickness=0, cursor="hand2")
        
        self.index = index
        self.emoji = emoji
        self.on_click = on_click
        self.card_size = size
        self.theme = theme or ThemeManager()
        self.is_flipped = False
        self.is_matched = False
        
        self._draw_back()
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _draw_back(self):
        """Нарисовать рубашку карточки."""
        self.delete("all")
        self.create_rectangle(0, 0, self.card_size, self.card_size, 
                             fill=self.theme.get("bg_card_back"), outline="")
        font_size = self.card_size // 3
        self.create_text(self.card_size // 2, self.card_size // 2,
                        text="❓", font=("Segoe UI Emoji", font_size),
                        fill=self.theme.get("text_primary"))
        self._is_showing_back = True
    
    def _draw_front(self):
        """Нарисовать лицевую сторону."""
        self.delete("all")
        fill_color = self.theme.get("bg_matched") if self.is_matched else self.theme.get("bg_card_front")
        self.create_rectangle(0, 0, self.card_size, self.card_size, fill=fill_color, outline="")
        font_size = self.card_size // 2
        self.create_text(self.card_size // 2, self.card_size // 2,
                        text=self.emoji, font=("Segoe UI Emoji", font_size))
        self._is_showing_back = False
    
    def _on_click(self, event=None):
        if not self.is_flipped and not self.is_matched:
            self.on_click(self.index)
    
    def _on_enter(self, event=None):
        if not self.is_flipped and not self.is_matched:
            self.itemconfig(1, fill=self.theme.get("bg_hover"))
    
    def _on_leave(self, event=None):
        if not self.is_flipped and not self.is_matched:
            self.itemconfig(1, fill=self.theme.get("bg_card_back"))
    
    def flip_show(self):
        self._draw_front()
        self.is_flipped = True
    
    def flip_hide(self):
        self._draw_back()
        self.is_flipped = False
    
    def mark_matched(self):
        self._draw_front()
        self.is_matched = True
    
    def reset(self, new_emoji: str | None = None):
        if new_emoji:
            self.emoji = new_emoji
        self.is_flipped = False
        self.is_matched = False
        self._draw_back()
