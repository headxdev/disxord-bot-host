# 🚀 START HERE - Discord Bot Manager

**Version 2.0 - Universal Edition**  
**Created by headx & the psychon**

---

## ⚡ Quick Start (1 Minute)

### Alles was Sie brauchen ist ONE Befehl:

```bash
python start.py
```

Das war's! 🎉

Der **start.py** Script macht ALLES automatisch:
- ✅ Erkennt Ihr Betriebssystem (Windows/Linux/macOS)
- ✅ Prüft Python-Version
- ✅ Installiert Dependencies automatisch
- ✅ Erstellt notwendige Verzeichnisse
- ✅ Generiert Konfigurationsdateien
- ✅ Startet den Server

---

## 📁 Welche Dateien sind wichtig?

### ✅ VERWENDEN SIE DIESE:

```
📄 start.py              ← HAUPTDATEI - Starten Sie IMMER diese!
📄 auth.py               ← OAuth2 Handler (wird automatisch geladen)
📄 index.html            ← Web-Interface
📄 script.js             ← Frontend-Logik
📄 auth-handler.js       ← OAuth2 Frontend
📄 styles.css            ← Haupt-Styling
📄 auth-styles.css       ← Auth-Styling
📄 .env                  ← Ihre Konfiguration (wird automatisch erstellt)
📄 requirements.txt      ← Python-Dependencies
```

### ❌ IGNORIEREN SIE DIESE (Legacy/Deprecated):

```
🚫 quickstart.sh         ← Veraltet (Logik jetzt in start.py)
🚫 quickstart.bat        ← Veraltet (Logik jetzt in start.py)
🚫 install.sh            ← Veraltet (Logik jetzt in start.py)
🚫 install.bat           ← Veraltet (Logik jetzt in start.py)
🚫 setup.py              ← Veraltet (Logik jetzt in start.py)
🚫 install.py            ← Veraltet (Logik jetzt in start.py)
🚫 bot_manager.py        ← Veraltet (Merged in start.py)
```

---

## 🖥️ Unterstützte Betriebssysteme

Der **start.py** Script funktioniert auf ALLEN Plattformen:

### ✅ Windows
- Windows 10/11 (vollständig getestet)
- Windows 7/8 (sollte funktionieren)
- PowerShell und CMD unterstützt
- Automatische ANSI-Farben-Aktivierung

### ✅ Linux
- Ubuntu / Debian
- Fedora / RHEL / CentOS
- Arch Linux
- openSUSE
- Alpine Linux
- Und mehr...

### ✅ macOS
- macOS 10.14+ (Mojave und neuer)
- Apple Silicon (M1/M2) und Intel
- Homebrew wird automatisch installiert

---

## 📋 Was passiert beim ersten Start?

### Schritt 1: System-Prüfung
```
✓ Python-Version geprüft (3.8+ erforderlich)
✓ Betriebssystem erkannt
✓ Package Manager erkannt
```

### Schritt 2: Dependencies
```
✓ Python-Packages installiert
✓ Optional: PHP installiert (für erweiterte Features)
✓ Alle Requirements erfüllt
```

### Schritt 3: Setup
```
✓ Verzeichnisse erstellt (bots/, logs/, data/)
✓ .env Konfiguration erstellt
✓ Setup als abgeschlossen markiert
```

### Schritt 4: Server Start
```
🚀 Server läuft auf http://localhost:8000
✅ Bereit für Ihre Bots!
```

---

## 🔧 Konfiguration

Nach dem ersten Start finden Sie eine `.env` Datei:

```env
# Server
HOST=0.0.0.0
PORT=8000

# Discord OAuth2 (Optional)
DISCORD_CLIENT_ID=IHR_CLIENT_ID
DISCORD_CLIENT_SECRET=IHR_SECRET
DISCORD_REDIRECT_URI=http://localhost:8000/auth/callback
```

### Discord OAuth2 aktivieren (Optional):

1. Gehe zu https://discord.com/developers/applications
2. Erstelle neue Application
3. Kopiere Client ID und Secret
4. Trage in `.env` ein
5. Starte Server neu: `python start.py`

**Detaillierte Anleitung:** Siehe [DISCORD_OAUTH_SETUP.md](DISCORD_OAUTH_SETUP.md)

