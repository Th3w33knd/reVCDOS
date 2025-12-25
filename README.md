# GTA Vice City — HTML5 Port (DOS Zone)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/13GFRIxTwVbixv0Vup9MSVXnB4SLmA3G7?usp=sharing)

> **Fast Start:** Run the server in one click using Google Colab. Click the badge above, run the cell, and use the **"Launch Game"** button. The tunnel password will be copied automatically — just paste it on the page that opens.

Web-based port of GTA: Vice City running in browser via WebAssembly.

## Requirements

- Colab or Docker or Python 3.8+ or PHP 8.0+
- Dependencies from `requirements.txt`

## Quick Start

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Lolendor/reVCDOS.git
    cd reVCDOS
    ```

2. **Configure Assets** (Optional):

   By default, the project uses the **DOS Zone CDN**. For local hosting, download and place assets in [(see structure)](#project-structure):
    *   **Resources:** `vcsky/fetched/` (or `fetched-ru/`) — `data`, `audio`, `anim`, `models` folders.
    *   **Binaries:** `vcbr/` — `.wasm.br` and `.data.br` files for your chosen language.
4. **Launch the Application**:
   Choose one of the setup methods below:
   * **Docker** (Recommended for most users) — fast and isolated.
   * **PHP** — Simply upload the folder to your web server (FTP/Hosting).
   * **Manual Installation** — for development and customization.

## Setup & Running

### Option 1: Using Docker (Recommended)
The easiest way to get started is using Docker Compose:

```bash
VCSKY_CACHE=1 VCBR_CACHE=1 docker compose up -d --build
```

To configure server options via environment variables:

```bash
# Set port, enable auth and custom saves
IN_PORT=3000 AUTH_LOGIN=admin AUTH_PASSWORD=secret CUSTOM_SAVES=1 docker compose up -d --build
```

| Environment Variable | Description |
|---------------------|-------------|
| `OUT_HOST` | External host (default: 0.0.0.0) |
| `OUT_PORT` | External port (default: 8000) |
| `IN_PORT` | Internal container port (default: 8000) |
| `AUTH_LOGIN` | HTTP Basic Auth username |
| `AUTH_PASSWORD` | HTTP Basic Auth password |
| `CUSTOM_SAVES` | Enable local saves (set to `1`) |
| `VCSKY_LOCAL` | Serve vcsky from local directory (set to `1`) |
| `VCBR_LOCAL` | Serve vcbr from local directory (set to `1`) |
| `VCSKY_URL` | Custom vcsky proxy URL |
| `VCBR_URL` | Custom vcbr proxy URL |
| `VCSKY_CACHE` | Cache vcsky files locally while proxying (set to `1`) |
| `VCBR_CACHE` | Cache vcbr files locally while proxying (set to `1`) |

### Option 2: Local Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python server.py --vcsky_cache --vcbr_cache
```

Server starts at `http://localhost:8000`

### Option 3: Shared Hosting on PHP (No installation)

If you want to run the game from a hosted environment with `PHP 8.0` or above, just copy the contents of this repo to your desired hosting
By default the `index.php` and `.htaccess` will get the job done. 
## Server Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--port` | int | 8000 | Server port |
| `--custom_saves` | flag | disabled | Enable local save files (saves router) |
| `--login` | string | none | HTTP Basic Auth username |
| `--password` | string | none | HTTP Basic Auth password |
| `--vcsky_local` | flag | disabled | Serve vcsky from local `vcsky/` directory |
| `--vcbr_local` | flag | disabled | Serve vcbr from local `vcbr/` directory |
| `--vcsky_url` | string | `https://cdn.dos.zone/vcsky/` | Custom vcsky proxy URL |
| `--vcbr_url` | string | `https://br.cdn.dos.zone/vcsky/` | Custom vcbr proxy URL |
| `--vcsky_cache` | flag | disabled | Cache vcsky files locally while proxying |
| `--vcbr_cache` | flag | disabled | Cache vcbr files locally while proxying |

