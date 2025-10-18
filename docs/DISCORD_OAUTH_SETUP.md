# Discord OAuth2 Setup Guide

**Created by headx & the psychon**

Diese Anleitung hilft Ihnen, Discord OAuth2 für den Bot Manager einzurichten, damit Benutzer ihre Discord-Accounts verbinden und ihre Bots automatisch importieren können.

## 📋 Voraussetzungen

- Ein Discord-Account
- Zugriff auf das [Discord Developer Portal](https://discord.com/developers/applications)
- Der Discord Bot Manager muss installiert sein

## 🚀 Schritt-für-Schritt-Anleitung

### 1. Discord Application erstellen

1. Gehen Sie zum [Discord Developer Portal](https://discord.com/developers/applications)
2. Klicken Sie auf **"New Application"**
3. Geben Sie einen Namen ein (z.B. "Discord Bot Manager")
4. Akzeptieren Sie die Terms of Service
5. Klicken Sie auf **"Create"**

### 2. OAuth2 konfigurieren

1. Klicken Sie in Ihrer Application auf **"OAuth2"** im linken Menü
2. Scrollen Sie zu **"Redirects"**
3. Klicken Sie auf **"Add Redirect"**
4. Fügen Sie folgende URL hinzu:
   ```
   http://localhost:8000/auth/callback
   ```
5. Klicken Sie auf **"Save Changes"**

### 3. Client ID und Secret kopieren

1. Gehen Sie zurück zur **"General Information"** Seite
2. Kopieren Sie die **"Application ID"** (auch Client ID genannt)
3. Klicken Sie auf **"Reset Secret"** (wenn Sie noch keines haben)
4. Kopieren Sie den **"Client Secret"**
   
   ⚠️ **WICHTIG**: Der Client Secret wird nur einmal angezeigt! Kopieren Sie ihn sofort!

### 4. Credentials in .env eintragen

1. Öffnen Sie die `.env` Datei in Ihrem Discord Bot Manager Verzeichnis
2. Tragen Sie Ihre Credentials ein:

```env
# Discord OAuth2 Configuration
DISCORD_CLIENT_ID=IHRE_CLIENT_ID_HIER
DISCORD_CLIENT_SECRET=IHR_CLIENT_SECRET_HIER
DISCORD_REDIRECT_URI=http://localhost:8000/auth/callback
```

**Beispiel:**
```env
DISCORD_CLIENT_ID=1234567890123456789
DISCORD_CLIENT_SECRET=aBcD1234eFgH5678iJkL9012mNoPqRsT
DISCORD_REDIRECT_URI=http://localhost:8000/auth/callback
```

### 5. Server neu starten

1. Stoppen Sie den Server (falls er läuft) mit `Ctrl+C`
2. Starten Sie den Server neu:
   ```bash
   python start.py
   ```

## ✅ Funktionstest

1. Öffnen Sie http://localhost:8000 in Ihrem Browser
2. Sie sollten einen **"Mit Discord anmelden"** Button sehen
3. Klicken Sie darauf
4. Sie werden zu Discord weitergeleitet
5. Autorisieren Sie die Application
6. Sie werden zurück zum Bot Manager geleitet
7. Ihr Discord-Profil sollte oben rechts angezeigt werden

## 🎯 Features nach der Anmeldung

Nach erfolgreicher Anmeldung können Sie:

- ✅ Ihre Discord Applications automatisch sehen
- ✅ Bestehende Discord Bots mit einem Klick importieren
- ✅ Bot-Informationen automatisch übernehmen (Name, Icon, etc.)
- ✅ Ihre Bots zentral verwalten

## 🔧 Erweiterte Konfiguration

### Öffentlicher Zugriff (Optional)

Wenn Sie den Bot Manager öffentlich zugänglich machen möchten:

1. **Ändern Sie die Redirect URI** im Discord Developer Portal:
   ```
   https://ihre-domain.com/auth/callback
   ```

2. **Aktualisieren Sie die .env Datei**:
   ```env
   DISCORD_REDIRECT_URI=https://ihre-domain.com/auth/callback
   ```

3. **SSL/HTTPS einrichten** für sichere Verbindungen

### Produktions-Setup

Für Produktionsumgebungen:

```env
HOST=0.0.0.0
PORT=443
ENABLE_HTTPS=True
DISCORD_REDIRECT_URI=https://ihre-domain.com/auth/callback
```

## 🛡️ Scopes und Berechtigungen

Der Bot Manager verwendet folgende OAuth2 Scopes:

- `identify` - Zugriff auf Benutzerprofil
- `email` - Zugriff auf E-Mail-Adresse
- `guilds` - Zugriff auf Server-Liste
- `applications.commands.permissions.update` - Application-Verwaltung

Diese Scopes werden automatisch beim Login angefordert.

## 🔒 Sicherheitshinweise

1. **Client Secret geheim halten!**
   - Teilen Sie Ihr Client Secret NIEMALS öffentlich
   - Committen Sie die .env Datei NICHT in Git
   - Die .env Datei ist bereits in .gitignore

2. **Token-Sicherheit**
   - Bot-Tokens werden nur lokal im Browser gespeichert
   - Niemals Tokens an Dritte weitergeben
   - Tokens können jederzeit im Discord Developer Portal erneuert werden

3. **Redirect URI Whitelist**
   - Nur autorisierte Redirect URIs funktionieren
   - Fügen Sie nur vertrauenswürdige URIs hinzu

## ❓ Troubleshooting

### Problem: "Invalid OAuth2 redirect_uri"

**Lösung:**
- Überprüfen Sie, ob die Redirect URI im Discord Developer Portal korrekt eingetragen ist
- Die URI muss EXAKT mit der in der .env Datei übereinstimmen
- Achten Sie auf http:// vs https://

### Problem: "Invalid client_secret"

**Lösung:**
- Generieren Sie ein neues Client Secret im Discord Developer Portal
- Kopieren Sie es sofort und tragen Sie es in die .env ein
- Starten Sie den Server neu

### Problem: "Application not found"

**Lösung:**
- Überprüfen Sie, ob die Client ID korrekt ist
- Stellen Sie sicher, dass die Application im Developer Portal existiert

### Problem: "Login funktioniert nicht"

**Lösung:**
1. Überprüfen Sie die Browser-Konsole auf Fehler
2. Prüfen Sie die Server-Logs
3. Stellen Sie sicher, dass der Server läuft
4. Testen Sie mit einem anderen Browser

## 📚 Weitere Ressourcen

- [Discord OAuth2 Dokumentation](https://discord.com/developers/docs/topics/oauth2)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord API Documentation](https://discord.com/developers/docs)

## 💬 Support

Bei Problemen:
1. Überprüfen Sie diese Anleitung erneut
2. Schauen Sie in den Server-Logs nach Fehlern
3. Erstellen Sie ein Issue auf GitHub

## 🎉 Fertig!

Sie haben Discord OAuth2 erfolgreich eingerichtet! Ihre Benutzer können jetzt ihre Discord-Accounts verbinden und ihre Bots einfach verwalten.

---

**Viel Erfolg mit dem Discord Bot Manager!**

**Created with ❤️ by headx & the psychon**
