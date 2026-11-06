<div align="center">

# CmdRush &gt;_

**Type real terminal commands against the clock. Get faster. Actually learn them.**

Linux · Git · Docker · Security, playable in your **browser** *or* your **terminal**.

[**▶ Play in the browser**](https://y4sh-0day.github.io/Top/) · [Terminal version](#-play-in-your-terminal) · [Add commands](#-contributing)

</div>

---

Most typing games make you type random English words. **CmdRush makes you type the commands you use every day**, so your practice makes you faster at real work.

## ✨ Features

- ⚡ **Speed mode**: the command is shown. Type it as fast as you can.
- 🧠 **Recall mode**: you see only what the command *does*. Type it from memory (worth double points).
- 📦 **4 packs, 69 real commands**: `linux`, `git`, `docker`, `security`, or all of them mixed.
- 🔥 Streak bonuses, WPM, accuracy and a saved **best score** for each pack, mode and round length.
- 📝 A **"commands to practice"** list after each round, showing the ones you skipped or missed.
- 🌐 **Web version**: one HTML file, no build step, no tracking.
- 💻 **CLI version**: one Python file, zero dependencies.

## 🌐 Play in the browser

Play the live version at **https://y4sh-0day.github.io/Top/**

Or run it locally:

```bash
git clone https://github.com/y4sh-0day/Top.git
cd Top
python3 -m http.server 8000
# open http://localhost:8000
```

**Keys:** `Enter` submits · `Tab` skips (in Recall mode it reveals the answer) · `Esc` returns to the menu

## ⌨️ Typing trainer (Mac and phone)

Learn to **touch type** at **https://y4sh-0day.github.io/Top/typing.html**

- A Mac keyboard and two hands show **which finger to use** for every key
- A guide to where to put your hands (home row, F and J bumps, thumbs, shift)
- Lessons: Home row → Top row → All letters → Capitals and punctuation → Numbers
- Live WPM and accuracy, best scores, and a list of your weakest keys
- On a **phone** it switches to thumb-typing tips and your phone's keyboard

## 💻 Play in your terminal

```bash
python3 cli/cmdrush.py                    # all packs, speed mode, 60 seconds
python3 cli/cmdrush.py -p git -m recall   # Git pack, from memory
python3 cli/cmdrush.py -p docker -t 30    # 30-second Docker round
python3 cli/cmdrush.py --list             # show packs
```

Best scores are saved in `~/.cmdrush.json`. Set `NO_COLOR=1` to turn colours off.

## 🧮 Scoring

| Action | Points |
|---|---|
| Correct command (Speed) | +1 |
| Correct command (Recall) | +2 |
| Streak bonus | +1 for every 5 correct in a row |
| Revealed or skipped | 0, and the streak resets |

## 🤝 Contributing

All commands live in [`commands.json`](commands.json), which both versions use. To add a command:

```json
{"cmd": "git rebase -i HEAD~3", "desc": "Interactively edit your last 3 commits"}
```

New packs are welcome too: `kubernetes`, `python`, `npm`, `vim`, `powershell` and more. Add a new key to `commands.json` and it shows up in both versions automatically. Open a pull request!

## ⭐ Like it?

If CmdRush helped you remember a command, **give it a star**. It helps other people find it.

## License

[MIT](LICENSE)
