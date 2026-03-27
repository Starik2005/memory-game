"""Менеджер рекордов для Memory Game."""

import json
import os
from typing import List, Dict
from datetime import datetime


class ScoreManager:
    """Управление рекордами игры."""
    
    DEFAULT_FILE = "scores.json"
    MAX_RECORDS = 10
    
    def __init__(self, filepath: str = DEFAULT_FILE):
        """
        Инициализация менеджера рекордов.
        
        Args:
            filepath: Путь к файлу для сохранения рекордов.
        """
        self.filepath = filepath
        self.scores: List[Dict] = []
        self._load()
    
    def _load(self):
        """Загрузка рекордов из файла."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.scores = data.get("scores", [])
            except (json.JSONDecodeError, IOError):
                self.scores = []
        else:
            self.scores = []
    
    def _save(self):
        """Сохранение рекордов в файл."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump({"scores": self.scores}, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения рекордов: {e}")
    
    def add_score(self, size: int, moves: int, player_name: str = "Игрок"):
        """
        Добавление нового рекорда.
        
        Args:
            size: Размер поля.
            moves: Количество ходов.
            player_name: Имя игрока.
            
        Returns:
            True если рекорд добавлен в топ-10.
        """
        record = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "size": size,
            "moves": moves,
            "player": player_name,
        }
        
        # Фильтруем рекорды для этого размера поля
        size_scores = [s for s in self.scores if s["size"] == size]
        
        # Добавляем новый рекорд
        size_scores.append(record)
        
        # Сортируем по количеству ходов (меньше = лучше)
        size_scores.sort(key=lambda x: x["moves"])
        
        # Оставляем только топ-10
        size_scores = size_scores[:self.MAX_RECORDS]
        
        # Проверяем, попал ли новый рекорд в топ-10
        is_top_10 = record in size_scores
        
        # Обновляем общие рекорды
        other_scores = [s for s in self.scores if s["size"] != size]
        self.scores = other_scores + size_scores
        
        # Сортируем все рекорды для консистентности
        self.scores.sort(key=lambda x: (x["size"], x["moves"]))
        
        self._save()
        
        return is_top_10
    
    def get_top_scores(self, size: int | None = None, limit: int = 10) -> List[Dict]:
        """
        Получение лучших рекордов.
        
        Args:
            size: Размер поля (None для всех размеров).
            limit: Максимальное количество записей.
            
        Returns:
            Список рекордов.
        """
        if size is not None:
            scores = [s for s in self.scores if s["size"] == size]
        else:
            scores = self.scores
        
        # Сортируем по размеру поля, затем по ходам
        scores.sort(key=lambda x: (x["size"], x["moves"]))
        
        return scores[:limit]
    
    def get_best_for_size(self, size: int) -> int | None:
        """
        Получение лучшего результата для размера поля.
        
        Args:
            size: Размер поля.
            
        Returns:
            Минимальное количество ходов или None.
        """
        scores = [s for s in self.scores if s["size"] == size]
        if not scores:
            return None
        return min(s["moves"] for s in scores)
    
    def clear(self):
        """Очистка всех рекордов."""
        self.scores = []
        self._save()
