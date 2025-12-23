# GTA Vice City — HTML5 Port (DOS Zone)

Web-based port of GTA: Vice City running in browser via WebAssembly.

## Requirements

- Python 3.8+
- Dependencies from `requirements.txt`

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python server.py
```

Server starts at `http://localhost:8000`

## URL Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `lang` | `en`, `ru` | Game language |
| `cheats` | `1` | Enable cheat menu (F3) |

**Examples:**
- `http://localhost:8000/?lang=ru` — Russian version
- `http://localhost:8000/?lang=en&cheats=1` — English + cheats

## Project Structure

```
├── server.py           # FastAPI proxy server
├── requirements.txt    # Python dependencies
├── dist/               # Game client files
│   ├── index.html      # Main page
│   ├── game.js         # Game loader
│   ├── index.js        # Module loader
│   ├── GamepadEmulator.js  # Touch controls
│   ├── idbfs.js        # IndexedDB filesystem
│   ├── jsdos-cloud-sdk.js  # Cloud saves (DOS Zone)
│   └── modules/        # WASM modules
│       ├── runtime.js      # WASM runtime initialization
│       ├── loader.js       # Asset/package loading
│       ├── fs.js           # Virtual filesystem
│       ├── audio.js        # Audio system
│       ├── graphics.js     # Rendering pipeline
│       ├── events.js       # Input events handling
│       ├── fetch.js        # Network requests (Real-time asset streaming)
│       ├── syscalls.js     # System calls
│       ├── main.js         # Main entry point
│       ├── cheats.js       # Cheat engine (F3)
│       ├── asm_consts/     # Language-specific ASM constants
│       │   ├── en.js
│       │   └── ru.js
│       └── packages/       # Language-specific data packages
│           ├── en.js
│           └── ru.js
├── vcbr/               # Brotli-compressed game data (optional)
│   ├── vc-sky-en-v6.data.br
│   ├── vc-sky-en-v6.wasm.br
│   ├── vc-sky-ru-v6.data.br
│   └── vc-sky-ru-v6.wasm.br
└── vcsky/              # Additional assets (optional)
    ├── data/
    ├── audio/
    ├── models/
    └── anim/
```

## Features

- 🎮 Gamepad emulation for touch devices
- ☁️ Cloud saves via js-dos key
- 🌍 English/Russian language support
- 🔧 Built-in cheat engine (memory scanner, cheats)
- 📱 Mobile touch controls

## Controls (Touch)

Touch controls appear automatically on mobile devices. Virtual joysticks for movement and camera, context-sensitive action buttons.

## Cheats

Enable with `?cheats=1`, press **F3** to open menu:
- Memory scanner (find/edit values)
- All classic GTA VC cheats
- AirBreak (noclip mode)

## License

Based on open-source re3/reVC project. Not affiliated with Rockstar Games.

---

**Authors:** DOS Zone ([@specialist003](https://github.com/okhmanyuk-ev), [@caiiiycuk](https://www.youtube.com/caiiiycuk), [@SerGen](https://t.me/ser_var))

**Deobfuscated by**: [@Lolendor](https://github.com/Lolendor)

**Russian translation:** [GamesVoice](https://www.gamesvoice.ru/)
