# Development Guide

---

## Logging

### Log-Verzeichnisse

| Komponente | Log-Pfad |
|------------|----------|
| Native Messaging Host | `~/Documents/DerSauger_LOG.txt` |
| WAVing_All_VIDS.py | `~/Documents/DerSauger_Logs/WAVing_All_VIDS.log` |

### Log-Format
```
[2025-12-03 01:23:45] [INFO] Message here
[2025-12-03 01:23:46] [WARN] Warning message
[2025-12-03 01:23:47] [ERROR] Error message
[2025-12-03 01:23:48] [DEBUG] Debug details
```

### Log-Levels
- **INFO** - Normale Operationen, wichtige Ereignisse
- **WARN** - Unerwartete aber handhabbare Situationen
- **ERROR** - Fehler die behoben werden sollten
- **DEBUG** - Detaillierte Infos für Entwickler

### Best Practices
1. **Retention:** Logs älter als 30 Tage werden automatisch gelöscht
2. **Rotation:** Log-Dateien werden bei 10MB rotiert (archiviert mit Timestamp)
3. **Session-Trennung:** Jede Session beginnt mit einer Trennlinie
4. **Konsistenz:** Alle Komponenten loggen in `~/Documents/DerSauger_Logs/`

### Beispiel Log-Output
```
[2025-12-03 01:23:45] [INFO] ============================================================
[2025-12-03 01:23:45] [INFO] Session started - WAVing_All_VIDS.py
[2025-12-03 01:23:45] [INFO] ============================================================
[2025-12-03 01:23:45] [INFO] Arguments received - convertpath: E:\Videos, downloadpath: E:\Downloads, format: wav
[2025-12-03 01:23:45] [INFO] Found mp4 files: ['video1.mp4', 'video2.mp4']
[2025-12-03 01:23:46] [INFO] Converting: video1.mp4 -> wav
[2025-12-03 01:23:50] [INFO] Successfully converted: video1.mp4
[2025-12-03 01:23:55] [INFO] Session completed successfully
```

---

## Development Environment Setup

First you need to setup a venv with python (Python 3.12 is recommended)


### Steps to Install Dev Venv

1. **Virtual Environment creation and activation:**
   It’s a common practice to use a virtual environment to isolate your project dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate   # On Windows
   ```

2. **Ensure `pip` is Installed:**
   Verify that `pip` is installed and up to date:
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Use `pip install` with `-r`:**
   Run the following command, replacing `requirements.txt` with the path to your requirements file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation:**
   After the installation completes, you can check if all packages are installed using:
   ```bash
   pip list
   ```
