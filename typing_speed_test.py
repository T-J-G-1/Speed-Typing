"""
Typing Speed Test (Tkinter) — upgraded version

Changes made:
- Uses 5 target paragraphs (selectable) and stores a separate high score per paragraph
- Measures WPM (standard: 5 characters = 1 word) based on *correct characters only*
- Also shows accuracy %
- Disables input until the typing test starts; disables again when it ends
- Safer high score loading/saving (JSON), no crashing on empty/corrupt files
- Refactored into a clean class-based app (no globals)
"""

import json
import os
import tkinter as tk
from tkinter import messagebox

BACKGROUND = "#f0f0f0"
HIGH_SCORE_FILE = "high_scores.json"


PARAGRAPHS = [
    "The quick brown fox jumps over the lazy dog. It is a classic sentence used to test typing because it contains every letter of the alphabet.",
    "When you learn to type with accuracy, speed comes naturally. Focus on steady rhythm, light keystrokes, and keeping your eyes on the screen instead of the keyboard.",
    "A small habit practiced daily becomes a powerful skill over time. If you type for five minutes each day, you will be surprised at how quickly your confidence improves.",
    "Software development is built on problem-solving. Breaking a task into smaller steps helps you move forward, even when the solution is not obvious at first.",
    "The ocean was calm, and the ship drifted quietly beneath the moon. Somewhere beyond the horizon, a new island waited with secrets hidden in its jungle paths.",
]


def safe_load_scores() -> dict:
    """Load high scores from JSON. Returns {} if missing or invalid."""
    if not os.path.exists(HIGH_SCORE_FILE):
        return {}
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def safe_save_scores(scores: dict) -> None:
    """Save high scores to JSON."""
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except OSError:
        # If saving fails, we silently ignore (or you could show a messagebox)
        pass


class TypingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")
        self.root.configure(background=BACKGROUND)
        self.root.minsize(520, 620)
        self.root.maxsize(520, 620)

        # Optional: frameless always-on-top widget window (your original behaviour)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # Drag to move window
        self.root.bind("<B1-Motion>", self.move_window)

        # State
        self.countdown_seconds = 5
        self.test_seconds = 30

        self.is_running = False
        self.remaining = 0
        self.timer_job = None

        self.scores = safe_load_scores()  # { "0": 72.5, "1": 65.0, ... }

        # UI
        self.build_ui()
        self.refresh_high_score_display()

    def move_window(self, event):
        self.root.geometry(f"+{event.x_root}+{event.y_root}")

    def build_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="Typing Speed Test",
            bg=BACKGROUND,
            font=("Arial", 24, "bold"),
        )
        title.pack(pady=(12, 6))

        # Exit button
        exit_button = tk.Button(self.root, text="X", command=self.root.quit, bg="red", fg="white")
        exit_button.place(x=490, y=10)

        # Paragraph selector
        selector_frame = tk.Frame(self.root, bg=BACKGROUND)
        selector_frame.pack(pady=(8, 6), fill="x", padx=12)

        tk.Label(selector_frame, text="Paragraph:", bg=BACKGROUND, font=("Arial", 12, "bold")).pack(side="left")

        self.paragraph_var = tk.StringVar(value="1")
        options = [str(i + 1) for i in range(len(PARAGRAPHS))]
        self.paragraph_menu = tk.OptionMenu(selector_frame, self.paragraph_var, *options, command=self.on_paragraph_change)
        self.paragraph_menu.pack(side="left", padx=8)

        # Target text display
        self.target_label = tk.Label(
            self.root,
            text=PARAGRAPHS[0],
            bg=BACKGROUND,
            font=("Arial", 12),
            wraplength=490,
            justify="left",
        )
        self.target_label.pack(padx=12, pady=(6, 10), fill="x")

        # Timer label
        self.timer_label = tk.Label(self.root, text="Ready", bg=BACKGROUND, font=("Arial", 20, "bold"))
        self.timer_label.pack(pady=(0, 10))

        # Score label
        self.score_label = tk.Label(
            self.root,
            text="WPM: 0.00  |  Accuracy: 0.00%",
            bg=BACKGROUND,
            font=("Arial", 16),
        )
        self.score_label.pack(pady=(0, 8))

        # High score label (per paragraph)
        self.high_score_label = tk.Label(
            self.root,
            text="High Score (this paragraph): 0.00 WPM",
            bg=BACKGROUND,
            font=("Arial", 14),
        )
        self.high_score_label.pack(pady=(0, 12))

        # Input box
        self.input_box = tk.Text(self.root, width=60, height=10, state=tk.DISABLED)
        self.input_box.pack(padx=12, pady=(0, 12))
        self.input_box.bind("<KeyRelease>", self.on_key_release)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BACKGROUND)
        btn_frame.pack(pady=(0, 10))

        self.start_button = tk.Button(btn_frame, text="Start", width=14, command=self.start_test)
        self.start_button.pack(side="left", padx=6)

        self.reset_one_button = tk.Button(btn_frame, text="Reset This High Score", width=20, command=self.confirm_reset_current)
        self.reset_one_button.pack(side="left", padx=6)

        self.reset_all_button = tk.Button(btn_frame, text="Reset ALL High Scores", width=20, command=self.confirm_reset_all)
        self.reset_all_button.pack(side="left", padx=6)

        # Small help text
        help_text = tk.Label(
            self.root,
            text="Tip: You score based on correct characters typed.\nWPM uses the standard 5 characters = 1 word.",
            bg=BACKGROUND,
            font=("Arial", 11),
        )
        help_text.pack(pady=(6, 0))

    def on_paragraph_change(self, _=None):
        idx = self.current_paragraph_index()
        self.target_label.config(text=PARAGRAPHS[idx])
        self.refresh_high_score_display()
        self.reset_ui_state()

    def current_paragraph_index(self) -> int:
        # paragraph_var is "1".."5"
        try:
            return int(self.paragraph_var.get()) - 1
        except ValueError:
            return 0

    def current_paragraph_key(self) -> str:
        return str(self.current_paragraph_index())

    def refresh_high_score_display(self):
        key = self.current_paragraph_key()
        hs = float(self.scores.get(key, 0.0))
        self.high_score_label.config(text=f"High Score (this paragraph): {hs:.2f} WPM")

    def reset_ui_state(self):
        # Stop timers if running
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

        self.is_running = False
        self.remaining = 0
        self.timer_label.config(text="Ready", fg="black")

        self.score_label.config(text="WPM: 0.00  |  Accuracy: 0.00%")
        self.input_box.config(state=tk.NORMAL)
        self.input_box.delete("1.0", "end")
        self.input_box.config(state=tk.DISABLED)

    def start_test(self):
        if self.is_running:
            return

        # Reset UI
        self.input_box.config(state=tk.NORMAL)
        self.input_box.delete("1.0", "end")
        self.input_box.config(state=tk.DISABLED)

        self.score_label.config(text="WPM: 0.00  |  Accuracy: 0.00%")

        # Start countdown
        self.is_running = True
        self.remaining = self.countdown_seconds
        self.update_countdown()

    def update_countdown(self):
        if not self.is_running:
            return

        if self.remaining > 0:
            self.timer_label.config(text=str(self.remaining), fg="black")
            self.remaining -= 1
            self.timer_job = self.root.after(1000, self.update_countdown)
        else:
            # Start typing phase
            self.remaining = self.test_seconds
            self.input_box.config(state=tk.NORMAL)
            self.input_box.focus_set()
            self.update_typing_timer()

    def update_typing_timer(self):
        if not self.is_running:
            return

        if self.remaining > 0:
            # Visual urgency
            if self.remaining <= 5:
                self.timer_label.config(fg="red")
            else:
                self.timer_label.config(fg="black")

            self.timer_label.config(text=f"Time left: {self.remaining}")
            self.remaining -= 1
            self.timer_job = self.root.after(1000, self.update_typing_timer)
        else:
            self.end_test()

    def end_test(self):
        if not self.is_running:
            return

        self.is_running = False
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

        self.input_box.config(state=tk.DISABLED)
