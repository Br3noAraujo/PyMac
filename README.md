# 🛡️ PyMac

![PyMac Banner](https://i.imgur.com/KVHK8J5.png)

> **"Become untraceable. Mask your identity at the edge of the network."**

---

## 🚀 What is PyMac?

**PyMac** is a cross-platform, fast, and hacker-styled MAC address changer and restorer for Linux and macOS (with limited Windows support). It lets you spoof, randomize, restore, and have fun with your network identity — all from the terminal, with beautiful color and emoji feedback.

---

## ✨ Features

- 🔍 List all active network interfaces
- 🔎 Show the current MAC address
- 🎲 Generate and apply a random MAC address
- 🦄 Generate and apply a funny MAC address
- 📝 Log all actions to `pymac.log`
- 🔄 Restore your original MAC address (auto-saved per interface)
- ❌ Robust error and warning handling with intuitive emojis
- 💡 Colorful, hacker-friendly output
- 🛡️ Root/sudo check for safe operation

---

## ⚡ Installation

```sh
pip install -r requirements.txt
```

> Only [colorama](https://pypi.org/project/colorama/) is required. All other dependencies are standard Python 3 libraries.

---

## 🖥️ Usage

```sh
sudo ./pymac.py [options]
```

### Most Common Usage

#### 🎲 Randomize your MAC address
![Random MAC Example](https://i.imgur.com/KVHK8J5.png)

#### 🦄 Get a funny MAC address
![Funny MAC Example](https://i.imgur.com/V3fZSbo.png)

#### 🔄 Restore your original MAC address
![Restore MAC Example](https://i.imgur.com/qCytCyK.png)

---

## 🧰 Command Line Options

| Short | Long         | Description                                      |
|-------|--------------|--------------------------------------------------|
| -l    | --list       | List active network interfaces                   |
| -s    | --show       | Show current MAC address of the interface        |
| -r    | --random     | Generate and apply a random MAC address          |
| -c    | --set        | Set custom MAC address (e.g. -c "XX:XX:XX:XX:XX:XX") |
| -R    | --restore    | Restore original MAC address (auto, if known)    |
| -f    | --funny      | Generate and apply a funny MAC address           |
| -i    | --iface      | Target network interface                         |
| --log |              | Enable logging to pymac.log                      |
| -h    | --help       | Show help and usage examples                     |

---

## 💡 Philosophy

PyMac is built for hackers, sysadmins, and privacy enthusiasts who want:
- **Speed** and **clarity** in the terminal
- **No bloat**: only standard Python + colorama
- **Elite, Unix-inspired UX**: color, emoji, and raw practicality
- **No OOP, no web dependencies, no GUI**

---

## ⚠️ Notes

- Most features require **root/sudo** privileges.
- Windows support is limited (read-only MAC display).
- PyMac auto-saves your original MAC per interface in `~/.pymac_state.pkl`.

---

## 🧑‍💻 Author

Coded by [Br3noAraujo](https://github.com/Br3noAraujo)

---

## 📜 License

MIT License. Free for hackers, sysadmins, and privacy rebels everywhere. 