**Examples:**
```bash
# Start on custom port
python server.py --port 3000

# Enable local saves
python server.py --custom_saves

# Enable HTTP Basic Authentication
python server.py --login admin --password secret123

# Use local vcsky and vcbr files (fully offline mode)
python server.py --vcsky_local --vcbr_local

# Use custom proxy URLs
python server.py --vcsky_url https://my-cdn.example.com/vcsky/ --vcbr_url https://my-cdn.example.com/vcbr/

# Cache files locally while proxying (hybrid mode) (recommended)
python server.py --vcsky_cache --vcbr_cache

# All options combined
python server.py --port 3000 --custom_saves --login admin --password secret123 --vcsky_local --vcbr_local
```

> **Note:** HTTP Basic Auth is only enabled when both `--login` and `--password` are provided.

> **Note:** By default, vcsky and vcbr are proxied from DOS Zone CDN. Use `--vcsky_local` and `--vcbr_local` flags to serve files from local directories instead.

> **Note:** Use `--vcsky_cache` and `--vcbr_cache` to cache proxied files locally. Files are downloaded once and served from local storage on subsequent requests.

## URL Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `lang` | `en`, `ru` | Game language |
| `cheats` | `1` | Enable cheat menu (F3) |
| `request_original_game` | `1` | Request original game files before play |
| `fullscreen` | `0` | Disable auto-fullscreen |


**Examples:**
- `http://localhost:8000/?lang=ru` — Russian version
- `http://localhost:8000/?lang=en&cheats=1` — English + cheats

## Project Structure

```
├── server.py           # FastAPI proxy server
├── index.php           # php proxy server
├── .htaccess           # apache config for php
├── requirements.txt    # Python dependencies
├── additions/          # Server extensions
│   ├── auth.py         # HTTP Basic Auth middleware
│   ├── cache.py        # Proxy caching and brotli decompression
│   └── saves.py        # Local saves router
├── dist/               # Game client files
│   ├── index.html      # Main page
│   ├── game.js         # Game loader
│   ├── index.js        # Module loader
│   ├── GamepadEmulator.js  # Touch controls
│   ├── idbfs.js        # IndexedDB filesystem
│   ├── jsdos-cloud-sdk.js  # Cloud saves (DOS Zone)
│   ├── jsdos-cloud-sdk-local.js  # Local saves (--custom_saves)
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
└── vcsky/                 # Decompressed assets (optional)
    ├── fetched/           # English version files
    │   ├── data/
    │   ├── audio/
    │   ├── models/
    │   └── anim/
    └── fetched-ru/        # Russian version files
        ├── data/
        ├── audio/
        └── ...
```

## Features

- 🎮 Gamepad emulation for touch devices
- ☁️ Cloud saves via js-dos key
- 💾 Local saves (with `--custom_saves` flag)
- 🌍 English/Russian language support
- 🔧 Built-in cheat engine (memory scanner, cheats)
- 📱 Mobile touch controls

## Local Saves

When local saves are enabled (`--custom_saves` flag), enter any 5-character identifier in the "js-dos key" input field on the start page. This identifier will be used to store your saves in the `saves/` directory on the server.

Example: Enter `mykey` or `12345` — saves will be stored as `mykey_vcsky.saves` or `12345_vcsky.saves`.

## Controls (Touch)

Touch controls appear automatically on mobile devices. Virtual joysticks for movement and camera, context-sensitive action buttons.

## Cheats

Enable with `?cheats=1`, press **F3** to open menu:
- Memory scanner (find/edit values)
- All classic GTA VC cheats
- AirBreak (noclip mode)

## License

Do what you want. Not affiliated with Rockstar Games.

---

**Authors:** DOS Zone ([@specialist003](https://github.com/okhmanyuk-ev), [@caiiiycuk](https://www.youtube.com/caiiiycuk), [@SerGen](https://t.me/ser_var))

**Deobfuscated by**: [@Lolendor](https://github.com/Lolendor)

**Russian translation:** [GamesVoice](https://www.gamesvoice.ru/)

**Added by the community:**
* PHP Support by [Rohamgames](https://github.com/Rohamgames)

## Support [me](https://github.com/Lolendor)

If you find this project useful:

- **TON / USDT (TON)**  `UQAyBchGEKi9NnNQ3AKMQMuO-SGEhMIAKFAbkwwrsiOPj9Gy`
