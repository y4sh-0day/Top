#!/usr/bin/env python3
"""CmdRush CLI - type real terminal commands against the clock, right in your terminal.

Usage:
  python3 cli/cmdrush.py                     # all packs, speed mode, 60s
  python3 cli/cmdrush.py -p git -m recall    # git pack, recall mode
  python3 cli/cmdrush.py --list              # show available packs
"""
import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "commands.json"
BEST_FILE = Path.home() / ".cmdrush.json"

USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def c(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


GREEN, RED, YELLOW, GREY, BOLD = "32", "31", "33", "90", "1"


def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_best():
    try:
        return json.loads(BEST_FILE.read_text())
    except (OSError, ValueError):
        return {}


def save_best(best):
    try:
        BEST_FILE.write_text(json.dumps(best, indent=2))
    except OSError:
        pass


def diff_view(typed, target):
    """Colour each character of the target: green if typed right, red if wrong."""
    out = []
    for i, ch in enumerate(target):
        if i < len(typed):
            out.append(c(ch, GREEN) if typed[i] == ch else c(ch, RED))
        else:
            out.append(c(ch, GREY))
    return "".join(out)


def play(data, pack, mode, seconds):
    items = [x for v in data.values() for x in v] if pack == "all" else list(data[pack])
    random.shuffle(items)

    print(c(f"\n  CmdRush >_  pack: {pack}  mode: {mode}  time: {seconds}s", BOLD))
    if mode == "speed":
        print(c("  Type the command shown. Empty Enter skips. Ctrl+C quits.", GREY))
    else:
        print(c("  Type the command from its description. Empty Enter reveals it. Ctrl+C quits.", GREY))
    input(c("  Press Enter to start...", YELLOW))

    score = streak = best_streak = chars = 0
    missed = []
    start = time.monotonic()
    i = 0
    try:
        while True:
            left = seconds - (time.monotonic() - start)
            if left <= 0:
                break
            if i >= len(items):
                random.shuffle(items)
                i = 0
            item = items[i]
            print()
            print(f"  {c(f'[{int(left):>3}s]', GREY)} {c('score', GREY)} {score}  {c('streak', GREY)} {streak}")
            print("  " + c(item["desc"], YELLOW))
            if mode == "speed":
                print("  " + c(item["cmd"], BOLD))
            typed = input(c("  $ ", GREEN)).strip()

            if time.monotonic() - start > seconds:
                print(c("  Too late, time ran out!", RED))
                break
            if typed == item["cmd"]:
                pts = (2 if mode == "recall" else 1) + streak // 5
                score += pts
                chars += len(item["cmd"]) + 1
                streak += 1
                best_streak = max(best_streak, streak)
                print(c(f"  ✓ +{pts}", GREEN))
                i += 1
            elif not typed:
                print(c("  skipped → ", GREY) + item["cmd"])
                missed.append(item)
                streak = 0
                i += 1
            else:
                print("  ✗ " + diff_view(typed, item["cmd"]))
                if mode == "recall":
                    print(c("  answer: ", GREY) + item["cmd"])
                    missed.append(item)
                    i += 1
                streak = 0
    except (KeyboardInterrupt, EOFError):
        print(c("\n  Quit.", GREY))

    elapsed = max(time.monotonic() - start, 1)
    wpm = round(chars / 5 / (elapsed / 60))
    return score, wpm, best_streak, missed


def main():
    parser = argparse.ArgumentParser(description="Type real terminal commands against the clock.")
    parser.add_argument("-p", "--pack", default="all", help="command pack (default: all)")
    parser.add_argument("-m", "--mode", choices=["speed", "recall"], default="speed")
    parser.add_argument("-t", "--time", type=int, default=60, help="round length in seconds")
    parser.add_argument("--list", action="store_true", help="list packs and exit")
    args = parser.parse_args()

    data = load_data()
    if args.list:
        for name, cmds in data.items():
            print(f"{name:10} {len(cmds)} commands")
        return
    if args.pack != "all" and args.pack not in data:
        parser.error(f"unknown pack '{args.pack}'. Choose from: all, {', '.join(data)}")

    score, wpm, best_streak, missed = play(data, args.pack, args.mode, args.time)

    key = f"{args.pack}:{args.mode}:{args.time}"
    best = load_best()
    new_best = score > best.get(key, 0)
    if new_best:
        best[key] = score
        save_best(best)

    print()
    print(c("  ── Results ──", BOLD))
    print(f"  Score: {c(score, GREEN)}   WPM: {wpm}   Best streak: {best_streak}")
    print("  " + (c("New best score!", YELLOW) if new_best and score else f"Best: {best.get(key, 0)}"))
    if missed:
        print(c("\n  Commands to practice:", GREY))
        for m in missed[:8]:
            print(f"    {c(m['cmd'], BOLD)}  {c('- ' + m['desc'], GREY)}")
    print()


if __name__ == "__main__":
    main()
