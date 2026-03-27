#!/usr/bin/env python3
"""DIY Projects - главный файл запуска."""

import sys


def run_memory_game():
    """Запуск игры Memory."""
    from memory_game import MemoryGameApp
    
    app = MemoryGameApp()
    app.run()


if __name__ == "__main__":
    # Запуск игры Memory по умолчанию
    run_memory_game()
