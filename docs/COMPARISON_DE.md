# yt-dlp Browser Extensions - Vollständige Marktanalyse

> Zuletzt aktualisiert: Dezember 2025

Dieses Dokument bietet eine umfassende Analyse aller bekannten Browser-Extensions, die yt-dlp oder youtube-dl als Backend für das Herunterladen von Videos verwenden.

---

## Inhaltsverzeichnis

1. [Übersicht](#übersicht)
2. [Vollständige Extension-Liste](#vollständige-extension-liste)
3. [Detaillierte Extension-Profile](#detaillierte-extension-profile)
4. [Feature-Vergleichsmatrix](#feature-vergleichsmatrix)
5. [Architektur-Vergleich](#architektur-vergleich)
6. [DerSaugers Alleinstellungsmerkmale](#dersaugers-alleinstellungsmerkmale)
7. [Feature-Ideen von Konkurrenten](#feature-ideen-von-konkurrenten)

---

## Übersicht

Stand Dezember 2025 gibt es ungefähr **14 Browser-Extensions**, die mit yt-dlp oder youtube-dl für Video-Downloads integrieren. Diese Extensions unterscheiden sich erheblich in:

- **Architektur**: Native Messaging vs. Lokaler Server vs. Nur-Befehle
- **Browser-Unterstützung**: Chrome, Firefox oder beide
- **Plattform-Unterstützung**: Windows, Linux, macOS
- **Funktionsumfang**: Einfache Downloads bis hin zu vollständigen Konvertierungs-Pipelines

### Architektur-Typen

| Typ | Beschreibung | Beispiele |
|-----|--------------|-----------|
| **Native Messaging** | Browser kommuniziert direkt mit einer lokalen nativen Anwendung | DerSauger, Grabby, mpvnet |
| **Lokaler Server** | Extension kommuniziert mit einem lokal laufenden Server (Node.js, Python, etc.) | Tetsuo-DL, metube-extension |
| **Befehls-Generator** | Generiert nur yt-dlp-Befehle zur manuellen Ausführung | yt-dlp-generator |

---

## Vollständige Extension-Liste

### Aktive Extensions (2024-2025)

| # | Name | Repository | Sterne | Letztes Update | Status |
|---|------|------------|--------|----------------|--------|
| 1 | **DerSauger** | [GrafKrausula/DerSauger](https://github.com/GrafKrausula/DerSauger) | - | Aktiv | ✅ Aktiv |
| 2 | **Grabby** | [pouriap/Grabby](https://github.com/pouriap/Grabby) | 47 | Mär 2024 | ✅ Aktiv |
| 3 | **mpvnet** | [MasterDevX/mpvnet](https://github.com/MasterDevX/mpvnet) | 27 | Sep 2023 | ✅ Aktiv |
| 4 | **metube-browser-extension** | [Rpsl/metube-browser-extension](https://github.com/Rpsl/metube-browser-extension) | 22 | Apr 2024 | ✅ Aktiv |
| 5 | **Tetsuo-DL** | [tetsuo-ai/Tetsuo-DL](https://github.com/tetsuo-ai/Tetsuo-DL) | 6 | Mär 2025 | ✅ Aktiv |
| 6 | **yt-dlp-generator** | [xdev23/yt-dlp-generator](https://github.com/xdev23/yt-dlp-generator) | 4 | Jun 2025 | ✅ Aktiv |
| 7 | **youtube-downloader-yt-dlp-local** | [CosmiX-6/youtube-downloader-yt-dlp-local](https://github.com/CosmiX-6/youtube-downloader-yt-dlp-local) | 1 | Jul 2025 | ✅ Aktiv |
| 8 | **yt-dlp-extension** (Jeff-Soares) | [Jeff-Soares/yt-dlp-extension](https://github.com/Jeff-Soares/yt-dlp-extension) | 0 | Mär 2025 | ✅ Aktiv |
| 9 | **yt-dlp-firefox-extension** | [px86/yt-dlp-firefox-extension](https://github.com/px86/yt-dlp-firefox-extension) | 0 | Apr 2025 | ✅ Aktiv |
| 10 | **url-saver** | [mduncs/url-saver](https://github.com/mduncs/url-saver) | 0 | Nov 2025 | ✅ Aktiv |
| 11 | **Playpocket** | [SANTHOSH-SACHIN/Playpocket](https://github.com/SANTHOSH-SACHIN/Playpocket) | 0 | Apr 2025 | ✅ Aktiv |
| 12 | **browser.yt-dlp_to_kodi** | [aportela/browser.yt-dlp_to_kodi](https://github.com/aportela/browser.yt-dlp_to_kodi) | 0 | Jul 2025 | ✅ Aktiv |

### Legacy/Inaktive Extensions

| # | Name | Repository | Sterne | Letztes Update | Status |
|---|------|------------|--------|----------------|--------|
| 13 | **TokkiDownload** | [IUCPROD/TokkiDownload](https://github.com/IUCPROD/TokkiDownload) | 1 | Sep 2020 | ⚠️ Inaktiv |
| 14 | **vid2mp3** | [le-mon/vid2mp3](https://github.com/le-mon/vid2mp3) | 2 | Jun 2017 | ⚠️ Inaktiv |
| 15 | **vidclip** | [TempusWare/vidclip](https://github.com/TempusWare/vidclip) | 0 | Jun 2024 | 📦 Archiviert |
| 16 | **youtube-dl_extensions** | [Bootz/youtube-dl_extensions](https://github.com/Bootz/youtube-dl_extensions) | 0 | Apr 2013 | ⚠️ Inaktiv |

---

## Detaillierte Extension-Profile

### 1. DerSauger

> **Repository**: [github.com/GrafKrausula/DerSauger](https://github.com/GrafKrausula/DerSauger)

**Beschreibung**: Eine Browser-Extension für Chrome und Firefox, die Videos mit yt-dlp über Native Messaging herunterlädt und sie automatisch in verschiedene Audio-Formate (WAV, MP3, etc.) konvertiert.

**Hauptfunktionen**:
- ✅ Chrome und Firefox Unterstützung
- ✅ Native Messaging Architektur (kein Server erforderlich)
- ✅ Automatische Audio-Konvertierung (WAV, MP3, etc.)
- ✅ FFmpeg-Integration für Format-Konvertierung
- ✅ yt-dlp Auto-Update Funktionalität
- ✅ Professioneller Windows NSIS Installer
- ✅ Konfigurierbare Download- und Konvertierungspfade

**Technischer Stack**:
- Frontend: JavaScript (Browser Extension)
- Backend: Python (Native Messaging Host)
- Konvertierung: FFmpeg, Python-Skripte
- Installer: NSIS

---

### 2. Grabby

> **Repository**: [github.com/pouriap/Grabby](https://github.com/pouriap/Grabby)

**Beschreibung**: Ein geistiger Nachfolger des legendären FlashGot-Addons. Grabby ermöglicht das Herunterladen von Dateien und Medien von Websites mit externen Download-Managern und yt-dlp.

**Hauptfunktionen**:
- ✅ Firefox als primäre Unterstützung (andere Browser via Wiki)
- ✅ Überschreibt Firefox's Download-Dialog
- ✅ Videos von Video-Sharing-Seiten herunterladen
- ✅ YouTube Playlist-Unterstützung
- ✅ Link-Erfassung und -Filterung
- ✅ Unterstützung für 15+ Download-Manager
- ✅ Download-Verlauf pro Tab

**Technischer Stack**:
- Frontend: TypeScript/JavaScript (WebExtension)
- Backend: Native Application (Grabby Toolkit)
- Enthält: yt-dlp.exe, ffmpeg.exe, grabby_flashgot.exe

**Unterstützte Download-Manager**:
- Internet Download Manager
- Free Download Manager
- JDownloader
- Xtreme Download Manager
- Und 11+ weitere

**Links**:
- [Firefox Add-on](https://addons.mozilla.org/en-US/firefox/addon/grabby/)
- [Grabby Toolkit Releases](https://github.com/pouriap/Grabby-Toolkit/releases/latest)
- [Discord Server](https://discord.gg/Xu6tHt8uXs)

---

### 3. mpvnet

> **Repository**: [github.com/MasterDevX/mpvnet](https://github.com/MasterDevX/mpvnet)

**Beschreibung**: Eine Chrome/Firefox-Extension zum Abspielen und Herunterladen von Medien mit mpv-Player und yt-dlp. Fokussiert auf Linux-Nutzer.

**Hauptfunktionen**:
- ✅ Chrome und Firefox Unterstützung
- ✅ Native Messaging Architektur
- ✅ Video/Audio direkt in mpv abspielen
- ✅ Video/Audio Download
- ✅ Video-Auflösungslimit-Einstellungen
- ✅ Unterstützt [alle yt-dlp unterstützten Seiten](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

**Technischer Stack**:
- Frontend: JavaScript, CSS, HTML
- Backend: Python (Native Messaging)
- Player: mpv
- Build: autoconf/automake

**Plattform**: Linux-fokussiert (benötigt autotools)

**Links**:
- [Firefox Release](https://github.com/MasterDevX/mpvnet/releases/tag/v1.0-firefox)
- [Chrome Release](https://github.com/MasterDevX/mpvnet/releases/tag/v1.0-chrome)

---

### 4. metube-browser-extension

> **Repository**: [github.com/Rpsl/metube-browser-extension](https://github.com/Rpsl/metube-browser-extension)

**Beschreibung**: Browser-Extension zum Senden von YouTube-Video-Links an einen selbst gehosteten MeTube-Server über das Kontextmenü.

**Hauptfunktionen**:
- ✅ Chrome Extension
- ✅ Kontextmenü-Integration
- ✅ Sendet Links an MeTube-Server
- ✅ Funktioniert mit selbst gehosteten MeTube-Instanzen

**Architektur**: HTTP-Kommunikation zum MeTube-Server (nicht eigenständig)

**Benötigt**: [MeTube](https://github.com/alexta69/metube) selbst gehosteter Server

---

### 5. Tetsuo-DL

> **Repository**: [github.com/tetsuo-ai/Tetsuo-DL](https://github.com/tetsuo-ai/Tetsuo-DL)

**Beschreibung**: Eine funktionsreiche Browser-Extension zum Herunterladen von YouTube-Videos mit einer modernen Oberfläche und erweiterten Optionen.

**Hauptfunktionen**:
- ✅ Mehrere Qualitätsoptionen
- ✅ Benutzerdefinierte Dateinamen
- ✅ Download-Warteschlange
- ✅ Download-Verlauf
- ✅ Benutzerdefinierte Download-Speicherorte
- ✅ Dark Mode
- ✅ Fortschrittsverfolgung mit Zeitschätzungen
- ✅ yt-dlp Auto-Updates
- ✅ Tastaturkürzel (Strg+Umschalt+Y)

**Technischer Stack**:
- Frontend: JavaScript, HTML, CSS
- Backend: Node.js Server (Port 17171)
- Downloader: yt-dlp

**Plattform**: Windows 7+ (Chrome/Edge)

**Installation**:
1. `install-win.bat` als Administrator ausführen
2. Entpackte Extension in Chrome laden

---

### 6. yt-dlp-generator

> **Repository**: [github.com/xdev23/yt-dlp-generator](https://github.com/xdev23/yt-dlp-generator)

**Beschreibung**: Chrome-Extension, die yt-dlp-Befehle generiert und in die Zwischenablage kopiert. Führt keine tatsächlichen Downloads durch.

**Hauptfunktionen**:
- ✅ Generiert yt-dlp-Befehle
- ✅ Kopiert Befehle in die Zwischenablage
- ✅ Chrome Extension

**Anwendungsfall**: Für Nutzer, die yt-dlp lieber manuell im Terminal ausführen

---

### 7. yt-dlp-firefox-extension (px86)

> **Repository**: [github.com/px86/yt-dlp-firefox-extension](https://github.com/px86/yt-dlp-firefox-extension)

**Beschreibung**: Eine Firefox-Extension zum Herunterladen von Video/Audio mit yt-dlp über die Native Messaging API.

**Hauptfunktionen**:
- ✅ Firefox Unterstützung
- ✅ Native Messaging Architektur
- ✅ Video und Audio Download
- ✅ Konfigurierbar über config.ini

**Technischer Stack**:
- Frontend: JavaScript, HTML
- Backend: Python (Native Messaging)
- Konfiguration: INI-Datei

**Plattform**: Linux (Shell-Skript Installer)

---

### 8. url-saver

> **Repository**: [github.com/mduncs/url-saver](https://github.com/mduncs/url-saver)

**Beschreibung**: Browser-Extension + Server zum Archivieren von Medien aus dem Web mit mehreren Tools.

**Hauptfunktionen**:
- ✅ yt-dlp Integration
- ✅ gallery-dl Integration
- ✅ dezoomify-rs Integration
- ✅ Fokus auf Medien-Archivierung

---

## Feature-Vergleichsmatrix

### Browser & Plattform-Unterstützung

| Extension | Chrome | Firefox | Windows | Linux | macOS |
|-----------|:------:|:-------:|:-------:|:-----:|:-----:|
| **DerSauger** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Grabby** | ⚠️ | ✅ | ✅ | ✅ | ❌ |
| **mpvnet** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Tetsuo-DL** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **metube-extension** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **yt-dlp-generator** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **px86 Extension** | ❌ | ✅ | ❌ | ✅ | ❌ |

### Architektur

| Extension | Native Messaging | Lokaler Server | Serverlos | Self-hosted |
|-----------|:----------------:|:--------------:|:---------:|:-----------:|
| **DerSauger** | ✅ | ❌ | ✅ | ❌ |
| **Grabby** | ✅ | ❌ | ✅ | ❌ |
| **mpvnet** | ✅ | ❌ | ✅ | ❌ |
| **Tetsuo-DL** | ❌ | ✅ | ❌ | ❌ |
| **metube-extension** | ❌ | ❌ | ❌ | ✅ |
| **yt-dlp-generator** | ❌ | ❌ | ✅ | ❌ |
| **px86 Extension** | ✅ | ❌ | ✅ | ❌ |

### Download-Funktionen

| Extension | Video DL | Audio DL | Qualitätswahl | Playlist | Warteschlange | Verlauf |
|-----------|:--------:|:--------:|:-------------:|:--------:|:-------------:|:-------:|
| **DerSauger** | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Grabby** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **mpvnet** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Tetsuo-DL** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **metube-extension** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **yt-dlp-generator** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **px86 Extension** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

### Konvertierung & Verarbeitung

| Extension | Auto-Konvert. | WAV Output | MP3 Output | FFmpeg | yt-dlp Update |
|-----------|:-------------:|:----------:|:----------:|:------:|:-------------:|
| **DerSauger** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Grabby** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **mpvnet** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Tetsuo-DL** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **metube-extension** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **yt-dlp-generator** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **px86 Extension** | ❌ | ❌ | ❌ | ❌ | ❌ |

### Installation & Benutzererfahrung

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

## Architektur-Vergleich

### Native Messaging (DerSauger, Grabby, mpvnet, px86)

```
┌─────────────────┐     Native Messaging      ┌──────────────────┐
│ Browser         │ ◄─────────────────────────► Native Host      │
│ Extension       │     (JSON Nachrichten)    │ (Python/exe)     │
└─────────────────┘                           └────────┬─────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │ yt-dlp + FFmpeg  │
                                              └──────────────────┘
```

**Vorteile**:
- Kein Server erforderlich
- Direkte Kommunikation
- Sicherer (keine offenen Ports)

**Nachteile**:
- Plattformspezifische Installation
- Native Host muss registriert werden

### Lokaler Server (Tetsuo-DL)

```
┌─────────────────┐     HTTP (localhost)      ┌──────────────────┐
│ Browser         │ ◄─────────────────────────► Node.js Server   │
│ Extension       │     (Port 17171)          │                  │
└─────────────────┘                           └────────┬─────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │ yt-dlp + FFmpeg  │
                                              └──────────────────┘
```

**Vorteile**:
- Einfacher zu entwickeln
- Browser-übergreifend kompatible API

**Nachteile**:
- Server muss im Hintergrund laufen
- Offener Port (potentielles Sicherheitsrisiko)

### Self-Hosted Server (metube-extension)

```
┌─────────────────┐     HTTP (Netzwerk)       ┌──────────────────┐
│ Browser         │ ◄─────────────────────────► MeTube Server    │
│ Extension       │                           │ (Docker)         │
└─────────────────┘                           └────────┬─────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │ yt-dlp + FFmpeg  │
                                              └──────────────────┘
```

**Vorteile**:
- Kann auf separatem Rechner laufen
- Web-UI verfügbar
- Mehrere Nutzer

**Nachteile**:
- Server-Setup erforderlich
- Komplexere Infrastruktur

---

## DerSaugers Alleinstellungsmerkmale

Basierend auf der umfassenden Analyse oben bietet DerSauger eine einzigartige Kombination von Funktionen, die in keiner anderen Extension zu finden ist:

### 1. Einzige Extension mit automatischer WAV-Konvertierung

**DerSauger ist die einzige Browser-Extension, die heruntergeladene Medien automatisch ins WAV-Format konvertiert.** Dies ist essentiell für:
- Audio-Produktions-Workflows
- Verlustfreie Audio-Archivierung
- Professionelle Audiobearbeitung

### 2. Chrome + Firefox + Native Messaging + Windows

| Kombination | DerSauger | Andere |
|-------------|:---------:|:------:|
| Chrome + Firefox | ✅ | mpvnet (nur Linux) |
| Native Messaging | ✅ | Grabby (primär Firefox) |
| Windows Support | ✅ | mpvnet ❌ |
| **Alles kombiniert** | ✅ | ❌ |

### 3. Serverlose Voll-Feature-Lösung

Im Gegensatz zu Tetsuo-DL (benötigt Node.js Server) oder metube-extension (benötigt Docker), benötigt DerSauger:
- Keinen Hintergrund-Server
- Keine offenen Ports
- Kein Docker-Setup
- Einfach installieren und nutzen

### 4. Professioneller Windows Installer

DerSauger enthält einen professionellen NSIS Installer, der:
- Python Virtual Environments einrichtet
- Native Messaging Hosts registriert
- yt-dlp und FFmpeg installiert
- Einen ordentlichen Uninstaller erstellt

### 5. Eingebautes yt-dlp Auto-Update

Nur DerSauger und Tetsuo-DL bieten automatische yt-dlp Updates. Kombiniert mit der Native Messaging Architektur macht dies DerSauger einzigartig.

---

## Feature-Ideen von Konkurrenten

Basierend auf dieser Analyse könnten folgende Features von Konkurrenten DerSauger verbessern:

### Von Tetsuo-DL

| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Download-Warteschlange | Mehrere Downloads in Warteschlange stellen | Mittel |
| Download-Verlauf | Frühere Downloads nachverfolgen | Mittel |
| Dark Mode | Modernes dunkles Theme | Niedrig |
| Fortschrittsverfolgung | Download-Fortschritt mit ETA anzeigen | Mittel |
| Tastaturkürzel | Schnellzugriffs-Hotkeys | Niedrig |

### Von Grabby

| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| Qualitätswahl | Video/Audio-Qualität vor Download wählen | Hoch |
| Link-Grabber | Alle Links auf einer Seite erfassen und filtern | Mittel |
| Download-Manager Integration | Externe Download-Manager unterstützen | Niedrig |

### Von mpvnet

| Feature | Beschreibung | Priorität |
|---------|--------------|-----------|
| mpv Player Integration | Direkt in mpv abspielen | Niedrig |
| Linux Support | Plattformübergreifende Unterstützung | Mittel |

---

## Fazit

DerSauger nimmt eine einzigartige Position im yt-dlp Browser-Extension Ökosystem ein durch die Kombination von:

1. **Browser-übergreifende Unterstützung** (Chrome + Firefox)
2. **Native Messaging Architektur** (kein Server erforderlich)
3. **Automatische Format-Konvertierung** (einzigartige WAV-Unterstützung)
4. **Professioneller Windows Installer**
5. **yt-dlp Auto-Updates**

Die Hauptkonkurrenten sind:
- **Grabby**: Mehr Features aber Firefox-fokussiert und komplexer
- **mpvnet**: Ähnliche Architektur aber nur Linux
- **Tetsuo-DL**: Bessere UI/UX aber benötigt lokalen Server

---

## Links & Ressourcen

### DerSauger
- Repository: https://github.com/GrafKrausula/DerSauger

### Konkurrenten
- Grabby: https://github.com/pouriap/Grabby
- mpvnet: https://github.com/MasterDevX/mpvnet
- Tetsuo-DL: https://github.com/tetsuo-ai/Tetsuo-DL
- metube-extension: https://github.com/Rpsl/metube-browser-extension
- yt-dlp-generator: https://github.com/xdev23/yt-dlp-generator
- px86 Extension: https://github.com/px86/yt-dlp-firefox-extension
- url-saver: https://github.com/mduncs/url-saver
- youtube-downloader-yt-dlp-local: https://github.com/CosmiX-6/youtube-downloader-yt-dlp-local

### Verwandte Projekte
- yt-dlp: https://github.com/yt-dlp/yt-dlp
- MeTube: https://github.com/alexta69/metube
- FFmpeg: https://ffmpeg.org/
