#!/usr/bin/env python3
import re, sys
from pathlib import Path

PATTERNS = [
    r'(api[_-]?key|apikey)\s*[:=]\s*[\"']?\w{8,}',
    r'(secret|password|token|bearer)\s*[:=]\s*[\"']?\w{8,}',
    r'sk-[a-zA-Z0-9]{20,}',
]

def scan(filepath):
    content = Path(filepath).read_text()
    for pattern in PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        if any(matches):
            print(f"WARNING: potential secret found in {filepath}")
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-secrets.py <path>")
        sys.exit(1)
    if scan(sys.argv[1]):
        print(f"No obvious secrets found")
        sys.exit(0)
    else:
        sys.exit(1)
