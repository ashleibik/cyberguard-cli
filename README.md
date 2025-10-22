# 🛡️ CyberGuard CLI (In Progress)
> A **Python terminal incident-response simulator** for practicing log forensics, process analysis, and containment workflows — built from scratch as a solo learning project.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-In%20progress-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## 🎯 Goal
Build a safe, realistic environment where users can **detect, investigate, and mitigate simulated cyber-attacks** using everyday command-line skills — no real system risk, pure learning.

---

## 🧩 Features
- 🔍 **Log analysis** — inspect `auth.log`, `web.log`, `mail.log`
- 🧠 **Simulated shell** — commands like `cat`, `grep`, `ps`, `kill`, `block ip`, `disable user`
- 🧱 **Attack scenarios**
  - SQL Injection  
  - SSH Brute Force  
  - Phishing Email Compromise  
  - Crypto-Miner Process
- 🕒 **Scoring system** — time & hint-based points
- ⚙️ **Safe sandbox** — no real OS commands executed

---

## 🚀 Run Locally
```bash
# clone the repository
git clone https://github.com/ashleibik/Cyberguard-Cli.git
cd Cyberguard-Cli

# optional: create virtual environment
python -m venv .venv
# Windows PowerShell:    .\.venv\Scripts\Activate.ps1
# macOS/Linux:           source .venv/bin/activate

# run the simulator
python run.py
