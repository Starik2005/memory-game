"""Менеджер тем для Memory Game."""

from typing import Dict


class ThemeManager:
    """Управление темами оформления."""
    
    # Тёмная тема (по умолчанию)
    DARK_THEME = {
        "bg_primary": "#1a1a2e",      # Основной фон
        "bg_secondary": "#16213e",    # Фон панелей
        "bg_tertiary": "#2c3e50",     # Фон заголовков
        "bg_card_back": "#2c3e50",    # Рубашка карточки
        "bg_card_front": "#ecf0f1",   # Лицо карточки
        "bg_matched": "#27ae60",      # Найденная пара
        "bg_hover": "#34495e",        # Наведение
        "bg_row_alt": "#243342",      # Чередование строк
        "text_primary": "#ffffff",    # Основной текст
        "text_secondary": "#ecf0f1",  # Вторичный текст
        "text_muted": "#95a5a6",      # Приглушённый текст
        "accent": "#e94560",          # Акцент (кнопки, заголовки)
        "accent_blue": "#3498db",     # Синий акцент
        "border": "#34495e",          # Границы
    }
    
    # Светлая тема
    LIGHT_THEME = {
        "bg_primary": "#f5f6fa",      # Основной фон
        "bg_secondary": "#ffffff",    # Фон панелей
        "bg_tertiary": "#dcdde1",     # Фон заголовков
        "bg_card_back": "#3498db",    # Рубашка карточки
        "bg_card_front": "#ffffff",   # Лицо карточки
        "bg_matched": "#2ecc71",      # Найденная пара
        "bg_hover": "#5dade2",        # Наведение
        "bg_row_alt": "#eaecee",      # Чередование строк
        "text_primary": "#2c3e50",    # Основной текст
        "text_secondary": "#34495e",  # Вторичный текст
        "text_muted": "#7f8c8d",      # Приглушённый текст
        "accent": "#e74c3c",          # Акцент (кнопки, заголовки)
        "accent_blue": "#2980b9",     # Синий акцент
        "border": "#bdc3c7",          # Границы
    }
    
    def __init__(self):
        self.current_theme = "dark"
        self.colors = self.DARK_THEME.copy()
    
    def set_theme(self, theme_name: str):
        """Установить тему."""
        if theme_name == "light":
            self.current_theme = "light"
            self.colors = self.LIGHT_THEME.copy()
        else:
            self.current_theme = "dark"
            self.colors = self.DARK_THEME.copy()
    
    def toggle(self) -> str:
        """Переключить тему и вернуть новое название."""
        self.set_theme("light" if self.current_theme == "dark" else "dark")
        return self.current_theme
    
    def get(self, key: str) -> str:
        """Получить цвет по ключу."""
        return self.colors.get(key, "#000000")
    
    def is_dark(self) -> bool:
        """Проверить, тёмная ли тема."""
        return self.current_theme == "dark"
