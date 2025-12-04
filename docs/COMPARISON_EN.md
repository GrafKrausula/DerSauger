# yt-dlp Browser Extensions - Complete Market Analysis

> Last updated: December 2025

This document provides a comprehensive analysis of all known browser extensions that use yt-dlp or youtube-dl as their backend for downloading videos from websites.

---

## Table of Contents

1. [Overview](#overview)
2. [Complete Extension List](#complete-extension-list)
3. [Detailed Extension Profiles](#detailed-extension-profiles)
4. [Feature Comparison Matrix](#feature-comparison-matrix)
5. [Architecture Comparison](#architecture-comparison)
6. [DerSauger's Unique Selling Points](#dersaugers-unique-selling-points)
7. [Feature Ideas from Competitors](#feature-ideas-from-competitors)

---

## Overview

As of December 2025, there are approximately **14 browser extensions** that integrate with yt-dlp or youtube-dl for video downloading. These extensions vary significantly in:

- **Architecture**: Native Messaging vs. Local Server vs. Command-only
- **Browser Support**: Chrome, Firefox, or both
- **Platform Support**: Windows, Linux, macOS
- **Feature Set**: Basic downloading to full conversion pipelines

### Architecture Types

| Type | Description | Examples |
|------|-------------|----------|
| **Native Messaging** | Browser communicates directly with a local native application | DerSauger, Grabby, mpvnet |
| **Local Server** | Extension communicates with a locally running server (Node.js, Python, etc.) | Tetsuo-DL, metube-extension |
| **Command Generator** | Only generates yt-dlp commands for manual execution | yt-dlp-generator |

---

## Complete Extension List

### Active Extensions (2024-2025)

| # | Name | Repository | Stars | Last Update | Status |
|---|------|------------|-------|-------------|--------|
| 1 | **DerSauger** | [GrafKrausula/DerSauger](https://github.com/GrafKrausula/DerSauger) | - | Active | ✅ Active |
| 2 | **Grabby** | [pouriap/Grabby](https://github.com/pouriap/Grabby) | 47 | Mar 2024 | ✅ Active |
| 3 | **mpvnet** | [MasterDevX/mpvnet](https://github.com/MasterDevX/mpvnet) | 27 | Sep 2023 | ✅ Active |
| 4 | **metube-browser-extension** | [Rpsl/metube-browser-extension](https://github.com/Rpsl/metube-browser-extension) | 22 | Apr 2024 | ✅ Active |
| 5 | **Tetsuo-DL** | [tetsuo-ai/Tetsuo-DL](https://github.com/tetsuo-ai/Tetsuo-DL) | 6 | Mar 2025 | ✅ Active |
| 6 | **yt-dlp-generator** | [xdev23/yt-dlp-generator](https://github.com/xdev23/yt-dlp-generator) | 4 | Jun 2025 | ✅ Active |
| 7 | **youtube-downloader-yt-dlp-local** | [CosmiX-6/youtube-downloader-yt-dlp-local](https://github.com/CosmiX-6/youtube-downloader-yt-dlp-local) | 1 | Jul 2025 | ✅ Active |
| 8 | **yt-dlp-extension** (Jeff-Soares) | [Jeff-Soares/yt-dlp-extension](https://github.com/Jeff-Soares/yt-dlp-extension) | 0 | Mar 2025 | ✅ Active |
| 9 | **yt-dlp-firefox-extension** | [px86/yt-dlp-firefox-extension](https://github.com/px86/yt-dlp-firefox-extension) | 0 | Apr 2025 | ✅ Active |
| 10 | **url-saver** | [mduncs/url-saver](https://github.com/mduncs/url-saver) | 0 | Nov 2025 | ✅ Active |
| 11 | **Playpocket** | [SANTHOSH-SACHIN/Playpocket](https://github.com/SANTHOSH-SACHIN/Playpocket) | 0 | Apr 2025 | ✅ Active |
| 12 | **browser.yt-dlp_to_kodi** | [aportela/browser.yt-dlp_to_kodi](https://github.com/aportela/browser.yt-dlp_to_kodi) | 0 | Jul 2025 | ✅ Active |

### Legacy/Inactive Extensions

| # | Name | Repository | Stars | Last Update | Status |
|---|------|------------|-------|-------------|--------|
| 13 | **TokkiDownload** | [IUCPROD/TokkiDownload](https://github.com/IUCPROD/TokkiDownload) | 1 | Sep 2020 | ⚠️ Inactive |
| 14 | **vid2mp3** | [le-mon/vid2mp3](https://github.com/le-mon/vid2mp3) | 2 | Jun 2017 | ⚠️ Inactive |
| 15 | **vidclip** | [TempusWare/vidclip](https://github.com/TempusWare/vidclip) | 0 | Jun 2024 | 📦 Archived |
| 16 | **youtube-dl_extensions** | [Bootz/youtube-dl_extensions](https://github.com/Bootz/youtube-dl_extensions) | 0 | Apr 2013 | ⚠️ Inactive |

---

## Detailed Extension Profiles

### 1. DerSauger

> **Repository**: [github.com/GrafKrausula/DerSauger](https://github.com/GrafKrausula/DerSauger)

**Description**: A browser extension for Chrome and Firefox that downloads videos using yt-dlp via Native Messaging and automatically converts them to various audio formats (WAV, MP3, etc.).

**Key Features**:
- ✅ Chrome and Firefox support
- ✅ Native Messaging architecture (no server required)
- ✅ Automatic audio conversion (WAV, MP3, etc.)
- ✅ FFmpeg integration for format conversion
- ✅ yt-dlp auto-update functionality
- ✅ Professional Windows NSIS installer
- ✅ Configurable download and convert paths

**Technical Stack**:
- Frontend: JavaScript (Browser Extension)
- Backend: Python (Native Messaging Host)
- Conversion: FFmpeg, Python scripts
- Installer: NSIS

---

### 2. Grabby

> **Repository**: [github.com/pouriap/Grabby](https://github.com/pouriap/Grabby)

**Description**: A spiritual successor to the legendary FlashGot addon. Grabby allows downloading files and media from websites using external download managers and yt-dlp.

**Key Features**:
- ✅ Firefox primary support (other browsers via wiki)
- ✅ Override Firefox's download dialog
- ✅ Download videos from video sharing sites
- ✅ YouTube playlist support
- ✅ Link grabbing and filtering
- ✅ Support for 15+ download managers
- ✅ Download history per tab

**Technical Stack**:
- Frontend: TypeScript/JavaScript (WebExtension)
- Backend: Native Application (Grabby Toolkit)
- Includes: yt-dlp.exe, ffmpeg.exe, grabby_flashgot.exe

**Supported Download Managers**:
- Internet Download Manager
- Free Download Manager
- JDownloader
- Xtreme Download Manager
- And 11+ more

**Links**:
- [Firefox Add-on](https://addons.mozilla.org/en-US/firefox/addon/grabby/)
- [Grabby Toolkit Releases](https://github.com/pouriap/Grabby-Toolkit/releases/latest)
- [Discord Server](https://discord.gg/Xu6tHt8uXs)

---

### 3. mpvnet

> **Repository**: [github.com/MasterDevX/mpvnet](https://github.com/MasterDevX/mpvnet)

**Description**: A Chrome/Firefox extension for playing and downloading media with mpv player and yt-dlp. Focused on Linux users.

**Key Features**:
- ✅ Chrome and Firefox support
- ✅ Native Messaging architecture
- ✅ Play video/audio directly in mpv player
- ✅ Video/audio downloading
- ✅ Video resolution limit settings
- ✅ Supports [all yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

**Technical Stack**:
- Frontend: JavaScript, CSS, HTML
- Backend: Python (Native Messaging)
- Player: mpv
- Build: autoconf/automake

**Platform**: Linux-focused (requires autotools)

**Links**:
- [Firefox Release](https://github.com/MasterDevX/mpvnet/releases/tag/v1.0-firefox)
- [Chrome Release](https://github.com/MasterDevX/mpvnet/releases/tag/v1.0-chrome)

---

### 4. metube-browser-extension

> **Repository**: [github.com/Rpsl/metube-browser-extension](https://github.com/Rpsl/metube-browser-extension)

**Description**: Browser extension for sending YouTube video links to a self-hosted MeTube server via context menu.

**Key Features**:
- ✅ Chrome extension
- ✅ Context menu integration
- ✅ Sends links to MeTube server
- ✅ Works with self-hosted MeTube instances

**Architecture**: HTTP communication to MeTube server (not standalone)

**Requires**: [MeTube](https://github.com/alexta69/metube) self-hosted server

---

### 5. Tetsuo-DL

> **Repository**: [github.com/tetsuo-ai/Tetsuo-DL](https://github.com/tetsuo-ai/Tetsuo-DL)

**Description**: A feature-rich browser extension for downloading YouTube videos with a modern interface and advanced options.

**Key Features**:
- ✅ Multiple quality options
- ✅ Custom filenames
- ✅ Download queue
- ✅ Download history
- ✅ Custom download locations
- ✅ Dark mode
- ✅ Progress tracking with time estimates
- ✅ yt-dlp auto-updates
- ✅ Keyboard shortcuts (Ctrl+Shift+Y)

**Technical Stack**:
- Frontend: JavaScript, HTML, CSS
- Backend: Node.js server (port 17171)
- Downloader: yt-dlp

**Platform**: Windows 7+ (Chrome/Edge)

**Installation**:
1. Run `install-win.bat` as Administrator
2. Load unpacked extension in Chrome

---

### 6. yt-dlp-generator

> **Repository**: [github.com/xdev23/yt-dlp-generator](https://github.com/xdev23/yt-dlp-generator)

**Description**: Chrome extension that generates yt-dlp commands and copies them to clipboard. Does not perform actual downloads.

**Key Features**:
- ✅ Generates yt-dlp commands
- ✅ Copies commands to clipboard
- ✅ Chrome extension

**Use Case**: For users who prefer to run yt-dlp manually in terminal

---

### 7. yt-dlp-firefox-extension (px86)

> **Repository**: [github.com/px86/yt-dlp-firefox-extension](https://github.com/px86/yt-dlp-firefox-extension)

**Description**: A Firefox extension for downloading video/audio using yt-dlp with native messaging API.

**Key Features**:
- ✅ Firefox support
- ✅ Native Messaging architecture
- ✅ Video and audio download
- ✅ Configurable via config.ini

**Technical Stack**:
- Frontend: JavaScript, HTML
- Backend: Python (Native Messaging)
- Config: INI file

**Platform**: Linux (shell script installer)

---

### 8. url-saver

> **Repository**: [github.com/mduncs/url-saver](https://github.com/mduncs/url-saver)

**Description**: Browser extension + server for archiving media from web using multiple tools.

**Key Features**:
- ✅ yt-dlp integration
- ✅ gallery-dl integration
- ✅ dezoomify-rs integration
- ✅ Media archiving focus

---

## Feature Comparison Matrix

### Browser & Platform Support

| Extension | Chrome | Firefox | Windows | Linux | macOS |
|-----------|:------:|:-------:|:-------:|:-----:|:-----:|
| **DerSauger** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Grabby** | ⚠️ | ✅ | ✅ | ✅ | ❌ |
| **mpvnet** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Tetsuo-DL** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **metube-extension** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **yt-dlp-generator** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **px86 Extension** | ❌ | ✅ | ❌ | ✅ | ❌ |

### Architecture

| Extension | Native Messaging | Local Server | Serverless | Self-hosted |
|-----------|:----------------:|:------------:|:----------:|:-----------:|
| **DerSauger** | ✅ | ❌ | ✅ | ❌ |
| **Grabby** | ✅ | ❌ | ✅ | ❌ |
| **mpvnet** | ✅ | ❌ | ✅ | ❌ |
| **Tetsuo-DL** | ❌ | ✅ | ❌ | ❌ |
| **metube-extension** | ❌ | ❌ | ❌ | ✅ |
| **yt-dlp-generator** | ❌ | ❌ | ✅ | ❌ |
| **px86 Extension** | ✅ | ❌ | ✅ | ❌ |

### Download Features

| Extension | Video DL | Audio DL | Quality Select | Playlist | Queue | History |
|-----------|:--------:|:--------:|:--------------:|:--------:|:-----:|:-------:|
| **DerSauger** | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Grabby** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **mpvnet** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Tetsuo-DL** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **metube-extension** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **yt-dlp-generator** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **px86 Extension** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

### Conversion & Processing

| Extension | Auto-Convert | WAV Output | MP3 Output | FFmpeg | yt-dlp Update |
|-----------|:------------:|:----------:|:----------:|:------:|:-------------:|
| **DerSauger** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Grabby** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **mpvnet** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Tetsuo-DL** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **metube-extension** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **yt-dlp-generator** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **px86 Extension** | ❌ | ❌ | ❌ | ❌ | ❌ |

### Installation & UX

| Extension | Installer | Dark Mode | mpv Integration | DL Manager Support |
|-----------|:---------:|:---------:|:---------------:|:------------------:|
| **DerSauger** | ✅ NSIS | ❌ | ❌ | ❌ |
| **Grabby** | ✅ Toolkit | ❌ | ❌ | ✅ (15+) |
| **mpvnet** | ❌ | ❌ | ✅ | ❌ |
| **Tetsuo-DL** | ✅ BAT | ✅ | ❌ | ❌ |
| **metube-extension** | ❌ | ❌ | ❌ | ❌ |
| **yt-dlp-generator** | ❌ | ❌ | ❌ | ❌ |
| **px86 Extension** | ❌ | ❌ | ❌ | ❌ |

---

## Architecture Comparison

### Native Messaging (DerSauger, Grabby, mpvnet, px86)

```
┌─────────────────┐     Native Messaging      ┌──────────────────┐
│ Browser         │ ◄─────────────────────────► Native Host      │
│ Extension       │     (JSON messages)       │ (Python/exe)     │
└─────────────────┘                           └────────┬─────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │ yt-dlp + FFmpeg  │
                                              └──────────────────┘
```

**Pros**:
- No server required
- Direct communication
- More secure (no open ports)

**Cons**:
- Platform-specific installation
- Native host must be registered

### Local Server (Tetsuo-DL)

```
┌─────────────────┐     HTTP (localhost)      ┌──────────────────┐
│ Browser         │ ◄─────────────────────────► Node.js Server   │
│ Extension       │     (port 17171)          │                  │
└─────────────────┘                           └────────┬─────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │ yt-dlp + FFmpeg  │
                                              └──────────────────┘
```

**Pros**:
- Easier to develop
- Cross-browser compatible API

**Cons**:
- Server must run in background
- Open port (potential security concern)

### Self-Hosted Server (metube-extension)

```
┌─────────────────┐     HTTP (network)        ┌──────────────────┐
│ Browser         │ ◄─────────────────────────► MeTube Server    │
│ Extension       │                           │ (Docker)         │
└─────────────────┘                           └────────┬─────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │ yt-dlp + FFmpeg  │
                                              └──────────────────┘
```

**Pros**:
- Can run on separate machine
- Web UI available
- Multiple users

**Cons**:
- Requires server setup
- More complex infrastructure

---

## DerSauger's Unique Selling Points

Based on the comprehensive analysis above, DerSauger offers a unique combination of features not found in any other extension:

### 1. Only Extension with Automatic WAV Conversion

**DerSauger is the only browser extension that automatically converts downloaded media to WAV format.** This is essential for:
- Audio production workflows
- Lossless audio archival
- Professional audio editing

### 2. Chrome + Firefox + Native Messaging + Windows

| Combination | DerSauger | Others |
|-------------|:---------:|:------:|
| Chrome + Firefox | ✅ | mpvnet (Linux only) |
| Native Messaging | ✅ | Grabby (Firefox primary) |
| Windows Support | ✅ | mpvnet ❌ |
| **All Combined** | ✅ | ❌ |

### 3. Serverless Full-Featured Solution

Unlike Tetsuo-DL (requires Node.js server) or metube-extension (requires Docker), DerSauger:
- Requires no background server
- No open ports
- No Docker setup
- Just install and use

### 4. Professional Windows Installer

DerSauger includes a professional NSIS installer that:
- Sets up Python virtual environments
- Registers Native Messaging hosts
- Installs yt-dlp and FFmpeg
- Creates proper uninstaller

### 5. Built-in yt-dlp Auto-Update

Only DerSauger and Tetsuo-DL offer automatic yt-dlp updates. Combined with Native Messaging architecture, this makes DerSauger unique.

---

## Feature Ideas from Competitors

Based on this analysis, the following features from competitors could enhance DerSauger:

### From Tetsuo-DL

| Feature | Description | Priority |
|---------|-------------|----------|
| Download Queue | Queue multiple downloads | Medium |
| Download History | Track previous downloads | Medium |
| Dark Mode | Modern dark theme | Low |
| Progress Tracking | Show download progress with ETA | Medium |
| Keyboard Shortcuts | Quick access hotkeys | Low |

### From Grabby

| Feature | Description | Priority |
|---------|-------------|----------|
| Quality Selection | Choose video/audio quality before download | High |
| Link Grabber | Grab and filter all links on a page | Medium |
| Download Manager Integration | Support external download managers | Low |

### From mpvnet

| Feature | Description | Priority |
|---------|-------------|----------|
| mpv Player Integration | Play directly in mpv | Low |
| Linux Support | Cross-platform support | Medium |

---

## Conclusion

DerSauger occupies a unique position in the yt-dlp browser extension ecosystem by combining:

1. **Cross-browser support** (Chrome + Firefox)
2. **Native Messaging architecture** (no server required)
3. **Automatic format conversion** (unique WAV support)
4. **Professional Windows installer**
5. **yt-dlp auto-updates**

The main competitors are:
- **Grabby**: More features but Firefox-focused and more complex
- **mpvnet**: Similar architecture but Linux-only
- **Tetsuo-DL**: Better UI/UX but requires local server

---

## Links & Resources

### DerSauger
- Repository: https://github.com/GrafKrausula/DerSauger

### Competitors
- Grabby: https://github.com/pouriap/Grabby
- mpvnet: https://github.com/MasterDevX/mpvnet
- Tetsuo-DL: https://github.com/tetsuo-ai/Tetsuo-DL
- metube-extension: https://github.com/Rpsl/metube-browser-extension
- yt-dlp-generator: https://github.com/xdev23/yt-dlp-generator
- px86 Extension: https://github.com/px86/yt-dlp-firefox-extension
- url-saver: https://github.com/mduncs/url-saver
- youtube-downloader-yt-dlp-local: https://github.com/CosmiX-6/youtube-downloader-yt-dlp-local

### Related Projects
- yt-dlp: https://github.com/yt-dlp/yt-dlp
- MeTube: https://github.com/alexta69/metube
- FFmpeg: https://ffmpeg.org/