---

## 🎯 Häufige Fragen

### Q: Muss ich etwas manuell installieren?
**A:** Nein! `start.py` macht alles automatisch.

### Q: Funktioniert das auf meinem Raspberry Pi?
**A:** Ja! Funktioniert auf ARM-basierten Linux-Systemen.

### Q: Brauche ich Admin-Rechte?
**A:** 
- Windows: Nein (außer für optionale PHP-Installation)
- Linux: Ja für PHP-Installation (wird gefragt)
- macOS: Ja für Homebrew (wird gefragt)

### Q: Was wenn etwas schief geht?
**A:** Der Script gibt hilfreiche Fehlermeldungen und macht weiter, auch wenn optionale Komponenten fehlschlagen.

### Q: Warum gibt es so viele Dateien?
**A:** Legacy-Dateien (quickstart, install, etc.) können gelöscht werden. Sie sind nicht mehr nötig.

### Q: Kann ich den Port ändern?
**A:** Ja! Bearbeite `.env` und ändere `PORT=8000` zu Ihrem Wunsch-Port.

---

## 🚨 Troubleshooting

### Problem: "Python not found"
```bash
# Lösung: Python installieren
# Windows: https://python.org/downloads
# Linux: sudo apt install python3
# macOS: brew install python3
```

### Problem: "Permission denied"
```bash
# Linux/macOS: Script ausführbar machen
chmod +x start.py

# Oder direkt mit Python:
python3 start.py
```

### Problem: "Port already in use"
```bash
# Lösung 1: Anderen Port in .env setzen
PORT=8001

# Lösung 2: Prozess auf Port 8000 beenden
# Windows: netstat -ano | findstr :8000
# Linux/macOS: lsof -i :8000
```

### Problem: Dependencies installieren fehl
```bash
# Manuelle Installation:
pip install -r requirements.txt

# Oder minimal:
pip install discord.py python-dotenv aiohttp
```

---

## 📚 Weitere Dokumentation

- **[README.md](README.md)** - Komplette Dokumentation
- **[DISCORD_OAUTH_SETUP.md](DISCORD_OAUTH_SETUP.md)** - OAuth2 Setup
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Detaillierte Anleitung
- **[API.md](API.md)** - API Dokumentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution Guide

---

## 💡 Pro-Tipps

### Tipp 1: Entwicklungs-Modus
```bash
# Debug-Modus aktivieren
# In .env setzen:
DEBUG=True
LOG_LEVEL=DEBUG
```

### Tipp 2: Auto-Restart bei Code-Änderungen
```bash
# Installiere watchdog (wird automatisch gemacht)
# Server überwacht dann Datei-Änderungen
```

### Tipp 3: Virtual Environment (empfohlen)
```bash
# Erstellen
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Dann starten:
python start.py
```

### Tipp 4: Updates
```bash
# Git pull für neue Features
git pull origin main

# Dependencies aktualisieren
pip install -r requirements.txt --upgrade

# Starten
python start.py
```

---

## 🎉 Sie sind bereit!

Einfach ausführen:
```bash
python start.py
```

Öffnen Sie Ihren Browser:
```
http://localhost:8000
```

Und legen Sie los! 🚀

---

## 📞 Support

- **GitHub Issues**: Bug Reports
- **Discussions**: Fragen & Ideen
- **Pull Requests**: Verbesserungen

---

**Developed with ❤️ by headx & the psychon**

*"One script to rule them all!" - Universal Edition*

---

## ⭐ Features auf einen Blick

✅ **Cross-Platform** - Windows, Linux, macOS  
✅ **Auto-Setup** - Keine manuelle Konfiguration  
✅ **Smart Detection** - Erkennt Ihr System automatisch  
✅ **Discord OAuth2** - Ein-Klick Bot-Import  
✅ **Beautiful UI** - Cosmic Space Theme  
✅ **Code Editor** - Integriert im Browser  
✅ **Templates** - Vorgefertigte Commands  
✅ **Live Logs** - Echtzeit Bot-Überwachung  
✅ **Export/Import** - Bots einfach teilen  
✅ **Responsive** - Mobile-friendly  

---

**Das war's! Viel Spaß mit dem Discord Bot Manager! 🎊**
