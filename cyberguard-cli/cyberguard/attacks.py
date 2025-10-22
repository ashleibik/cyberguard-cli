from __future__ import annotations
import re

def _sql_injection_success(shell) -> bool:
    # Success if suspicious IP is blocked
    return "198.51.100.42" in shell.blocked_ips

def _brute_force_success(shell) -> bool:
    # Success if IP blocked or user disabled/reset
    ip_blocked = "203.0.113.7" in shell.blocked_ips
    user_disabled = "devops" in shell.disabled_users
    return ip_blocked or user_disabled

def _phishing_success(shell) -> bool:
    # Success if user password reset
    # We don't track state for reset, but accept after they type reset password for 'jordan'
    return True if any(u for u in shell.disabled_users if u == "jordan") else False

def _miner_success(shell) -> bool:
    # Success if crypto miner process (1337) killed
    return 1337 not in shell.processes

ATTACKS = [
    {
        "name": "SQL Injection in Web Logs",
        "prompt": "Investigate web logs for SQL injection attempts. Mitigate the source.",
        "hint": "Look in web.log for patterns like ' OR 1=1 and block the offending IP.",
        "success": _sql_injection_success,
        "explain": "Blocking the attacking IP stops the injection attempt at the edge.",
    },
    {
        "name": "SSH Brute Force",
        "prompt": "Multiple failed SSH logins detected to user 'devops'. Find the IP and stop it.",
        "hint": "Search auth.log for 'Failed password' and then block that IP or disable the user.",
        "success": _brute_force_success,
        "explain": "Blocking the brute-force IP or disabling the target account halts the attack.",
    },
    {
        "name": "Phishing Email Compromise",
        "prompt": "User 'jordan' clicked a suspicious email. Contain the account.",
        "hint": "Review mail.log for IOC, then disable the user or reset password.",
        "success": _phishing_success,
        "explain": "Disabling the account prevents further misuse and begins recovery.",
    },
    {
        "name": "Crypto-Miner Process Detected",
        "prompt": "High CPU detected. Find and kill the malicious process.",
        "hint": "Use 'ps' to list processes and 'kill <pid>' to stop the miner.",
        "success": _miner_success,
        "explain": "Terminating the miner frees resources and removes the threat.",
    },
]
