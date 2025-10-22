from __future__ import annotations
import math

class Scoreboard:
    def __init__(self):
        self.rows = []  # (round_num, seconds, used_hint, points)

    def add(self, round_num: int, seconds: float, used_hint: bool) -> int:
        base = 100
        time_penalty = int(seconds)  # 1 point per second
        hint_penalty = 20 if used_hint else 0
        pts = max(10, base - time_penalty - hint_penalty)
        self.rows.append((round_num, seconds, used_hint, pts))
        return pts

    def summary(self) -> str:
        total = sum(r[3] for r in self.rows)
        lines = ["Round | Time(s) | Hint | Points"]
        for r in self.rows:
            lines.append(f"{r[0]:>5} | {r[1]:>7.1f} | {'Y' if r[2] else 'N':>4} | {r[3]:>6}")
        lines.append("-" * 30)
        lines.append(f"Total points: {total}")
        return "\n".join(lines)
