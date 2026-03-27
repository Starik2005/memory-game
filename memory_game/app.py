"""Главное окно приложения Memory Game."""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional

from .game import MemoryGame
from .card_widget import CardWidget
from .scores import ScoreManager


# Доступные размеры поля (только чётные)
GAME_SIZES = {
    "4×4": 4,
    "6×6": 6,
    "8×8": 8,
    "10×10": 10,
    "12×12": 12,
}
DEFAULT_SIZE = "6×6"


class MemoryGameApp:
    """Основное приложение Memory Game."""
    
    def __init__(self, root: Optional[tk.Tk] = None):
        self.root = root if root else tk.Tk()
        self.root.title("🎮 Memory Game")
        self.root.configure(bg="#1a1a2e")
        self.root.geometry("1100x700")
        self.root.minsize(800, 500)
        
        self.game: Optional[MemoryGame] = None
        self.cards: List[CardWidget] = []
        self.score_manager = ScoreManager()
        self._flip_after_id: Optional[str] = None
        
        self._setup_ui()
        self.new_game(6)
    
    def _setup_ui(self):
        self.main_container = tk.Frame(self.root, bg="#1a1a2e")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_game_panel()
        self._create_scores_panel()
    
    def _create_game_panel(self):
        game_frame = tk.Frame(self.main_container, bg="#1a1a2e")
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self._create_header(game_frame)
        self._create_board_frame(game_frame)
        self._create_footer(game_frame)
    
    def _create_header(self, parent):
        header = tk.Frame(parent, bg="#16213e", height=60)
        header.pack(fill=tk.X, padx=0, pady=(0, 10))
        header.pack_propagate(False)
        
        title = tk.Label(
            header, text="🎮 Memory Game",
            font=("Segoe UI Emoji", 20, "bold"),
            bg="#16213e", fg="#e94560",
        )
        title.pack(side=tk.LEFT, padx=10)
        
        stats_frame = tk.Frame(header, bg="#16213e")
        stats_frame.pack(side=tk.RIGHT, padx=10)
        
        self.moves_label = tk.Label(
            stats_frame, text="Ходы: 0",
            font=("Segoe UI", 14), bg="#16213e", fg="#ffffff",
        )
        self.moves_label.pack(side=tk.LEFT, padx=10)
        
        self.pairs_label = tk.Label(
            stats_frame, text="Пар: 0/0",
            font=("Segoe UI", 14), bg="#16213e", fg="#ffffff",
        )
        self.pairs_label.pack(side=tk.LEFT, padx=10)
    
    def _create_board_frame(self, parent):
        self.board_container = tk.Frame(parent, bg="#1a1a2e")
        self.board_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=5)
        
        self.board_canvas = tk.Canvas(self.board_container, bg="#1a1a2e", highlightthickness=0)
        
        v_scrollbar = ttk.Scrollbar(self.board_container, orient=tk.VERTICAL, command=self.board_canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.board_container, orient=tk.HORIZONTAL, command=self.board_canvas.xview)
        
        self.board_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.cards_frame = tk.Frame(self.board_canvas, bg="#1a1a2e")
        
        self.board_window = self.board_canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.cards_frame.bind("<Configure>", self._on_frame_configure)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.board_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.board_canvas.bind("<Configure>", self._on_canvas_resize)
        self.board_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_canvas_resize(self, event):
        if event and event.widget != self.board_canvas:
            return
        if hasattr(self, '_resize_after_id'):
            self.root.after_cancel(self._resize_after_id)
        self._resize_after_id = self.root.after(200, self._resize_cards)
    
    def _on_frame_configure(self, event=None):
        self.board_canvas.configure(scrollregion=self.board_canvas.bbox("all"))
    
    def _on_mousewheel(self, event):
        self.board_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _create_footer(self, parent):
        footer = tk.Frame(parent, bg="#16213e", height=60)
        footer.pack(fill=tk.X, padx=0, pady=(10, 0))
        footer.pack_propagate(False)
        
        size_label = tk.Label(
            footer, text="Размер:",
            font=("Segoe UI", 12), bg="#16213e", fg="#ffffff",
        )
        size_label.pack(side=tk.LEFT, padx=10)
        
        self.size_var = tk.StringVar(value=DEFAULT_SIZE)
        
        size_combo = ttk.Combobox(
            footer, textvariable=self.size_var,
            values=list(GAME_SIZES.keys()), state="readonly", width=8,
        )
        size_combo.pack(side=tk.LEFT, padx=5)
        size_combo.bind("<<ComboboxSelected>>", lambda e: self._on_size_selected(GAME_SIZES))
        
        new_game_btn = tk.Button(
            footer, text="🔄 Новая игра",
            font=("Segoe UI", 12, "bold"), bg="#e94560", fg="#ffffff",
            border=0, padx=20, pady=8, cursor="hand2", command=self._on_new_game,
        )
        new_game_btn.pack(side=tk.RIGHT, padx=10)
        
        self.size_var.trace_add("write", self._on_size_change)
    
    def _create_scores_panel(self):
        scores_frame = tk.Frame(self.main_container, bg="#16213e", width=280)
        scores_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        scores_frame.pack_propagate(False)
        
        title = tk.Label(
            scores_frame, text="🏆 Рекорды",
            font=("Segoe UI", 16, "bold"), bg="#16213e", fg="#e94560",
        )
        title.pack(pady=(10, 10))
        
        filter_label = tk.Label(
            scores_frame, text="Показать:",
            font=("Segoe UI", 11), bg="#16213e", fg="#ffffff",
        )
        filter_label.pack(pady=(0, 5))
        
        self.score_size_var = tk.StringVar(value="Все")
        score_sizes = ["Все"] + list(GAME_SIZES.keys())
        
        score_filter = ttk.Combobox(
            scores_frame, textvariable=self.score_size_var,
            values=score_sizes, state="readonly", width=10,
        )
        score_filter.pack(pady=(0, 10))
        score_filter.bind("<<ComboboxSelected>>", lambda e: self._update_scores_display())
        
        scores_container = tk.Frame(scores_frame, bg="#1a1a2e")
        scores_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.scores_canvas = tk.Canvas(scores_container, bg="#1a1a2e", highlightthickness=0)
        scores_scrollbar = ttk.Scrollbar(scores_container, orient=tk.VERTICAL, command=self.scores_canvas.yview)
        self.scores_canvas.configure(yscrollcommand=scores_scrollbar.set)
        
        self.scores_list_frame = tk.Frame(self.scores_canvas, bg="#1a1a2e")
        self.scores_canvas.create_window((0, 0), window=self.scores_list_frame, anchor="nw")
        self.scores_list_frame.bind("<Configure>", lambda e: self.scores_canvas.configure(scrollregion=self.scores_canvas.bbox("all")))
        
        scores_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scores_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        clear_btn = tk.Button(
            scores_frame, text="🗑️ Очистить",
            font=("Segoe UI", 10), bg="#e94560", fg="#ffffff",
            border=0, padx=15, pady=5, cursor="hand2", command=self._clear_scores,
        )
        clear_btn.pack(pady=10)
        
        self._update_scores_display()
    
    def _resize_cards(self):
        if not self.game:
            return
        
        revealed_indices = [i for i, r in enumerate(self.game.revealed) if r]
        matched_indices = [i for i, m in enumerate(self.game.matched) if m]
        
        for card in self.cards:
            card.destroy()
        self.cards.clear()
        
        self._create_cards()
        
        for i in revealed_indices:
            if i < len(self.cards):
                self.cards[i].flip_show()
        for i in matched_indices:
            if i < len(self.cards):
                self.cards[i].mark_matched()
    
    def _update_scores_display(self):
        for widget in self.scores_list_frame.winfo_children():
            widget.destroy()
        
        filter_size = self.score_size_var.get()
        size = None if filter_size == "Все" else GAME_SIZES.get(filter_size)
        
        scores = self.score_manager.get_top_scores(size=size, limit=10)
        
        if not scores:
            label = tk.Label(
                self.scores_list_frame, text="Пока нет рекордов",
                font=("Segoe UI", 11), bg="#1a1a2e", fg="#7f8c8d",
            )
            label.pack(pady=20)
            return
        
        header = tk.Frame(self.scores_list_frame, bg="#2c3e50")
        header.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(header, text="#", font=("Segoe UI", 10, "bold"), bg="#2c3e50", fg="#ffffff", width=3).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="Поле", font=("Segoe UI", 10, "bold"), bg="#2c3e50", fg="#ffffff", width=6).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="Ходы", font=("Segoe UI", 10, "bold"), bg="#2c3e50", fg="#ffffff", width=6).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="Дата", font=("Segoe UI", 10, "bold"), bg="#2c3e50", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        
        for i, score in enumerate(scores, 1):
            row = tk.Frame(self.scores_list_frame, bg="#1a1a2e")
            row.pack(fill=tk.X, pady=1)
            
            bg_color = "#243342" if i % 2 == 0 else "#1a1a2e"
            row.config(bg=bg_color)
            
            tk.Label(row, text=str(i), font=("Segoe UI", 10), bg=bg_color, fg="#ecf0f1", width=3, anchor="w").pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=f"{score['size']}×{score['size']}", font=("Segoe UI", 10), bg=bg_color, fg="#3498db", width=6, anchor="w").pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=str(score['moves']), font=("Segoe UI", 10, "bold"), bg=bg_color, fg="#e94560", width=6, anchor="w").pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=score['date'], font=("Segoe UI", 9), bg=bg_color, fg="#95a5a6").pack(side=tk.LEFT, padx=5)
        
        if self.game:
            best = self.score_manager.get_best_for_size(self.game.size)
            if best is not None:
                best_frame = tk.Frame(self.scores_list_frame, bg="#27ae60")
                best_frame.pack(fill=tk.X, pady=(10, 0))
                tk.Label(best_frame, text=f"🏆 Лучший: {best} ход.", font=("Segoe UI", 10, "bold"), bg="#27ae60", fg="#ffffff").pack(pady=5)
    
    def _clear_scores(self):
        self.score_manager.clear()
        self._update_scores_display()
    
    def _on_size_change(self, *args):
        pass
    
    def _on_size_selected(self, sizes_map, event=None):
        display_value = self.size_var.get()
        size = sizes_map.get(display_value, 6)
        self.new_game(size)
    
    def _on_new_game(self):
        display_value = self.size_var.get()
        size = GAME_SIZES.get(display_value, 6)
        self.new_game(size)
    
    def new_game(self, size: int):
        for card in self.cards:
            card.destroy()
        self.cards.clear()
        
        self.game = MemoryGame(size)
        self._update_stats()
        self._create_cards()
        
        self.score_size_var.set(f"{size}×{size}")
        self._update_scores_display()
    
    def _create_cards(self):
        if not self.game:
            return
        
        card_size = self._calculate_card_size()
        
        for i in range(len(self.game.board)):
            row = i // self.game.size
            col = i % self.game.size
            emoji = self.game.get_emoji(i)
            
            card = CardWidget(
                self.cards_frame, index=i, emoji=emoji,
                on_click=self._on_card_click, size=card_size,
            )
            card.grid(row=row, column=col, padx=3, pady=3)
            self.cards.append(card)
    
    def _calculate_card_size(self) -> int:
        if not self.game:
            return 60
        
        self.root.update_idletasks()
        canvas_width = self.board_canvas.winfo_width()
        canvas_height = self.board_canvas.winfo_height()
        
        available_width = canvas_width - 20
        available_height = canvas_height - 20
        
        card_width = available_width // self.game.size - 6
        card_height = available_height // self.game.size - 6
        
        card_size = min(card_width, card_height)
        card_size = max(30, min(card_size, 120))
        
        return card_size
    
    def _on_card_click(self, index: int):
        if not self.game:
            return
        
        if not self.game.flip_card(index):
            return
        
        self.cards[index].flip_show()
        self._update_stats()
        
        if len(self.game.flipped) == 2:
            idx1, idx2 = self.game.flipped
            
            if not self.game.matched[idx1]:
                if self._flip_after_id:
                    self.root.after_cancel(self._flip_after_id)
                
                self._flip_after_id = self.root.after(
                    800, lambda: self._hide_unmatched_cards(idx1, idx2),
                )
    
    def _hide_unmatched_cards(self, idx1: int, idx2: int):
        if not self.game:
            return
        
        self.game.reset_flipped()
        self.cards[idx1].flip_hide()
        self.cards[idx2].flip_hide()
        self._flip_after_id = None
    
    def _update_stats(self):
        if not self.game:
            return
        
        found = sum(self.game.matched) // 2
        total = self.game.pairs_count
        
        self.moves_label.config(text=f"Ходы: {self.game.moves}")
        self.pairs_label.config(text=f"Пар: {found}/{total}")
        
        if self.game.game_over:
            self._on_game_won()
    
    def _on_game_won(self):
        for card in self.cards:
            if card.is_flipped:
                card.mark_matched()
        
        self.score_manager.add_score(self.game.size, self.game.moves)
        self._update_scores_display()
        
        win_window = tk.Toplevel(self.root)
        win_window.title("🎉 Победа!")
        win_window.geometry("300x180")
        win_window.configure(bg="#16213e")
        
        win_window.update_idletasks()
        x = (win_window.winfo_screenwidth() - 300) // 2
        y = (win_window.winfo_screenheight() - 180) // 2
        win_window.geometry(f"300x180+{x}+{y}")
        
        win_window.after(10, lambda: win_window.grab_set())
        
        msg = tk.Label(
            win_window, text=f"🎉 Поздравляю!\n\nВы нашли все пары за {self.game.moves} ход.!",
            font=("Segoe UI", 14), bg="#16213e", fg="#ffffff", justify=tk.CENTER,
        )
        msg.pack(expand=True)
        
        close_btn = tk.Button(
            win_window, text="Закрыть",
            font=("Segoe UI", 11), bg="#e94560", fg="#ffffff",
            border=0, padx=20, pady=5, cursor="hand2", command=win_window.destroy,
        )
        close_btn.pack(pady=10)
    
    def run(self):
        self.root.mainloop()
