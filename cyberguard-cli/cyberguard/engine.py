from __future__ import annotations
import random, time, re, pathlib, sys
from .attacks import ATTACKS
from .scoring import Scoreboard

LOGS = {
    "auth.log": "auth.log",
    "web.log": "web.log",
    "mail.log": "mail.log",
}

HELP_TEXT = (
    "Available commands:\n"
    "  cat <file> [| grep <pattern>]\n"
    "  grep <pattern> <file>\n"
    "  ps\n"
    "  kill <pid>\n"
    "  block ip <IP>\n"
    "  disable user <USER>\n"
    "  reset password <USER>\n"
    "  hint\n"
    "  help\n"
    "  clear\n"
    "  exit\n"
)

class Shell:
    def __init__(self, logs_dir: pathlib.Path):
        self.logs_dir = logs_dir
        self.processes = {1337: "python crypto_miner.py", 2222: "nginx: worker", 3333: "sshd: root@pts/0"}
        self.blocked_ips = set()
        self.disabled_users = set()

    def cat(self, filename: str) -> str:
        path = self.logs_dir / filename
        if not path.exists():
            return f"cat: {filename}: No such file"
        return path.read_text()

    def grep(self, pattern: str, content: str) -> str:
        out = []
        try:
            rx = re.compile(pattern)
        except re.error:
            return f"grep: invalid regex '{pattern}'"
        for line in content.splitlines():
            if rx.search(line):
                out.append(line)
        return "\n".join(out)

    def ps(self) -> str:
        return "\n".join(f"{pid} {cmd}" for pid, cmd in sorted(self.processes.items()))

    def kill(self, pid_str: str) -> str:
        try:
            pid = int(pid_str)
        except ValueError:
            return "kill: PID must be an integer"
        if pid in self.processes:
            del self.processes[pid]
            return f"[OK] Killed process {pid}."
        return f"kill: {pid}: No such process"

    def block_ip(self, ip: str) -> str:
        self.blocked_ips.add(ip)
        return f"[OK] IP {ip} blocked."

    def disable_user(self, user: str) -> str:
        self.disabled_users.add(user)
        return f"[OK] User {user} disabled."

    def reset_password(self, user: str) -> str:
        return f"[OK] Initiated password reset flow for {user}."

    def run_line(self, line: str) -> str:
        line = line.strip()
        if not line:
            return ""
        if line == "help":
            return HELP_TEXT
        if line == "ps":
            return self.ps()
        if line.startswith("kill "):
            return self.kill(line.split(maxsplit=1)[1])
        if line.startswith("block ip "):
            return self.block_ip(line.split(maxsplit=2)[2])
        if line.startswith("disable user "):
            return self.disable_user(line.split(maxsplit=2)[2])
        if line.startswith("reset password "):
            return self.reset_password(line.split(maxsplit=2)[2])
        if line.startswith("grep "):
            # grep <pattern> <file>
            parts = line.split(maxsplit=2)
            if len(parts) < 3:
                return "usage: grep <pattern> <file>"
            pat, file = parts[1], parts[2]
            content = self.cat(file)
            if content.startswith("cat:"):
                return content
            return self.grep(pat, content)
        if line.startswith("cat "):
            # support pipe: cat <file> | grep <pattern>
            if "| grep" in line:
                left, _, right = line.partition("| grep")
                _, _, file = left.strip().partition(" ")
                pattern = right.strip()
                content = self.cat(file.strip())
                if content.startswith("cat:"):
                    return content
                return self.grep(pattern, content)
            else:
                _, _, file = line.partition(" ")
                return self.cat(file.strip())
        if line == "clear":
            return "\x1b[2J\x1b[H"
        if line == "exit":
            raise SystemExit
        return f"Unknown command: {line}. Type 'help'."

class Game:
    def __init__(self, logs_dir: pathlib.Path):
        self.shell = Shell(logs_dir)
        self.score = Scoreboard()

    def play_round(self, round_num: int) -> None:
        attack = random.choice(ATTACKS)
        print(f"\n=== Round {round_num}: {attack['name']} ===")
        print(attack["prompt"])
        t0 = time.time()
        used_hint = False
        while True:
            try:
                line = input("> ")
            except EOFError:
                print("\n[!] Input stream ended.")
                return
            if line.strip() == "hint":
                print("Hint:", attack["hint"])
                used_hint = True
                continue
            out = self.shell.run_line(line)
            if out:
                print(out)
            if attack["success"](self.shell):
                dt = time.time() - t0
                pts = self.score.add(round_num, dt, used_hint)
                print(f"[RESOLVED] {attack['name']} in {dt:.1f}s (+{pts} pts)")
                print("—", attack["explain"])
                break

    def run(self, rounds: int = 3):
        print("Welcome to CyberGuard CLI. Type 'help' for commands. Type 'hint' if stuck.")
        for r in range(1, rounds + 1):
            self.play_round(r)
        print("\nFinal Score:")
        print(self.score.summary())

def main():
    logs_dir = pathlib.Path(__file__).parent / "data" / "logs"
    Game(logs_dir).run()

if __name__ == "__main__":
    main()
