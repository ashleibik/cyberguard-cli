# CyberGuard CLI 🛡️

A terminal-based **cybersecurity incident response simulator**. Practice detecting and responding to attacks using realistic logs and commands.

## Features
- Randomized incident scenarios (brute force, SQL injection, phishing, crypto-miner).
- Terminal-style commands (`cat`, `grep`, `ps`, `kill`, `block ip`, `disable user`, etc.).
- Scoring for speed and correctness.
- Beginner-friendly, fully offline, no dependencies.

## Quick Start
```bash
# 1) Use Python 3.10+
python --version

# 2) Run the game
python run.py

# 3) (Optional) Run tests
python -m unittest
```

## Gameplay
- Each round spawns an incident. Use commands to investigate and mitigate.
- Type `help` to see available commands. Type `hint` if you’re stuck.
- Type `exit` anytime to quit.

## Example
```
> help
Available commands: cat, grep, ps, kill, block ip <IP>, disable user <USER>, reset password <USER>, hint, help, clear
> cat auth.log | grep failed
... suspicious login failures ...
> block ip 203.0.113.7
[OK] IP 203.0.113.7 blocked.
```

## Resume Bullet
**Built a command-line cybersecurity simulator** that trains incident response through realistic log analysis, command execution, and scoring; implemented attack generators (SQLi, brute force, phishing, crypto-mining), and a lightweight shell parser in Python.

## Repo Structure
```
cyberguard-cli/
├─ run.py
├─ cyberguard/
│  ├─ __init__.py
│  ├─ engine.py
│  ├─ attacks.py
│  ├─ scoring.py
│  └─ data/
│     └─ logs/
│        ├─ auth.log
│        ├─ web.log
│        └─ mail.log
└─ tests/
   └─ test_engine.py
```
