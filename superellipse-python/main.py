"""Интерактивная визуализация суперэллипса на Tkinter.

Формула обобщённого суперэллипса:
    x(t) = a * sign(cos(t)) * |cos(t)| ** (2 / n)
    y(t) = b * sign(sin(t)) * |sin(t)| ** (2 / n)

При n = 2 получается обычный эллипс. При a = b полуоси равны.
"""
import math
import tkinter as tk
from tkinter import ttk


class SuperellipseApp:
    """Окно приложения и логика отрисовки суперэллипса."""

    BG = "#151923"
    PANEL = "#202635"
    GRID = "#30394b"
    LINE = "#7dd3fc"
    TEXT = "#edf2f7"
    MUTED = "#aab6c8"
    ACCENT = "#38bdf8"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Суперэллипс — интерактивная визуализация")
        self.root.geometry("900x700")
        self.root.minsize(620, 520)
        self.root.configure(bg=self.BG)

        self.n_value = tk.DoubleVar(value=2.0)
        self.equal_axes = tk.BooleanVar(value=True)
        self.a_value = tk.DoubleVar(value=1.0)
        self.b_value = tk.DoubleVar(value=0.7)

        self._build_ui()
        self.root.bind("<Configure>", self._on_resize)
        self.redraw()

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg=self.BG, padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(
            header, text="СУПЕРЭЛЛИПС", bg=self.BG, fg=self.TEXT,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Изучай, как параметр n меняет форму кривой Ламе",
            bg=self.BG, fg=self.MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

        self.canvas = tk.Canvas(
            self.root, bg="#10141c", highlightthickness=0, bd=0
        )
        self.canvas.pack(fill="both", expand=True, padx=24, pady=(0, 14))

        controls = tk.Frame(self.root, bg=self.PANEL, padx=20, pady=14)
        controls.pack(fill="x", padx=24, pady=(0, 20))

        top = tk.Frame(controls, bg=self.PANEL)
        top.pack(fill="x")
        self.n_label = tk.Label(
            top, text="Показатель n = 2.00", bg=self.PANEL, fg=self.TEXT,
            font=("Segoe UI", 11, "bold")
        )
        self.n_label.pack(side="left")
        self.shape_label = tk.Label(
            top, text="Обычный эллипс", bg=self.PANEL, fg=self.ACCENT,
            font=("Segoe UI", 10)
        )
        self.shape_label.pack(side="right")

        self.n_scale = ttk.Scale(
            controls, from_=0.5, to=8.0, orient="horizontal",
            variable=self.n_value, command=self._on_n_change
        )
        self.n_scale.pack(fill="x", pady=(12, 8))

        tick_row = tk.Frame(controls, bg=self.PANEL)
        tick_row.pack(fill="x")
        for value, label in ((0.5, "0.5"), (1, "1"), (2, "2"), (4, "4"), (6, "6"), (8, "8")):
            tk.Label(tick_row, text=label, bg=self.PANEL, fg=self.MUTED,
                     font=("Segoe UI", 9)).pack(side="left", expand=True)
        tk.Button(
            controls, text="Сбросить n = 2", command=self.reset,
            bg="#26384b", fg=self.TEXT, activebackground="#34506b",
            activeforeground=self.TEXT, relief="flat", padx=12, pady=6,
            cursor="hand2"
        ).pack(anchor="e", pady=(10, 0))

        self.root.bind("<Left>", lambda _event: self.n_value.set(max(0.5, self.n_value.get() - 0.1)) or self.redraw())
        self.root.bind("<Right>", lambda _event: self.n_value.set(min(8.0, self.n_value.get() + 0.1)) or self.redraw())

    def _on_n_change(self, _value: str) -> None:
        self.redraw()

    def _on_resize(self, event: tk.Event) -> None:
        if event.widget is self.root:
            self.root.after_idle(self.redraw)

    @staticmethod
    def _signed_power(value: float, exponent: float) -> float:
        if abs(value) < 1e-12:
            return 0.0
        return math.copysign(abs(value) ** exponent, value)

    def _shape_description(self, n: float) -> str:
        if abs(n - 2.0) < 0.08:
            return "Обычный эллипс"
        if n < 1.8:
            return "Ромбовидная форма"
        if n < 2.5:
            return "Переходная форма"
        if n < 5.5:
            return "Скруглённый прямоугольник"
        return "Почти квадрат"

    def redraw(self) -> None:
        if not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 200)
        height = max(self.canvas.winfo_height(), 200)
        cx, cy = width / 2, height / 2
        radius = max(40, min(width * 0.34, height * 0.36))
        n = max(0.5, min(8.0, self.n_value.get()))
        exponent = 2.0 / n

        # Лёгкая координатная сетка и оси помогают видеть симметрию.
        for x in range(int(cx) % 40, width, 40):
            self.canvas.create_line(x, 0, x, height, fill=self.GRID, width=1)
        for y in range(int(cy) % 40, height, 40):
            self.canvas.create_line(0, y, width, y, fill=self.GRID, width=1)
        self.canvas.create_line(20, cy, width - 20, cy, fill="#566176", width=1)
        self.canvas.create_line(cx, 20, cx, height - 20, fill="#566176", width=1)

        points = []
        steps = 900
        for i in range(steps + 1):
            t = 2 * math.pi * i / steps
            x = self._signed_power(math.cos(t), exponent)
            y = self._signed_power(math.sin(t), exponent)
            points.extend((cx + radius * x, cy - radius * y))

        self.canvas.create_polygon(
            points, fill="#17374a", outline=self.LINE, width=2.5,
            smooth=False
        )
        # Небольшие маркеры на осях показывают полуоси.
        for x, y in ((cx + radius, cy), (cx - radius, cy),
                     (cx, cy + radius), (cx, cy - radius)):
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                                    fill="#e0f2fe", outline="")

        self.n_label.configure(text=f"Показатель n = {n:.2f}")
        self.shape_label.configure(text=self._shape_description(n))
        self.canvas.create_text(
            16, 14, anchor="nw", text=f"x = sign(cos t) · |cos t|^{exponent:.2f}",
            fill=self.MUTED, font=("Consolas", 9)
        )
        self.canvas.create_text(
            16, 32, anchor="nw", text=f"y = sign(sin t) · |sin t|^{exponent:.2f}",
            fill=self.MUTED, font=("Consolas", 9)
        )

    def reset(self) -> None:
        self.n_value.set(2.0)
        self.redraw()


def main() -> None:
    root = tk.Tk()
    SuperellipseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
